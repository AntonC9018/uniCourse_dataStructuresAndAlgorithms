"""Compiler-backed, bounded integer timelines for the approved expression renderer.

Clang decides syntax/types. A small whitelist reduces only side-effect-free integer
expressions; GDB verifies every stored value and the program's output before rendering.
No unsupported statement is ever executed.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from model import Step, Timeline, Variable


class Unsupported(ValueError):
    """The snippet cannot safely be represented by this visualization category."""


MIN_INT, MAX_INT = -(2**31), 2**31 - 1
COLORS = ("#61d4c4", "#ffbd69", "#b5a0ff")
_QUOTED_OR_COMMENT = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/')


def _run(command: list[str], *, timeout: int = 30) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise Unsupported(f"tool execution failed: {exc}") from exc


def _tool(env: str, executable: str) -> str:
    selected = os.environ.get(env) or shutil.which(executable)
    if not selected:
        raise Unsupported(f"{executable} is required (set {env})")
    return selected


def _body(source: str) -> str:
    def comment(match):
        value = match.group()
        return "\n" * value.count("\n") + " " if value.startswith(("//", "/*")) else value
    source = _QUOTED_OR_COMMENT.sub(comment, source)
    for line in source.splitlines():
        if line.lstrip().startswith("#") and not re.fullmatch(r'\s*#\s*include\s*[<"][\w./]+[>"]\s*', line):
            raise Unsupported("only ordinary include directives are supported")
    source = re.sub(r'^\s*#\s*include[^\n]*', '', source, flags=re.MULTILINE).strip()
    source = re.sub(r'^using\s+namespace\s+std\s*;\s*', '', source)
    if re.search(r'\bmain\s*\(', source):
        match = re.fullmatch(r'int\s+main\s*\(\s*(?:void\s*)?\)\s*\{([\s\S]*)\}\s*', source)
        if not match:
            raise Unsupported("only a standalone parameterless main or statement fragment is supported")
        source = match.group(1).strip()
    if not source or len(source) > 10_000:
        raise Unsupported("empty or oversized snippet")
    # Keep offsets byte-equivalent to Clang and avoid unreviewed identifier/string encodings.
    if not source.isascii():
        raise Unsupported("non-ASCII source text is not supported")
    return source


def _bounds(node: dict) -> tuple[int, int]:
    try:
        first, last = node["range"]["begin"], node["range"]["end"]
        return first["offset"], last["offset"] + last["tokLen"]
    except KeyError as exc:
        raise Unsupported("macro-expanded or implicit source ranges are not supported") from exc


def _compact(source: str) -> tuple[str, list[int]]:
    """Collapse whitespace outside literals and retain a source-offset map."""
    out, mapping, index = [], [0] * (len(source) + 1), 0
    pattern = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|\s+|.', re.DOTALL)
    for match in pattern.finditer(source):
        token = match.group()
        if token.isspace():
            replacement = " " if out and out[-1] != " " else ""
        else:
            replacement = token
        for offset in range(match.start(), match.end()):
            mapping[offset] = index + (min(offset - match.start(), len(replacement)) if not token.isspace() else 0)
        out.append(replacement)
        index += len(replacement)
        mapping[match.end()] = index
    return "".join(out).rstrip(), mapping


def _main_ast(program: str, directory: Path) -> dict:
    path = directory / "source.cpp"
    path.write_text(program)
    result = _run([_tool("CLANGXX", "clang++"), "-std=c++20", "-fsyntax-only", "-fno-color-diagnostics",
                   "-Xclang", "-ast-dump=json", "-Xclang", "-ast-dump-filter=main", str(path)])
    if result.returncode:
        diagnostic = next((line for line in result.stderr.splitlines() if "error:" in line), "ill-formed C++")
        raise Unsupported(diagnostic)
    decoder, offset, selected = json.JSONDecoder(), 0, []
    try:
        while offset < len(result.stdout):
            while offset < len(result.stdout) and result.stdout[offset].isspace():
                offset += 1
            if offset == len(result.stdout):
                break
            node, offset = decoder.raw_decode(result.stdout, offset)
            if node.get("kind") == "FunctionDecl" and node.get("name") == "main":
                selected.append(node)
    except ValueError as exc:
        raise Unsupported("Clang returned invalid AST JSON") from exc
    if len(selected) != 1:
        raise Unsupported("expected one main function")
    compound = [node for node in selected[0].get("inner", []) if node.get("kind") == "CompoundStmt"]
    if len(compound) != 1:
        raise Unsupported("main has no supported body")
    if _bounds(compound[0])[1] != program.rfind("}") + 1:
        raise Unsupported("declarations outside main are unsupported")
    return compound[0]


def _integer(value: int) -> int:
    if not MIN_INT <= value <= MAX_INT:
        raise Unsupported("signed integer overflow is outside the timeline category")
    return value


def _unwrap(node: dict) -> dict:
    while node.get("kind") in {"ImplicitCastExpr", "ExprWithCleanups"}:
        if node.get("kind") == "ImplicitCastExpr" and node.get("castKind") not in {"LValueToRValue", "NoOp", "FunctionToPointerDecay", "ArrayToPointerDecay"}:
            raise Unsupported("implicit numeric conversions are outside this category")
        children = node.get("inner", [])
        if len(children) != 1:
            raise Unsupported("unsupported implicit expression")
        node = children[0]
    return node


@dataclass
class Statement:
    source: str
    expression: str
    span: tuple[int, int]
    node: dict | None
    target: str | None = None
    declaration: bool = False
    output_suffix: str | None = None


def _expression(node: dict, initialized: dict[str, int | None], operations: list) -> int:
    node = _unwrap(node)
    kind, children = node.get("kind"), node.get("inner", [])
    if node.get("type", {}).get("qualType") not in {"int", "const int"}:
        raise Unsupported("only int-valued expressions are supported")
    if kind == "IntegerLiteral":
        return _integer(int(node["value"]))
    if kind == "DeclRefExpr":
        declaration = node.get("referencedDecl", {})
        name = declaration.get("name")
        if declaration.get("kind") != "VarDecl" or name not in initialized:
            raise Unsupported("expression references an undeclared or nonlocal variable")
        value = initialized[name]
        if value is None:
            raise Unsupported(f"reading uninitialized variable {name}")
        operations.append((node, value, name))
        return value
    if kind in {"InitListExpr", "CXXFunctionalCastExpr"}:
        # int{} and {} are atoms; never display an intermediate invalid `int0`.
        if kind == "CXXFunctionalCastExpr":
            if len(children) != 1 or children[0].get("kind") != "InitListExpr" or children[0].get("inner"):
                raise Unsupported("only empty int{} functional initialization is supported")
            value = 0
        elif not children:
            value = 0
        elif len(children) == 1:
            value = _expression(children[0], initialized, operations)
        else:
            raise Unsupported("multiple initializer elements are unsupported")
        operations.append((node, value, None))
        return value
    if kind == "ParenExpr" and len(children) == 1:
        value = _expression(children[0], initialized, operations)
    elif kind == "UnaryOperator" and node.get("opcode") in {"+", "-"} and len(children) == 1:
        operand = _expression(children[0], initialized, operations)
        value = _integer(operand if node["opcode"] == "+" else -operand)
    elif kind == "BinaryOperator" and node.get("opcode") in {"+", "-", "*", "/", "%"} and len(children) == 2:
        left = _expression(children[0], initialized, operations)
        right = _expression(children[1], initialized, operations)
        operation = node["opcode"]
        if operation in {"/", "%"}:
            if right == 0 or (left == MIN_INT and right == -1):
                raise Unsupported("undefined integer division")
            quotient = (abs(left) // abs(right)) * (-1 if (left < 0) != (right < 0) else 1)
            value = quotient if operation == "/" else left - quotient * right
        else:
            value = {"+": lambda: left + right, "-": lambda: left - right, "*": lambda: left * right}[operation]()
        value = _integer(value)
    else:
        raise Unsupported(f"unsupported expression: {kind} {node.get('opcode', '')}".rstrip())
    operations.append((node, value, None))
    return value


def _cout_operands(node: dict, program: str) -> list[dict]:
    node = _unwrap(node)
    if node.get("kind") == "DeclRefExpr" and node.get("referencedDecl", {}).get("name") == "cout":
        return []
    if node.get("kind") != "CXXOperatorCallExpr" or len(node.get("inner", [])) != 3:
        raise Unsupported("only std::cout insertion calls are supported")
    callee, left, right = node["inner"]
    callee = _unwrap(callee)
    if callee.get("referencedDecl", {}).get("name") != "operator<<":
        raise Unsupported("only stream insertion calls are supported")
    return _cout_operands(left, program) + [right]


def _statement(node: dict, program: str, initialized: dict, names: list) -> Statement:
    start, end = _bounds(node)
    if end < len(program) and program[end] == ";":
        end += 1
    original = program[start:end]
    source, mapping = _compact(original)
    target, declaration, output_suffix = None, False, None
    if node["kind"] == "DeclStmt":
        children = node.get("inner", [])
        if len(children) != 1 or children[0].get("kind") != "VarDecl":
            raise Unsupported("one scalar declaration per statement is required")
        variable = children[0]
        if variable.get("type", {}).get("qualType") not in {"int", "const int"}:
            raise Unsupported("only scalar int variables fit this category")
        target, declaration = variable["name"], True
        if target.startswith("__course_") or target in names or len(names) >= 3:
            raise Unsupported("unique variable names and at most three variables are supported")
        if variable.get("storageClass") or variable.get("constexpr"):
            raise Unsupported("static and constexpr storage are outside this category")
        names.append(target)
        children = variable.get("inner", [])
        expression = children[0] if children else None
        # Nonempty declaration braces are surrounding statement context, not RHS.
        if expression and expression.get("kind") == "InitListExpr" and len(expression.get("inner", [])) == 1:
            expression = expression["inner"][0]
    elif node["kind"] == "BinaryOperator" and node.get("opcode") == "=":
        left, expression = node["inner"]
        if left.get("kind") != "DeclRefExpr":
            raise Unsupported("only direct scalar assignments are supported")
        target = left.get("referencedDecl", {}).get("name")
        if target not in initialized:
            raise Unsupported("assignment destination is not a prior local variable")
    elif node["kind"] == "CXXOperatorCallExpr":
        operands = _cout_operands(node, program)
        if not operands:
            raise Unsupported("empty output expression")
        expression = operands[0]
        output_suffix = ""
        for operand in operands[1:]:
            plain = _unwrap(operand)
            name = plain.get("referencedDecl", {}).get("name")
            if name == "endl":
                output_suffix += "\n"
            elif plain.get("kind") == "CharacterLiteral" and int(plain["value"]) in {9, 10, 32}:
                output_suffix += chr(int(plain["value"]))
            else:
                raise Unsupported("one integer output followed only by whitespace or endl is supported")
    else:
        raise Unsupported(f"unsupported statement: {node['kind']}")
    if expression is None:
        span = (len(source) - 1, len(source) - 1)
        display_expression = ""
    else:
        first, last = _bounds(expression)
        span = (mapping[first - start], mapping[last - start])
        display_expression = source[slice(*span)]
    return Statement(source, display_expression, span, expression, target, declaration, output_suffix)


def _runtime_verify(statements: list[Statement], names: list[str], expected: list[dict], stdout: str,
                    directory: Path) -> dict[str, int]:
    """Observe actual frame values/locations at post-statement checkpoints via GDB."""
    body, declared = [], []
    for index, statement in enumerate(statements):
        body.append(statement.source)
        if statement.declaration:
            declared.append(statement.target)
        pointers = ["&" + name for name in declared] + ["nullptr"] * (3 - len(declared))
        body.append(f"__course_checkpoint({index}, {', '.join(pointers)});")
    program = """#include <iostream>
#include <cstdint>
using namespace std;
__attribute__((noinline)) void __course_checkpoint(int position, const void* p0,
 const void* p1, const void* p2) {
 asm volatile("" : : "g"(p0), "g"(p1), "g"(p2) : "memory");
}
int main() {
""" + "\n".join(body) + "\n}\n"
    path, binary = directory / "runtime.cpp", directory / "runtime"
    path.write_text(program)
    compilation = _run([_tool("CLANGXX", "clang++"), "-std=c++20", "-g", "-O0",
                        "-fno-omit-frame-pointer", str(path), "-o", str(binary)])
    if compilation.returncode:
        raise Unsupported("whitelisted runtime program did not compile")
    output, report, script = directory / "stdout.txt", directory / "report.json", directory / "verify.py"
    script.write_text('''import gdb, json, shlex
expected = ''' + repr(expected) + '''
records, failures, exits = [], [], []
class Checkpoint(gdb.Breakpoint):
    def stop(self):
        try:
            current = gdb.newest_frame()
            position = int(current.read_var("position"))
            frame = current.older()
            row = {}
            for name, expected_value in expected[position].items():
                value = frame.read_var(name)
                address = value.address
                if address is None or int(value.type.sizeof) != 4:
                    raise RuntimeError("unsupported storage for " + name)
                row[name] = {"value": int(value) if expected_value is not None else None,
                             "address": int(address)}
                if expected_value is not None and int(value) != expected_value:
                    raise RuntimeError("runtime value disagrees for " + name)
            records.append({"position": position, "variables": row})
        except Exception as error:
            failures.append(str(error))
        return False
Checkpoint("__course_checkpoint", internal=True)
gdb.events.exited.connect(lambda event: exits.append(getattr(event, "exit_code", None)))
gdb.execute("set pagination off")
gdb.execute("set confirm off")
gdb.execute("run > " + shlex.quote(''' + repr(str(output)) + '''))
with open(''' + repr(str(report)) + ''', "w") as handle:
    json.dump({"records": records, "failures": failures, "exits": exits}, handle)
''')
    result = _run([_tool("GDB", "gdb"), "--batch", "-nx", "--quiet", "-ex",
                   "set auto-load safe-path /nonexistent", "-x", str(script), str(binary)])
    if result.returncode or not report.is_file():
        raise Unsupported("GDB could not collect the runtime trace")
    observed = json.loads(report.read_text())
    records = observed["records"]
    if observed["failures"] or observed["exits"] != [0] or [row["position"] for row in records] != list(range(len(expected))):
        reason = "; ".join(observed["failures"]) or "missing checkpoints or abnormal program exit"
        raise Unsupported("runtime verification failed: " + reason)
    if output.read_text() != stdout:
        raise Unsupported("runtime output disagrees with the expression trace")
    addresses = {}
    for record in records:
        for name, item in record["variables"].items():
            if name in addresses and addresses[name] != item["address"]:
                raise Unsupported("variable address changed during the trace")
            addresses[name] = item["address"]
    if set(addresses) != set(names) or len(set(addresses.values())) != len(names):
        raise Unsupported("runtime locations are not distinct scalar objects")
    first = min(addresses.values())
    return {name: 64 + address - first for name, address in addresses.items()}


def trace(source: str, *, runtime: bool = True) -> Timeline:
    """Derive a timeline automatically, rejecting every unsupported construct."""
    body = _body(source)
    program = "#include <iostream>\n#include <cstdint>\nusing namespace std;\nint main() {\n" + body + "\n}\n"
    with tempfile.TemporaryDirectory(prefix="course-expression-") as temporary:
        directory = Path(temporary)
        ast = _main_ast(program, directory)
        initialized, names, statements, steps, expected = {}, [], [], [], []
        stdout = ""
        for node in ast.get("inner", []):
            if node.get("kind") == "ReturnStmt":
                children = node.get("inner", [])
                if len(children) == 1 and children[0].get("kind") == "IntegerLiteral" and children[0].get("value") == "0" and node is ast["inner"][-1]:
                    continue
                raise Unsupported("only a final return 0 is supported")
            statement = _statement(node, program, initialized, names)
            line = len(statements)
            statements.append(statement)
            if len(statements) > 20:
                raise Unsupported("too many statements")
            # Future slots are added below after the whole declaration list is known.
            def append(expression, **kwargs):
                steps.append((dict(initialized), Step(line, expression, (), stdout=stdout,
                                                      declared=tuple(initialized), **kwargs)))
            if statement.node is None:
                initialized[statement.target] = None
                append("")
                expected.append(dict(initialized))
                continue
            operations = []
            value = _expression(statement.node, initialized, operations)
            expression = statement.expression
            append(expression)
            root_start, _ = _bounds(statement.node)
            replacements = []
            for operation, result, read in operations:
                first, last = _bounds(operation)
                first, last = first - root_start, last - root_start
                # Map AST source spans through whitespace normalization and prior replacements.
                raw_first, raw_last = _bounds(statement.node)
                _, compact_map = _compact(program[raw_first:raw_last])
                first, last = compact_map[first], compact_map[last]
                start = first + sum(len(text) - (end - begin) for begin, end, text in replacements if end <= first)
                end = last + sum(len(text) - (finish - begin) for begin, finish, text in replacements if finish <= last)
                replacement = str(result)
                updated = expression[:start] + replacement + expression[end:]
                replacements = [(a, b, text) for a, b, text in replacements if not (first <= a and b <= last)]
                replacements.append((first, last, replacement))
                replacements.sort()
                if read:
                    append(updated, read=read, transfer=result, read_span=(start, end))
                elif updated != expression:
                    append(updated)
                expression = updated
            if expression != str(value):
                # A literal's spelling (hex, separators) may differ; show its decimal value.
                append(str(value))
                expression = str(value)
            if statement.target:
                initialized[statement.target] = value
                append(expression, write=statement.target, transfer=value)
            else:
                stdout += str(value) + statement.output_suffix
                append(expression)
            expected.append(dict(initialized))
        if not names:
            raise Unsupported("a variable timeline requires at least one int variable")
        addresses = _runtime_verify(statements, names, expected, stdout, directory) if runtime else {
            name: 64 + 4 * index for index, name in enumerate(names)}
        ordered = sorted(names, key=lambda name: addresses[name])
        variables = tuple(Variable(name, addresses[name], color=COLORS[names.index(name)]) for name in ordered)
        resolved = [replace(step, values=tuple(values.get(name) for name in ordered)) for values, step in steps]
        resolved[-1] = replace(resolved[-1], hold=3.5)
        return Timeline("expression-timeline", "", tuple(item.source for item in statements),
                        variables, tuple(resolved), expression_spans=tuple(item.span for item in statements))
