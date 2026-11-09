"""The unified trace format: validation, the committed fixtures and the trace command."""
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
from trace_format import FORMAT, FormatError, scalar, validate  # noqa: E402

CLANG = os.environ.get('CLANGXX') or shutil.which('clang++')
GDB = os.environ.get('GDB') or shutil.which('gdb')


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

    def with_newline(self, spelling, printed='\n'):
        """The fixture followed by `std::cout << <spelling>;`, which prints `printed`."""
        trace, pane = copy.deepcopy(self.trace), 'std::cout << ' + spelling
        last, span = trace['steps'][-1], [13, len(pane)]
        trace['source'].append(pane + ';')
        shown = dict(last, line=last['line'] + 1, pane=pane, op=None, expr=span, hold=1)
        trace['steps'] += [shown, dict(shown, stdout=last['stdout'] + printed,
                                       op={'kind': 'print', 'value': printed, 'span': span})]
        return trace

    def test_whitespace_output_prints_as_it_is_spelled(self):
        for spelling, printed in [('std::endl', '\n'), ("'\\n'", '\n'), ("' '", ' ')]:
            with self.subTest(spelling):
                validate(self.with_newline(spelling, printed))
        for spelling, printed in [('std::endl', ' '), ('std::flush', '\n'), ('"\\n"', '\n')]:
            with self.subTest(spelling), self.assertRaisesRegex(FormatError, 'does not cover'):
                validate(self.with_newline(spelling, printed))
        self.trace = self.with_newline('std::endl')
        self.rejects('stdout must grow', lambda t: t['steps'][-1].update(stdout=t['steps'][-2]['stdout'] + ' '))


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


class LayoutValidationTests(unittest.TestCase):
    """Static layouts must place each field exactly where plain C++ alignment puts it."""

    @staticmethod
    def layout(size, alignment, *fields):
        return {'format': FORMAT, 'kind': 'layout', 'records': [{
            'name': 'A', 'size': size, 'alignment': alignment,
            'fields': [{'name': name, 'offset': offset, 'size': width, 'kind': 'int',
                        'type': 'int' if width == 4 else 'uint8_t'}
                       for name, offset, width in fields]}]}

    def test_accepts_exact_padding(self):
        validate(self.layout(12, 4, ('a', 0, 1), ('b', 4, 4), ('c', 8, 1)))

    def test_rejects_impossible_padding(self):
        cases = {
            'leading': (self.layout(8, 4, ('x', 4, 4)), 'must start at offset 0'),
            'internal': (self.layout(12, 4, ('a', 0, 1), ('b', 8, 4)), 'must start at offset 4'),
            'trailing': (self.layout(12, 4, ('x', 0, 4)), 'size must be 4'),
            'alignment': (self.layout(8, 8, ('a', 0, 4), ('b', 4, 4)), 'alignment must be 4'),
        }
        for padding, (trace, message) in cases.items():
            with self.subTest(padding), self.assertRaisesRegex(FormatError, message):
                validate(trace)


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



@unittest.skipUnless(CLANG and GDB, 'Clang and GDB are required for runtime traces')
class GenerateCommandTests(unittest.TestCase):
    def run_generate(self, operation, source):
        with tempfile.NamedTemporaryFile('w', suffix='.cpp') as handle:
            handle.write(source)
            handle.flush()
            return subprocess.run([sys.executable, str(ROOT / 'generate.py'), operation, '--source',
                                   handle.name], capture_output=True, text=True, check=True).stdout

    def test_trace_prints_the_unified_format_deterministically(self):
        output = self.run_generate('trace', 'int a = 5;\nint b = a + 6;\na = 7;\nstd::cout << b << std::endl;\n')
        trace = json.loads(output)
        validate(trace)
        self.assertEqual(output.strip(), json.dumps(trace, sort_keys=True))
        self.assertEqual(trace['steps'][-1]['stdout'], '11\n')

    def test_pointer_traces_are_byte_identical(self):
        source = 'int a = 5;\nint* p = &a;\nint* q = p;\n*q = 6;\nstd::cout << *p << std::endl;\n'
        first, second = (self.run_generate('trace', source) for _ in range(2))
        self.assertEqual(first, second)
        self.assertEqual(json.loads(first)['steps'][-1]['targets'], {'p': 'a', 'q': 'a'})

    def test_probe_names_the_reason(self):
        supported = json.loads(self.run_generate('probe', 'int a{1};\nint* p{&a};\n*p = 2;\n'))
        self.assertEqual(supported, {'supported': True, 'template': 'expression-timeline'})
        rejected = json.loads(self.run_generate('probe', 'int a{1};\nint* p{&a};\nint* q = p + 1;\n'))
        self.assertEqual(rejected, {'supported': False, 'reason': 'pointer arithmetic and comparison are not supported'})


if __name__ == '__main__':
    unittest.main()
