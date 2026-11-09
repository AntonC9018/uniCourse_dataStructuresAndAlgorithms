"""The unified trace format: validation, the Timeline converter, and the committed fixtures."""
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'player'))
import fixtures  # noqa: E402
from model import EXPRESSION, SWAP  # noqa: E402
from trace_format import FormatError, from_timeline, reduction_span, scalar, validate  # noqa: E402
import tracing  # noqa: E402

CLANG = os.environ.get('CLANGXX') or shutil.which('clang++')
GDB = os.environ.get('GDB') or shutil.which('gdb')


def kinds(trace):
    return [step['op'] and step['op']['kind'] for step in trace['steps']]


class FixtureTests(unittest.TestCase):
    def test_committed_fixtures_are_current_and_valid(self):
        rendered = fixtures.render()
        self.assertEqual(sorted(rendered), sorted(p.name for p in fixtures.FIXTURES.glob('*.json')))
        for name, content in rendered.items():
            with self.subTest(name):
                self.assertEqual((fixtures.FIXTURES / name).read_text(), content,
                                 'run python3 visualizations/player/fixtures.py')
                validate(json.loads(content))

    def test_pointer_chain_reduces_in_lesson_notation(self):
        trace = fixtures.double_pointer()
        panes = [step['pane'] for step in trace['steps'] if step['line'] == 4]
        self.assertEqual(panes, ['**pp = 7', '**72 = 7', '*p = 7', '*64 = 7', 'a = 7', 'a = 7'])
        self.assertEqual(trace['steps'][-1]['targets'], {'p': 'b', 'pp': 'p'})

    def test_struct_copy_copies_pointer_targets(self):
        trace = fixtures.shallow_copy()
        copied = next(step for step in trace['steps'] if step['op'] and step['op'].get('name') == 's2')
        self.assertEqual(copied['targets'], {'s1.pa': 's1.a', 's2.pa': 's1.a'})
        self.assertEqual(trace['steps'][1]['values']['s1.pa'], 0)


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.trace = fixtures.write_through()

    def rejects(self, message, change):
        broken = copy.deepcopy(self.trace)
        change(broken)
        with self.assertRaisesRegex(FormatError, message):
            validate(broken)

    def test_accepts_a_fixture(self):
        validate(self.trace)

    def test_rejects_other_versions_and_unknown_keys(self):
        self.rejects('format', lambda t: t.update(format=2))
        self.rejects('unknown', lambda t: t.update(colour='red'))
        self.rejects('unknown', lambda t: t['steps'][0].update(extra=1))

    def test_rejects_inconsistent_storage(self):
        self.rejects('overlap', lambda t: t['variables'][1].update(address=66))
        self.rejects('expected exactly', lambda t: t['steps'][2]['values'].pop('b'))
        self.rejects('only a write', lambda t: [s['values'].update(a=9) for s in t['steps'][3:]])
        self.rejects('only pointers', lambda t: t['steps'][-1]['targets'].update(a='b'))

    def test_rejects_operations_that_disagree_with_the_pane(self):
        read = next(i for i, s in enumerate(self.trace['steps']) if (s['op'] or {}).get('kind') == 'read')
        self.rejects('replacement', lambda t: t['steps'][read]['op'].update(value='3'))
        self.rejects('replace', lambda t: t['steps'][read]['op'].update(span=[0, 2]))
        deref = read + 1
        self.rejects('pointer', lambda t: t['steps'][deref]['op'].update(via='a'))
        self.rejects('first step', lambda t: t['steps'][0].update(op={'kind': 'eval'}))

    def test_rejects_output_without_print(self):
        self.rejects('only a print', lambda t: t['steps'][-1].update(op=None))


class OperationValueTests(unittest.TestCase):
    """Operation values must agree with the memory snapshots around them."""

    def rejects(self, trace, message, change):
        broken = copy.deepcopy(trace)
        change(broken['steps'])
        with self.assertRaisesRegex(FormatError, message):
            validate(broken)

    def test_rejects_a_write_that_memory_contradicts(self):
        # The reported case: `int a = 5;` writes 5, but memory says 999.
        trace = {'format': 1, 'source': ['int a = 5;'], 'variables': [scalar('a', 64)],
                 'steps': [{'line': 0, 'pane': 'int a = 5', 'values': {'a': None}, 'targets': {},
                            'stdout': '', 'hold': 1, 'op': None},
                           {'line': 0, 'pane': 'int a = 5', 'values': {'a': 999}, 'targets': {},
                            'stdout': '', 'hold': 1,
                            'op': {'kind': 'write', 'name': 'a', 'value': '5', 'span': [8, 9],
                                   'destination': [4, 5]}}]}
        self.rejects(trace, r'a holds 999 after the write, not .5.', lambda steps: None)
        trace['steps'][1]['values']['a'] = 5
        validate(trace)

    def test_rejects_a_struct_copy_that_memory_contradicts_field_by_field(self):
        trace = fixtures.copy_assignment()
        write = next(i for i, s in enumerate(trace['steps']) if (s['op'] or {}).get('name') == 'b')

        def change(steps):
            for step in steps[write:]:
                step['values']['b.f2'] = 9
        self.rejects(trace, r'b holds \{5, 9\} after the write, not .\{5, 6\}.', change)
        self.rejects(trace, r'a holds \{5, 6\} before the read, not .\{5\}.',
                     lambda steps: replace_text(steps[write - 1:write + 1], '{5, 6}', '{5}'))

    def test_null_pointers_are_stored_as_zero(self):
        trace = fixtures.shallow_copy()
        self.assertEqual(trace['steps'][1]['op']['value'], '{nullptr, 1}')
        self.assertEqual(trace['steps'][1]['values']['s1.pa'], 0)
        self.rejects(trace, r's1 holds \{\?, 1\} after the write, not .\{nullptr, 1\}.',
                     lambda steps: steps[1]['values'].update({'s1.pa': '?'}))

    def test_rejects_text_that_is_not_a_value(self):
        trace = fixtures.write_through()
        self.rejects(trace, 'is not a value', lambda steps: replace_text(steps[:2], '1', 'one'))

    def test_rejects_a_read_that_memory_contradicts(self):
        trace = fixtures.write_through()
        read = 6  # `*b = 2` → `*64 = 2`: b holds 64.
        self.assertEqual(trace['steps'][read]['op']['kind'], 'read')
        self.rejects(trace, r'b holds 64 before the read, not .68.',
                     lambda steps: replace_text(steps[read:read + 1], '64', '68'))

    def test_rejects_a_wrong_address(self):
        trace = fixtures.write_through()
        addr = 3  # `int* b = &a` → `int* b = 64`.
        self.assertEqual(trace['steps'][addr]['op']['kind'], 'addr')
        self.rejects(trace, r'the address of a is 64, not .68.',
                     lambda steps: replace_text(steps[addr:addr + 1], '64', '68'))

    def test_rejects_a_dereference_to_somewhere_else(self):
        trace = fixtures.reassign()
        deref = next(i for i, s in enumerate(trace['steps']) if (s['op'] or {}).get('kind') == 'deref')
        self.rejects(trace, 'p does not point to b',
                     lambda steps: (steps[deref]['op'].update(target='b'),
                                    steps[deref].update(pane=steps[deref]['pane'].replace('a', 'b', 1))))

    def test_rejects_targets_that_disagree_with_pointer_values(self):
        trace = fixtures.write_through()
        self.rejects(trace, r'b holds 68, but a is at 64',
                     lambda steps: [step['values'].update(b=68) for step in steps[4:]])
        self.rejects(trace, 'b holds the address 64 but points nowhere',
                     lambda steps: [step['targets'].clear() for step in steps[4:]])
        self.rejects(trace, 'only pointers', lambda steps: steps[-1]['targets'].update(a='b'))


def replace_text(steps, old, new):
    """Change a value's text in the panes and operations of `steps`, keeping spans valid.

    Reductions index the previous pane, so only the spans of writes and prints move."""
    for step in steps:
        at = step['pane'].index(old)
        step['pane'] = step['pane'].replace(old, new, 1)
        op = step['op'] or {}
        if 'value' in op:
            op['value'] = op['value'].replace(old, new, 1)
        for key in ('span', 'destination') if op.get('kind') in ('write', 'print') else ():
            if key in op and op[key][1] > at:
                op[key] = [op[key][0], op[key][1] + len(new) - len(old)]


class ConverterTests(unittest.TestCase):
    def test_manual_expression_timeline(self):
        trace = from_timeline(EXPRESSION)
        self.assertEqual(trace['format'], 1)
        self.assertEqual(kinds(trace), [None, 'write', None, 'read', 'eval', 'write', None, 'write',
                                        None, 'read', 'print'])
        self.assertEqual([s['pane'] for s in trace['steps'][2:6]],
                         ['int b = a + 6;', 'int b = 5 + 6;', 'int b = 11;', 'int b = 11;'])
        self.assertEqual(trace['steps'][4]['op'], {'kind': 'eval', 'value': '11', 'span': [8, 13]})
        self.assertEqual(trace['steps'][5]['op']['destination'], [4, 5])
        self.assertEqual(trace['spans'], [[6, 7], [6, 11], [4, 5], [13, 14]])
        self.assertEqual(trace['steps'][-1]['stdout'], '11')

    def test_swap_writes_unchanged_values(self):
        trace = from_timeline(SWAP)
        self.assertEqual(kinds(trace).count('write'), 4)
        self.assertEqual(trace['steps'][-1]['values'], {'a': 2, 'b': 2})

    def test_reduction_spans(self):
        cases = [('5 + 6', '11', [0, 5]), ('(15) * 12', '15 * 12', [0, 4]),
                 ('1 * 1 + 1', '1 + 1', [0, 5]), ('1 + 1 * 1', '1 + 1', [4, 9]),
                 ('-22 - -1', '-21', [0, 8]), ('-(6) * 3', '-6 * 3', [1, 4]),
                 ('{}', '0', [0, 2]), ('int{}', '0', [0, 5]), ('0x10', '16', [0, 4])]
        for before, after, span in cases:
            with self.subTest(before):
                self.assertEqual(reduction_span(before, after), span)


@unittest.skipUnless(CLANG, 'Clang is required for AST integration tests')
class TracedConversionTests(unittest.TestCase):
    def convert(self, source):
        return from_timeline(tracing.trace(source, runtime=False))

    def test_empty_braces_turn_into_zero(self):
        trace = self.convert('int a{}; a = {}; int b = int{};')
        self.assertEqual([s['pane'] for s in trace['steps'][:2]], ['int a = {};', 'int a = 0;'])
        self.assertEqual(trace['steps'][1]['op'], {'kind': 'eval', 'value': '0', 'span': [8, 10]})
        self.assertEqual(trace['spans'][0], [5, 7])

    def test_declaration_shows_unknown_value(self):
        trace = self.convert('int a; a = 2 * 3 + 1;')
        self.assertEqual(trace['steps'][0]['values'], {'a': '?'})
        self.assertIsNone(trace['spans'][0])
        self.assertEqual([s['pane'] for s in trace['steps'] if s['line'] == 1],
                         ['a = 2 * 3 + 1;', 'a = 6 + 1;', 'a = 7;', 'a = 7;'])

    def test_parentheses_and_repeated_reads(self):
        trace = self.convert('int c{12}; int o{3}; int r = (c + o) * c;')
        panes = [s['pane'] for s in trace['steps'] if s['line'] == 2]
        self.assertEqual(panes, ['int r = (c + o) * c;', 'int r = (12 + o) * c;', 'int r = (12 + 3) * c;',
                                 'int r = (15) * c;', 'int r = 15 * c;', 'int r = 15 * 12;',
                                 'int r = 180;', 'int r = 180;'])


@unittest.skipUnless(CLANG and GDB, 'Clang and GDB are required for runtime traces')
class GenerateCommandTests(unittest.TestCase):
    def test_trace_prints_the_unified_format_deterministically(self):
        with tempfile.NamedTemporaryFile('w', suffix='.cpp') as source:
            source.write('int a = 5;\nint b = a + 6;\na = 7;\nstd::cout << b << std::endl;\n')
            source.flush()
            output = subprocess.run([sys.executable, str(ROOT / 'generate.py'), 'trace', '--source',
                                     source.name], capture_output=True, text=True, check=True).stdout
        trace = json.loads(output)
        validate(trace)
        self.assertEqual(output.strip(), json.dumps(trace, sort_keys=True))
        self.assertEqual(trace['steps'][-1]['stdout'], '11\n')


if __name__ == '__main__':
    unittest.main()
