"""Behavioral coverage for compiler-backed traces and fail-closed eligibility."""
import json
import os
from pathlib import Path
import shutil
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from execution import Cell, Execution  # noqa: E402
import tracing  # noqa: E402
from tracing import Pointer, Unsupported  # noqa: E402

CLANG = os.environ.get("CLANGXX") or shutil.which("clang++")
GDB = os.environ.get("GDB") or shutil.which("gdb")

DOUBLE_POINTER = """int a = 5;
int b = 6;
int* p = &a;
int** pp = &p;
**pp = 7;
*pp = &b;
**pp = 8;
std::cout << a << std::endl;
std::cout << *p << std::endl;
"""


def panes(trace, line):
    return [step["pane"] for step in trace["steps"] if step["line"] == line]


def ops(trace, line):
    return [step["op"] for step in trace["steps"] if step["line"] == line and step["op"]]


def final(trace, key="values"):
    return trace["steps"][-1][key]


def addresses(trace):
    return {variable["name"]: variable["address"] for variable in trace["variables"]}


@unittest.skipUnless(CLANG, "Clang is required for AST integration tests")
class StaticIntegerTraceTests(unittest.TestCase):
    def trace(self, source):
        return tracing.trace(source, runtime=False)

    def test_expression_and_cumulative_output(self):
        trace = self.trace("int a = 5; int b = a + 6; a = 7; std::cout << b << std::endl;")
        self.assertEqual(panes(trace, 1), ["int b = a + 6", "int b = 5 + 6", "int b = 11", "int b = 11"])
        self.assertEqual([op["kind"] for op in ops(trace, 1)], ["read", "eval", "write"])
        self.assertEqual(ops(trace, 1)[1], {"kind": "eval", "value": "11", "span": [8, 13]})
        self.assertEqual(ops(trace, 1)[2]["destination"], [4, 5])
        self.assertEqual(final(trace), {"a": 7, "b": 11})
        self.assertEqual(final(trace, "stdout"), "11\n")
        self.assertEqual(trace["spans"], [[8, 9], [8, 13], [4, 5], [13, 14]])

    def test_precedence_parentheses_and_repeated_reads(self):
        trace = self.trace("int c{12}; int o{3}; int r = (c + o) * c;")
        self.assertEqual(panes(trace, 2), ["int r = (c + o) * c", "int r = (12 + o) * c",
                                           "int r = (12 + 3) * c", "int r = (15) * c", "int r = 15 * c",
                                           "int r = 15 * 12", "int r = 180", "int r = 180"])
        self.assertEqual(sum(op.get("name") == "c" for op in ops(trace, 2) if op["kind"] == "read"), 2)

    def test_empty_braces_and_typed_value_initialization(self):
        trace = self.trace("int a{}; a = int{}; int b = int{};")
        self.assertEqual(panes(trace, 0), ["int a = {}", "int a = 0", "int a = 0"])
        self.assertEqual(ops(trace, 0)[0], {"kind": "eval", "value": "0", "span": [8, 10]})
        self.assertEqual(trace["spans"][0], [5, 7])
        self.assertNotIn("int0", json.dumps(trace))
        self.assertEqual(final(trace), {"a": 0, "b": 0})

    def test_literal_spelling_settles_on_its_value(self):
        trace = self.trace("int a{0x10};")
        self.assertEqual(panes(trace, 0), ["int a = 0x10", "int a = 16", "int a = 16"])

    def test_whitespace_comments_and_full_main(self):
        trace = self.trace("""#include <iostream>
int main() {
 // Русский комментарий is removed, not executed or displayed.
 int a{ 7 };
 int b = (\n a + 2\n );
 std::cout << b << '\\n';
 return 0;
}
""")
        self.assertEqual(trace["source"], ["int a{ 7 };", "int b = ( a + 2 );", "std::cout << b << '\\n';"])
        self.assertEqual(final(trace), {"a": 7, "b": 9})
        self.assertEqual(final(trace, "stdout"), "9\n")

    def test_output_context_survives_later_statements(self):
        trace = self.trace("int a{1}; std::cout << a << std::endl; a=2; std::cout << a << std::endl;")
        first = next(i for i, step in enumerate(trace["steps"]) if step["stdout"])
        self.assertTrue(all(step["stdout"].startswith("1\n") for step in trace["steps"][first:]))
        self.assertEqual(final(trace, "stdout"), "1\n2\n")

    def test_const_and_auto_copy_are_scalar_values(self):
        trace = self.trace("const int a{5}; auto b=a; b=6; std::cout << a;")
        self.assertEqual(final(trace), {"a": 5, "b": 6})
        self.assertEqual(final(trace, "stdout"), "5")

    def test_uninitialized_storage_is_distinct_from_unallocated(self):
        trace = self.trace("int a; a = 2 * 3 + 1; int b;")
        self.assertEqual(trace["steps"][0]["values"], {"a": "?", "b": None})
        self.assertIsNone(trace["spans"][0])
        self.assertEqual(panes(trace, 1), ["a = 2 * 3 + 1", "a = 6 + 1", "a = 7", "a = 7"])
        self.assertEqual(final(trace), {"a": 7, "b": "?"})

    def test_cpp_negative_division_and_remainder(self):
        trace = self.trace("int a{-7}; int b=a/3; int c=a%3;")
        self.assertEqual(final(trace), {"a": -7, "b": -2, "c": -1})

    def test_cells_are_ordered_by_address(self):
        trace = self.trace("int a{1}; int b{2}; int c{3};")
        self.assertEqual([v["name"] for v in trace["variables"]], ["c", "b", "a"])
        self.assertEqual(addresses(trace), {"c": 64, "b": 68, "a": 72})
        self.assertEqual([v["color"] for v in trace["variables"]], [2, 1, 0])


@unittest.skipUnless(CLANG, "Clang is required for AST integration tests")
class StaticPointerTraceTests(unittest.TestCase):
    def trace(self, source):
        return tracing.trace(source, runtime=False)

    def test_double_pointer_reduces_in_lesson_notation(self):
        trace = self.trace(DOUBLE_POINTER)
        at = addresses(trace)
        self.assertEqual(panes(trace, 4), ["**pp = 7", f"**{at['p']} = 7", "*p = 7", f"*{at['a']} = 7",
                                           "a = 7", "a = 7"])
        self.assertEqual([op["kind"] for op in ops(trace, 4)], ["read", "deref", "read", "deref", "write"])
        self.assertEqual(ops(trace, 4)[1], {"kind": "deref", "target": "p", "via": "pp", "span": [1, 4]})
        self.assertEqual(ops(trace, 4)[3], {"kind": "deref", "target": "a", "via": "p", "span": [0, 3]})
        # The right side is evaluated before the left.
        self.assertEqual(panes(trace, 5), ["*pp = &b", f"*pp = {at['b']}", f"*{at['p']} = {at['b']}",
                                           f"p = {at['b']}", f"p = {at['b']}"])
        self.assertEqual(ops(trace, 5)[-1]["destination"], [0, 1])
        self.assertEqual(final(trace, "targets"), {"p": "b", "pp": "p"})
        self.assertEqual(final(trace), {"a": 7, "b": 8, "p": at["b"], "pp": at["p"]})
        self.assertEqual(final(trace, "stdout"), "7\n8\n")

    def test_address_of_takes_the_label_and_sets_the_target(self):
        trace = self.trace("int a{ 1 }; int* b{ &a }; *b = 2; std::cout << a;")
        # Clang puts b below a, aligned to 8, leaving padding above b.
        self.assertEqual(addresses(trace), {"b": 64, "a": 76})
        self.assertEqual(panes(trace, 1), ["int* b = &a", "int* b = 76", "int* b = 76"])
        self.assertEqual(ops(trace, 1)[0], {"kind": "addr", "name": "a", "value": "76", "span": [9, 11]})
        write = trace["steps"][4]
        self.assertEqual((write["op"]["kind"], write["targets"], write["values"]["b"]), ("write", {"b": "a"}, 76))
        self.assertEqual(panes(trace, 2), ["*b = 2", "*76 = 2", "a = 2", "a = 2"])
        self.assertEqual([v["kind"] for v in trace["variables"]], ["ptr", "int"])
        self.assertEqual([v["size"] for v in trace["variables"]], [8, 4])

    def test_pointer_variables_are_aligned(self):
        trace = self.trace("int a{1}; int* p{&a}; int b{2}; int* q{&b};")
        for variable in trace["variables"]:
            self.assertEqual(variable["address"] % variable["size"], 0, variable)

    def test_null_pointers_are_stored_as_zero(self):
        trace = self.trace("int* p{}; int* q = nullptr; int* r = 0; int a{1}; p = &a; q = p;")
        self.assertEqual(panes(trace, 0), ["int* p = {}", "int* p = nullptr", "int* p = nullptr"])
        self.assertEqual(panes(trace, 1), ["int* q = nullptr", "int* q = nullptr"])
        self.assertEqual(panes(trace, 2), ["int* r = 0", "int* r = 0"])
        self.assertEqual(trace["steps"][2]["values"]["p"], 0)
        self.assertEqual(trace["steps"][2]["targets"], {})
        self.assertEqual(final(trace, "targets"), {"p": "a", "q": "a"})
        self.assertEqual(final(trace)["r"], 0)

    def test_copying_a_null_pointer_reads_zero(self):
        trace = self.trace("int* p{}; int* q = p;")
        self.assertEqual(panes(trace, 1), ["int* q = p", "int* q = 0", "int* q = 0"])
        self.assertEqual(final(trace, "targets"), {})

    def test_pointer_copies_share_a_target(self):
        trace = self.trace("int a = 5; int* p = &a; int* q = p; *q = 6; std::cout << *p << std::endl;")
        at = addresses(trace)
        self.assertEqual(panes(trace, 2), ["int* q = p", f"int* q = {at['a']}", f"int* q = {at['a']}"])
        self.assertEqual(panes(trace, 4), ["std::cout << *p << std::endl", f"std::cout << *{at['a']} << std::endl",
                                           "std::cout << a << std::endl", "std::cout << 6 << std::endl",
                                           "std::cout << 6 << std::endl"])
        self.assertEqual(final(trace, "targets"), {"p": "a", "q": "a"})
        self.assertEqual(final(trace, "stdout"), "6\n")

    def test_parentheses_reduce_with_a_dereference(self):
        trace = self.trace("int a{ 5 }; int* b{ &a }; std::cout << (*b) + 7;")
        self.assertEqual(panes(trace, 2), ["std::cout << (*b) + 7", "std::cout << (*76) + 7", "std::cout << a + 7",
                                           "std::cout << 5 + 7", "std::cout << 12", "std::cout << 12"])
        self.assertEqual(ops(trace, 2)[1]["span"], [13, 18])

    def test_auto_deduces_pointers(self):
        trace = self.trace("int value{ 5 }; int* p{ &value }; auto pp{ &p }; **pp = 9;")
        self.assertEqual([v["kind"] for v in trace["variables"]], ["ptr", "ptr", "int"])
        self.assertEqual(final(trace)["value"], 9)
        self.assertEqual(panes(trace, 2)[0], "auto pp = &p")

    def test_reassigning_a_pointer_holds_longer(self):
        trace = self.trace("int a = 5; int b = 7; int* p = &a; p = &b; int* q; q = &a;")
        writes = [step for step in trace["steps"] if step["op"] and step["op"]["kind"] == "write"]
        self.assertEqual([step["hold"] for step in writes[2:]], [1.2, 1.6, 3])
        self.assertEqual(trace["steps"][-3]["values"]["q"], "?")

    def test_unsupported_and_undefined_never_execute(self):
        sources = [
            "int a; std::cout << a;",  # undefined read
            "int a=a;",  # self initialization
            "int a{5}; int b=++a;",  # side effect
            "int a{5}; int b=(a=7);",  # embedded assignment
            "int a{2147483647}; a=a+1;",  # signed overflow
            "int a{50000}; int b=a*a;",  # multiplication overflow
            "int a{1}; int b=a/0;",
            "int a{1}; int b=a%0;",
            "double a{1.5};", "bool a{true};", "static int a{1};",
            "int a{1}; while(a) a=0;", "int a{1}; if(a) a=0;",
            "int a{1}; alignas(16) int b{2}; a=b;",
            "int a{1}; std::cout << a << a;",  # multiple evaluated operands
            "#define VALUE 1\nint a{VALUE};",
            "int __course_checkpoint{5};",
            "int a,b;",
            "int a{1}; } int outside(){return 0;} int other(){",  # escaped wrapper
            "int a{1}; int b{2}; int c{3}; int d{4}; int e{5}; int f{6}; int g{7}; int h{8}; int i{9};",
        ]
        self.assert_rejected_without_running(sources)

    def test_unsupported_pointer_constructs_never_execute(self):
        cases = {
            "int a[2]{};": "arrays",
            "int a{1}; int* p{&a}; int* q = p + 1;": "pointer arithmetic",
            "int a{1}; int* p{&a}; int d = *(p + 0);": "pointer arithmetic",
            "int a{1}; int* p{&a}; int* q{&a}; int d = p - q;": "pointer arithmetic",
            "int a{1}; int* p{&a}; int d = p[0];": "ArraySubscriptExpr",
            "int a{1}; int* p{&a}; int* q{&a}; int e = p == q;": "pointer arithmetic and comparison",
            "int a{1}; int& r = a;": "references",
            "int a{1}; int* p = (int*)&a;": "CStyleCastExpr",
            "int a{1}; long* p = reinterpret_cast<long*>(&a);": "pointers to int",
            "int* p = new int{1};": "CXXNewExpr",
            "int a{1}; void* p = &a;": "pointers to int",
            "const int a{1}; const int* p = &a;": "pointers to int",
            "int a{1}; int* const p = &a;": "pointers to int",
            "int a{5}; int b = *(&a);": "pointer variable",
            "int a{5}; int* p{&a}; int* q = &*p;": "address of a variable",
            "int* p{}; *p = 1;": "null pointer p",
            "int* p; *p = 1;": "uninitialized variable p",
            "int a{5}; int* b{&a}; std::cout << b;": "randomized address",
            "int a{5}; int* b{&a}; int* c = b++;": "UnaryOperator",
            "int a{5}; int* p{&a}; *p += 1;": "CompoundAssignOperator",
            "int a{5}; int* p{&a}; std::cout << *p; std::cout << std::endl;": "bare std::endl",
            "int a; (a) = 5;": "parenthesized variable",
        }
        for source, reason in cases.items():
            with self.subTest(source=source), self.assertRaisesRegex(Unsupported, reason):
                with patch.object(tracing, "execute") as execute:
                    tracing.trace(source)
                execute.assert_not_called()

    def test_compiler_errors_name_no_temporary_path(self):
        with self.assertRaises(Unsupported) as caught:
            self.trace("int* b{ 32 };")
        self.assertRegex(str(caught.exception), r"^error: cannot initialize a variable of type 'int \*'")

    def assert_rejected_without_running(self, sources):
        with patch.object(tracing, "execute") as execute:
            for source in sources:
                with self.subTest(source=source), self.assertRaises(Unsupported):
                    tracing.trace(source)
            execute.assert_not_called()


class ObservationTests(unittest.TestCase):
    """GDB's raw frames are interpreted by address; only real variables are pointer targets."""
    PREDICTED = [{"a": 5}, {"a": 5, "p": Pointer("a")}]

    def execution(self, pointer_value, size=8):
        a, p = Cell(0x7ffc_1004, 4, False, 5), Cell(0x7ffc_0ff8, size, True, pointer_value)
        return Execution([{"a": a}, {"a": a, "p": p}], "")

    def test_pointer_values_map_back_to_variables(self):
        addresses, states = tracing._observed(self.execution(0x7ffc_1004), self.PREDICTED, {"p"})
        self.assertEqual(states, self.PREDICTED)
        self.assertEqual(tracing._normalize(addresses, {"a": 4, "p": 8}), {"a": 76, "p": 64})

    def test_a_pointer_to_anything_else_is_rejected(self):
        with self.assertRaisesRegex(Unsupported, "not the address of a variable"):
            tracing._observed(self.execution(0x7ffc_1008), self.PREDICTED, {"p"})

    def test_a_disagreeing_target_is_rejected(self):
        with self.assertRaisesRegex(Unsupported, "runtime verification failed: p"):
            tracing._observed(self.execution(0), self.PREDICTED, {"p"})

    def test_unexpected_storage_is_rejected(self):
        with self.assertRaisesRegex(Unsupported, "runtime storage of p"):
            tracing._observed(self.execution(0x7ffc_1004, size=4), self.PREDICTED, {"p"})

    def test_normalization_keeps_alignment(self):
        self.assertEqual(tracing._normalize({"a": 0x1004, "p": 0x1008}, {"a": 4, "p": 8}), {"a": 68, "p": 72})
        self.assertEqual(tracing._normalize({"a": 0x1004, "b": 0x1008}, {"a": 4, "b": 4}), {"a": 64, "b": 68})


@unittest.skipUnless(CLANG and GDB, "Clang and Python-enabled GDB are required")
class RuntimeTraceTests(unittest.TestCase):
    def test_real_frame_values_and_relative_addresses(self):
        trace = tracing.trace("int a{5}; int b{a + 6}; a = 7; std::cout << b << std::endl;")
        self.assertEqual(final(trace), {"a": 7, "b": 11})
        self.assertEqual(final(trace, "stdout"), "11\n")
        self.assertEqual(sorted(addresses(trace).values()), [64, 68])
        # Public traces contain no ASLR addresses or runtime directory paths.
        self.assertNotIn("/tmp/", json.dumps(trace))

    def test_failed_swap_does_not_preserve_lost_old_value(self):
        trace = tracing.trace("int a{1}; int b{2}; a=b; b=a;")
        self.assertEqual(final(trace), {"a": 2, "b": 2})
        writes = [step["op"]["value"] for step in trace["steps"] if step["op"] and step["op"]["kind"] == "write"]
        self.assertEqual(writes, ["1", "2", "2", "2"])

    def test_const_auto_empty_initialization_and_multiline_output(self):
        for source, output in [
            ("const int a=5; auto b=a; b=6; std::cout << a << std::endl; std::cout << b << std::endl;", "5\n6\n"),
            ("int a{}; a=int{}; int b=int{}; std::cout << a << std::endl; std::cout << b << std::endl;", "0\n0\n"),
            ("int a; a=5; std::cout << a;", "5"),
        ]:
            with self.subTest(source=source):
                self.assertEqual(final(tracing.trace(source), "stdout"), output)

    def test_double_pointer_runs_as_predicted(self):
        traced, predicted = tracing.trace(DOUBLE_POINTER), tracing.trace(DOUBLE_POINTER, runtime=False)
        self.assertEqual(traced, predicted)
        self.assertEqual(final(traced, "targets"), {"p": "b", "pp": "p"})
        self.assertTrue(all(64 <= address < 128 for address in addresses(traced).values()))

    def test_static_layout_matches_the_frame(self):
        for source in ["int a{1}; int* p{&a}; int b{2}; int** pp{&p}; int c{3};",
                       "int* p{}; int a{1}; int b{2}; int* q{&b};",
                       "int x{ 0 }; int* px{ &x }; int y{ x }; int* py{ px }; *px = 1;"]:
            with self.subTest(source=source):
                self.assertEqual(addresses(tracing.trace(source)), addresses(tracing.trace(source, runtime=False)))

    def test_traces_are_byte_identical(self):
        first, second = (json.dumps(tracing.trace(DOUBLE_POINTER), sort_keys=True) for _ in range(2))
        self.assertEqual(first, second)

    def test_static_prediction_mismatch_is_fatal(self):
        original = tracing._after

        def wrong(kind):
            def after(statement, state):
                result = original(statement, state)
                value = result.get(statement.target)
                if kind is int and isinstance(value, int):
                    result[statement.target] = value + 1
                elif kind is Pointer and isinstance(value, Pointer):
                    result[statement.target] = Pointer()  # predict null, run sets &a
                return result
            return after
        for source, kind in [("int a{5};", int), ("int a{5}; int* p{&a};", Pointer)]:
            with self.subTest(source=source), patch.object(tracing, "_after", side_effect=wrong(kind)):
                with self.assertRaisesRegex(Unsupported, "runtime verification failed"):
                    tracing.trace(source)


if __name__ == "__main__":
    unittest.main()
