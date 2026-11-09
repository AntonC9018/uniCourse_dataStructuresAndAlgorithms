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
from trace_format import FormatError, validate  # noqa: E402

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
