"""Behavioral coverage for automatic expression traces and fail-closed eligibility."""
from dataclasses import asdict
import os
from pathlib import Path
import shutil
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tracing


CLANG = os.environ.get("CLANGXX") or shutil.which("clang++")
GDB = os.environ.get("GDB") or shutil.which("gdb")


@unittest.skipUnless(CLANG, "Clang is required for AST integration tests")
class StaticTraceTests(unittest.TestCase):
    def check_read_spans(self, timeline):
        for previous, current in zip(timeline.steps, timeline.steps[1:]):
            if current.read and current.transfer is not None:
                start, end = current.read_span
                self.assertEqual(previous.expression[start:end], current.read)
                self.assertEqual(current.expression,
                                 previous.expression[:start] + str(current.transfer)
                                 + previous.expression[end:])

    def test_expression_and_cumulative_output(self):
        timeline = tracing.trace("int a = 5; int b = a + 6; a = 7; std::cout << b << std::endl;", runtime=False)
        expressions = [s.expression for s in timeline.steps if s.line == 1]
        self.assertEqual(expressions, ["a + 6", "5 + 6", "11", "11"])
        self.assertEqual(timeline.steps[-1].values, (7, 11))
        self.assertEqual(timeline.steps[-1].stdout, "11\n")
        self.check_read_spans(timeline)

    def test_precedence_parentheses_and_repeated_reads(self):
        timeline = tracing.trace("int count{12}; int other{3}; int result = (count + other) * count;", runtime=False)
        self.assertEqual(timeline.steps[-1].values, (12, 3, 180))
        self.check_read_spans(timeline)
        self.assertGreaterEqual(sum(s.read == "count" for s in timeline.steps), 2)
        self.assertIn("(15) * count", [s.expression for s in timeline.steps])
        self.assertIn("15 * 12", [s.expression for s in timeline.steps])

    def test_empty_braces_and_typed_value_initialization(self):
        timeline = tracing.trace("int a{}; a = int{}; int b = int{};", runtime=False)
        self.assertEqual(timeline.source[0][slice(*timeline.expression_spans[0])], "{}")
        self.assertEqual([s.expression for s in timeline.steps[:2]], ["{}", "0"])
        self.assertEqual(timeline.steps[-1].values, (0, 0))
        self.assertNotIn("int0", [s.expression for s in timeline.steps])

    def test_whitespace_comments_and_full_main(self):
        timeline = tracing.trace("""#include <iostream>
int main() {
 // Русский комментарий is removed, not executed or displayed.
 int a{ 7 };
 int b = (\n a + 2\n );
 std::cout << b << '\\n';
 return 0;
}
""", runtime=False)
        self.assertEqual(timeline.steps[-1].values, (7, 9))
        self.assertEqual(timeline.steps[-1].stdout, "9\n")
        self.check_read_spans(timeline)

    def test_output_context_survives_later_statements(self):
        timeline = tracing.trace("int a{1}; std::cout << a << std::endl; a=2; std::cout << a << std::endl;", runtime=False)
        after_first = next(i for i, s in enumerate(timeline.steps) if s.stdout)
        self.assertTrue(all(s.stdout.startswith("1\n") for s in timeline.steps[after_first:]))
        self.assertEqual(timeline.steps[-1].stdout, "1\n2\n")

    def test_const_and_auto_copy_are_scalar_values(self):
        timeline = tracing.trace("const int a{5}; auto b=a; b=6; std::cout << a;", runtime=False)
        self.assertEqual(timeline.steps[-1].values, (5, 6))
        self.assertEqual(timeline.steps[-1].stdout, "5")

    def test_uninitialized_storage_is_distinct_from_unallocated(self):
        timeline = tracing.trace("int a; a=5; std::cout << a;", runtime=False)
        self.assertEqual(timeline.steps[0].declared, ("a",))
        self.assertEqual(timeline.steps[0].values, (None,))
        self.assertEqual(timeline.steps[-1].values, (5,))

    def test_unsupported_and_undefined_never_execute(self):
        sources = [
            "int a; std::cout << a;",  # undefined read
            "int a=a;",  # self initialization
            "int a{5}; int b = *(&a);",  # scalar-looking pointer operation
            "int a{5}; int *p=&a;",
            "int a{5}; int b=++a;",  # side effect
            "int a{5}; int b=(a=7);",  # embedded assignment
            "int a{2147483647}; a=a+1;",  # signed overflow
            "int a{50000}; int b=a*a;",  # multiplication overflow
            "int a{1}; int b=a/0;",
            "int a{1}; int b=a%0;",
            "double a{1.5};", "bool a{true};", "static int a{1};",
            "int a{1}; while(a) a=0;", "int a{1}; if(a) a=0;",
            "int a{1}; std::cout << a << a;",  # multiple evaluated operands
            "#define VALUE 1\nint a{VALUE};",
            "int __course_checkpoint{5};",
            "int a,b;", "int a{1}; int b{2}; int c{3}; int d{4};",
            "int a{1}; } int outside(){return 0;} int other(){",  # escaped wrapper
        ]
        with patch.object(tracing, "_runtime_verify") as execute:
            for source in sources:
                with self.subTest(source=source), self.assertRaises(tracing.Unsupported):
                    tracing.trace(source)
            execute.assert_not_called()

    def test_cpp_negative_division_and_remainder(self):
        timeline = tracing.trace("int a{-7}; int b=a/3; int c=a%3;", runtime=False)
        self.assertEqual(timeline.steps[-1].values, (-7, -2, -1))


@unittest.skipUnless(CLANG and GDB, "Clang and Python-enabled GDB are required")
class RuntimeTraceTests(unittest.TestCase):
    def test_real_frame_values_and_relative_addresses(self):
        timeline = tracing.trace("int a{5}; int b{a + 6}; a = 7; std::cout << b << std::endl;")
        values = dict(zip((v.name for v in timeline.variables), timeline.steps[-1].values))
        self.assertEqual(values, {"a": 7, "b": 11})
        self.assertEqual(timeline.steps[-1].stdout, "11\n")
        self.assertEqual(min(v.address for v in timeline.variables), 64)
        self.assertTrue(all(v.size == 4 for v in timeline.variables))
        self.assertEqual([v.address for v in timeline.variables], sorted(v.address for v in timeline.variables))
        self.assertEqual(len({v.address for v in timeline.variables}), 2)
        # Public trace artifacts contain no ASLR addresses or runtime directory paths.
        self.assertNotIn("/tmp/", str(asdict(timeline)))

    def test_failed_swap_does_not_preserve_lost_old_value(self):
        timeline = tracing.trace("int a{1}; int b{2}; a=b; b=a;")
        self.assertEqual(timeline.steps[-1].values, (2, 2))
        writes = [step for step in timeline.steps if step.write]
        self.assertEqual([step.transfer for step in writes], [1, 2, 2, 2])

    def test_const_auto_empty_initialization_and_multiline_output(self):
        for source, output in [
            ("const int a=5; auto b=a; b=6; std::cout << a << std::endl; std::cout << b << std::endl;", "5\n6\n"),
            ("int a{}; a=int{}; int b=int{}; std::cout << a << std::endl; std::cout << b << std::endl;", "0\n0\n"),
            ("int a; a=5; std::cout << a;", "5"),
        ]:
            with self.subTest(source=source):
                self.assertEqual(tracing.trace(source).steps[-1].stdout, output)

    def test_static_prediction_mismatch_is_fatal(self):
        original = tracing._expression
        def wrong_result(node, initialized, operations):
            value = original(node, initialized, operations)
            return value + 1
        with patch.object(tracing, "_expression", side_effect=wrong_result):
            with self.assertRaisesRegex(tracing.Unsupported, "runtime verification failed"):
                tracing.trace("int a{5};")


if __name__ == "__main__":
    unittest.main()
