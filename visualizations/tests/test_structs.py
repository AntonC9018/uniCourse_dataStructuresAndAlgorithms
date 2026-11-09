"""Aggregate tracing against Clang's ABI and GDB, including pointer aliasing."""
import json
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tracing
import generate
from tracing import Unsupported
from trace_format import validate

CLANG = os.environ.get('CLANGXX') or shutil.which('clang++')
GDB = os.environ.get('GDB') or shutil.which('gdb')

STRUCT_POINTERS = '''struct S { int x; int *p; S *next; };
int a=1;
S s{2,&a,nullptr};
S t=s;
t=s;
S *p=&s;
p->x=3;
int *q=&s.x;
*t.p=7;
std::cout << p->x;
'''


@unittest.skipUnless(CLANG and GDB, 'Clang and GDB are required')
class StructTests(unittest.TestCase):
    def test_shallow_copy_preserves_pointer_fields(self):
        result = tracing.trace(STRUCT_POINTERS)
        validate(result)
        last = result['steps'][-1]
        self.assertEqual(last['targets'], {'s.p': 'a', 't.p': 'a', 'p': 's', 'q': 's.x'})
        self.assertEqual(last['values']['s.x'], 3)
        self.assertEqual(last['values']['t.x'], 2)
        self.assertEqual(last['values']['a'], 7)
        self.assertEqual(last['stdout'], '3')
        variables = {v['name']: v for v in result['variables']}
        self.assertEqual(variables['s']['size'], 24)
        self.assertEqual([f['offset'] for f in variables['s']['fields']], [0, 8, 16])
        self.assertEqual(variables['s']['fields'], variables['t']['fields'])
        # These addresses coincide, but their arcs have different endpoints.
        self.assertEqual(last['values']['p'], last['values']['q'])

    def test_initialization_copies_and_arrow_chains(self):
        source = '''struct S {int x; S *next;};
S a{.x=4}; S b{a}; S c{}; c=b; b.next=&a; S *p=&b;
p->next->x=9; c=*p; (*p).x=7; std::cout << a.x;'''
        result = tracing.trace(source)
        last = result['steps'][-1]
        self.assertEqual(last['stdout'], '9')
        self.assertEqual(last['values']['c.x'], 4)
        self.assertEqual(last['values']['b.x'], 7)
        self.assertEqual(last['targets'], {'b.next': 'a', 'c.next': 'a', 'p': 'b'})

    def test_elided_aggregate_initialization_and_struct_double_pointer(self):
        result = tracing.trace('struct S {int x;}; S a=S{1}; S b{}; S *p=&a; '
                               'S **pp=&p; b=**pp; p->x=9;')
        self.assertEqual(result['steps'][-1]['values']['a.x'], 9)
        self.assertEqual(result['steps'][-1]['values']['b.x'], 1)

    def test_probe_and_trace_reject_materialized_temporaries_before_execution(self):
        for source in ('struct S {int x;}; S a{1}; a=S{2}; int b=3;',
                       'struct S {int x;}; S a{1}; int b=3; a=S{2};',
                       'struct S {int x;}; S a{1}; S *p=&a; *p=S{2};'):
            with self.subTest(source=source), tempfile.TemporaryDirectory() as temporary:
                path = Path(temporary) / 'source.cpp'
                path.write_text(source)
                results = {}
                for operation in ('probe', 'trace'):
                    stdout, stderr = StringIO(), StringIO()
                    with (patch.object(sys, 'argv', ['generate.py', operation, '--source', str(path)]),
                          patch.object(tracing, 'execute') as execute,
                          redirect_stdout(stdout), redirect_stderr(stderr)):
                        status = generate.main()
                    execute.assert_not_called()
                    if operation == 'probe':
                        self.assertEqual(status, 0)
                        results[operation] = json.loads(stdout.getvalue())
                    else:
                        self.assertEqual(status, 1)
                        results[operation] = stderr.getvalue().strip()
                self.assertFalse(results['probe']['supported'])
                self.assertIn('materialized temporaries', results['probe']['reason'])
                self.assertEqual(results['trace'], 'unsupported: ' + results['probe']['reason'])

    def test_uninitialized_fields_are_tracked_independently(self):
        result = tracing.trace('struct S {int x; int *p;}; S a; a.x=3; a.p=&a.x; S b=a;')
        self.assertEqual(result['steps'][1]['values']['a.x'], '?')
        last = result['steps'][-1]
        self.assertEqual(last['values']['b.x'], 3)
        self.assertEqual(last['targets'], {'a.p': 'a.x', 'b.p': 'a.x'})

    def test_elaborated_local_struct_pointers(self):
        for spelling in ('S', 'struct S'):
            with self.subTest(spelling=spelling):
                source = ('struct S {int x;}; S s{1}; '
                          f'{spelling} *p=&s; p->x=2; '
                          f'{spelling} **pp=&p; (*pp)->x=3;')
                result = tracing.trace(source)
                self.assertEqual(result, tracing.trace(source, runtime=False))
                last = result['steps'][-1]
                self.assertEqual(last['values']['s.x'], 3)
                self.assertEqual(last['targets'], {'p': 's', 'pp': 'p'})

    def test_elaborated_struct_pointer_fields(self):
        for spelling in ('S', 'struct S'):
            with self.subTest(spelling=spelling):
                source = (f'struct S {{int x; {spelling} *next;}}; '
                          'S a{1,nullptr}; S b{2,&a}; b.next->x=9; '
                          'b.next=&b; b.next->x=7;')
                result = tracing.trace(source)
                self.assertEqual(result, tracing.trace(source, runtime=False))
                last = result['steps'][-1]
                self.assertEqual(last['values']['a.x'], 9)
                self.assertEqual(last['values']['b.x'], 7)
                self.assertEqual(last['targets'], {'b.next': 'b'})

    def test_multiple_types_and_forward_declarations(self):
        result = tracing.trace('struct B; struct A {B *p;}; struct B {int x;}; '
                               'B b{8}; A a{&b}; std::cout << a.p->x;')
        self.assertEqual(result['steps'][-1]['stdout'], '8')

    def test_cold_runs_and_probe_layout(self):
        first = tracing.trace(STRUCT_POINTERS)
        self.assertEqual(first, tracing.trace(STRUCT_POINTERS, runtime=False))
        self.assertEqual(json.dumps(first, sort_keys=True),
                         json.dumps(tracing.trace(STRUCT_POINTERS), sort_keys=True))

    def test_unsupported_definitions_and_reads_never_execute(self):
        cases = {
            'struct S {double x;}; S s{};': 'unsupported field type double',
            'struct S {int x[2];}; S s{};': 'unsupported field type int',
            'struct S {int x:2;}; S s{};': 'bitfields',
            'struct S {int x=1;}; S s{};': 'default initializers',
            'struct S {int x; S(){x=1;}}; S s;': 'methods',
            'struct A {int x;}; struct B {A a;}; B b{};': 'unsupported field type A',
            'struct S {}; S s{};': 'empty structs',
            'struct S {int x;}; S a; S b=a;': 'uninitialized struct',
            'struct S {int x;}; S a; int b=a.x;': 'uninitialized variable a.x',
            'struct S {int x;}; S *p{}; p->x=1;': 'null pointer p',
        }
        for source, reason in cases.items():
            with self.subTest(source=source), patch.object(tracing, 'execute') as execute:
                with self.assertRaisesRegex(Unsupported, reason):
                    tracing.trace(source)
                execute.assert_not_called()

    def test_generated_browser_fixture_is_current(self):
        path = Path(__file__).parent / 'fixtures' / 'struct-generated.json'
        fixture = json.loads(path.read_text())
        self.assertEqual(tracing.trace('\n'.join(fixture['source'])), fixture)

    def test_unchanged_field_mismatch_is_fatal(self):
        original = tracing.execute
        def corrupted(*args):
            execution = original(*args)
            from dataclasses import replace
            last = execution.checkpoints[-1]
            last['s.x'] = replace(last['s.x'], value=999)
            return execution
        with patch.object(tracing, 'execute', side_effect=corrupted):
            with self.assertRaisesRegex(Unsupported, 's.x disagrees'):
                tracing.trace('struct S {int x; int y;}; S s{1,2}; s.y=3;')
