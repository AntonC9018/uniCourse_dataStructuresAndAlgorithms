"""Compiler-backed static layouts and validation, including nonexecuting probes."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from layout import trace
from trace_format import validate, FormatError
from toolchain import Unsupported


class LayoutTests(unittest.TestCase):
    def test_padding_and_types(self):
        result = trace('struct A { uint8_t f1; int f2; uint8_t f3; };')
        record = result['records'][0]
        self.assertEqual((record['size'], record['alignment']), (12, 4))
        self.assertEqual([f['offset'] for f in record['fields']], [0, 4, 8])
        result = trace('struct B { int8_t a; int* p; size_t n; uint64_t v; };')
        record = result['records'][0]
        self.assertEqual((record['size'], record['alignment']), (32, 8))
        self.assertEqual([f['size'] for f in record['fields']], [1, 8, 8, 8])

    def test_multiple_and_no_execution(self):
        result = trace('struct A { int a; }; struct B { A* p; }; while (true) {}')
        self.assertEqual([r['name'] for r in result['records']], ['A', 'B'])

    def test_unsupported(self):
        for source in ('int a;', 'struct A {};', 'struct A { double x; };',
                       'struct A { int x:2; };', 'struct A { int x[2]; };'):
            with self.subTest(source=source), self.assertRaises(Unsupported):
                trace(source)

    def test_shadowed_type_names(self):
        # The snippet's own alias decides the size, not the companion's <cstdint>.
        record = trace('using uint8_t = uint64_t; struct A { uint8_t x; };')['records'][0]
        self.assertEqual((record['size'], record['fields'][0]['size']), (8, 8))
        self.assertEqual(record['fields'][0]['type'], 'uint8_t')
        for source in ('struct uint8_t { int a; int b; }; struct A { uint8_t x; };',
                       'using size_t = double; struct A { size_t x; };'):
            with self.subTest(source=source), self.assertRaises(Unsupported):
                trace(source)

    def test_invalid_layout(self):
        result = trace('struct A { int a; int b; };')
        for key, value in [('offset', 2), ('size', 20), ('kind', 'float')]:
            bad = copy.deepcopy(result)
            bad['records'][0]['fields'][1][key] = value
            with self.assertRaises(FormatError):
                validate(bad)

    def test_cli_probe_matches_trace(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'example.cpp'
            path.write_text('struct A { uint8_t a; int b; };')
            command = [sys.executable, str(Path(__file__).resolve().parents[1] / 'generate.py')]
            for operation in ('probe', 'trace'):
                result = subprocess.run(command + [operation, '--template', 'layout', '--source', str(path)],
                                        capture_output=True, text=True, check=True)
                data = json.loads(result.stdout)
                self.assertEqual(data['template'] if operation == 'probe' else data['kind'], 'layout')
