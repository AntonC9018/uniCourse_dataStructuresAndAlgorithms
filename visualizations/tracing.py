"""Compiler-backed execution traces of flat `int` and pointer examples, in the unified format.

Clang decides syntax and types. A whitelist evaluates only side-effect-free expressions over
`int` and pointers to `int` (of any depth): variable reads, address-of, dereference through a
pointer variable, parentheses, braces and integer arithmetic. Each statement becomes the
reductions the lessons write out, `**pp = 7` → `**72 = 7` → `*p = 7` → `*64 = 7` → `a = 7`.

GDB then runs the program (`execution.py`) and supplies main's frame after every statement:
the values and the layout come from it, and pointer values are mapped back to the variables
whose address they hold. A prediction that disagrees with the run rejects the snippet, and no
statement outside the whitelist is ever executed. Addresses are normalized to start near 64.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
import json
from pathlib import Path
import re
import tempfile

from execution import Execution, execute
from toolchain import Unsupported, run, tool
from trace_format import FORMAT, UNKNOWN, FormatError, scalar, validate

__all__ = ["Pointer", "Unsupported", "trace"]

MIN_INT, MAX_INT = -(2**31), 2**31 - 1
FIRST_ADDRESS = 64
INT_SIZE, POINTER_SIZE = 4, 8
MAX_STATEMENTS, MAX_VARIABLES = 20, 8
_QUOTED_OR_COMMENT = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/')
_DECLARATION = r'(?:const\s+)?(?:int|auto)(?:\s+const)?(?:\s*\*+\s*|\s+)\w+\s*'


# Values -----------------------------------------------------------------------------------

@dataclass(frozen=True)
class Pointer:
    """A pointer value: the variable whose address it holds, or None for a null pointer."""
    target: str | None = None


Value = int | Pointer


def _integer(value: int) -> int:
    if not MIN_INT <= value <= MAX_INT:
        raise Unsupported("signed integer overflow is outside the timeline category")
    return value


def _depth(node: dict) -> int:
    """How many pointer levels lie over `int`: 0 for `int`, 2 for `int **`."""
    qualified = node.get("type", {}).get("qualType", "")
    match = re.fullmatch(r"(const )?int(?: (\*+))?", qualified)
    if match and not (match.group(1) and match.group(2)):
        return len(match.group(2) or "")
    if "&" in qualified:
        raise Unsupported("references are not supported")
    if "[" in qualified:
        raise Unsupported("arrays are not supported")
    if "*" in qualified:
        raise Unsupported(f"only pointers to int are supported, not {qualified}")
    raise Unsupported(f"only int and pointer values are supported, not {qualified or 'this type'}")


# Source text ------------------------------------------------------------------------------

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
    result = run([tool("CLANGXX", "clang++"), "-std=c++20", "-fsyntax-only", "-fno-color-diagnostics",
                  "-Xclang", "-ast-dump=json", "-Xclang", "-ast-dump-filter=main", str(path)])
    if result.returncode:
        diagnostic = next((line for line in result.stderr.splitlines() if "error:" in line), "error: ill-formed C++")
        # Drop the temporary path, which differs between runs.
        raise Unsupported(diagnostic[diagnostic.index("error:"):])
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


# Evaluation -------------------------------------------------------------------------------

@dataclass(frozen=True)
class Reduction:
    """One rewrite of the pane: the text at `span` becomes a value, an address or a name.

    `read` replaces it with the value of `name`, `addr` with the address of `name`, `deref`
    with the name of the variable `name` (a pointer) points to, and `eval` with `value` (or
    `spelling`, when the value is not written as a number). `span` indexes the statement's
    original pane; inner reductions come first.
    """
    kind: str
    span: tuple[int, int]
    name: str | None = None
    value: Value | None = None
    spelling: str | None = None


class _Evaluator:
    """Evaluates one expression against the state before its statement, recording reductions."""

    def __init__(self, state: dict[str, Value | None], locate: Callable[[dict], tuple[int, int]]):
        self.state, self.locate, self.reductions = state, locate, []

    def _reduce(self, kind: str, node: dict, **details) -> None:
        self.reductions.append(Reduction(kind, self.locate(node), **details))

    def _load(self, name: str) -> Value:
        value = self.state[name]
        if value is None:
            raise Unsupported(f"reading uninitialized variable {name}")
        return value

    def variable(self, node: dict) -> str:
        """The local variable a DeclRefExpr names."""
        declaration = node.get("referencedDecl", {})
        name = declaration.get("name")
        if node.get("kind") != "DeclRefExpr" or declaration.get("kind") != "VarDecl" or name not in self.state:
            raise Unsupported("expression references an undeclared or nonlocal variable")
        return name

    def lvalue(self, node: dict, outer: dict | None = None) -> str:
        """The variable `node` designates. Parentheses around a dereference reduce with it."""
        kind, children = node.get("kind"), node.get("inner", [])
        if kind == "ParenExpr" and len(children) == 1:
            return self.lvalue(children[0], outer or node)
        if kind == "DeclRefExpr":
            return self.variable(node)
        if kind == "UnaryOperator" and node.get("opcode") == "*" and len(children) == 1:
            pointer, via = self.rvalue(children[0])
            if via is None:
                raise Unsupported("only dereferencing a pointer variable is supported, not a computed address")
            if pointer.target is None:
                raise Unsupported(f"dereferencing the null pointer {via} is undefined")
            self._reduce("deref", outer or node, name=via)
            return pointer.target
        raise Unsupported(f"unsupported assignable expression: {kind}")

    def rvalue(self, node: dict) -> tuple[Value, str | None]:
        """The value of `node`, and the variable it was read from, if it was read."""
        kind, children = node.get("kind"), node.get("inner", [])
        if kind == "ExprWithCleanups" and len(children) == 1:
            return self.rvalue(children[0])
        if kind == "ImplicitCastExpr" and len(children) == 1:
            cast = node.get("castKind")
            if cast == "LValueToRValue":
                _depth(node)
                name = self.lvalue(children[0])
                value = self._load(name)
                self._reduce("read", node, name=name, value=value)
                return value, name
            if cast == "NullToPointer" and _depth(node):
                literal = children[0]
                if literal.get("kind") == "CXXNullPtrLiteralExpr" or (
                        literal.get("kind") == "IntegerLiteral" and literal.get("value") == "0"):
                    self._reduce("eval", node, value=Pointer())
                    return Pointer(), None
            if cast == "NoOp":
                return self.rvalue(children[0])
            _reject_pointer_operator(children[0])
            raise Unsupported(f"implicit {cast} conversions are outside this category")
        depth = _depth(node)
        if kind == "IntegerLiteral":
            return _integer(int(node["value"])), None
        if kind == "InitListExpr" or kind == "CXXFunctionalCastExpr":
            return self._braces(node, depth), None
        if kind == "ParenExpr" and len(children) == 1:
            value, _ = self.rvalue(children[0])
        elif kind == "UnaryOperator" and node.get("opcode") == "&" and len(children) == 1:
            if children[0].get("kind") != "DeclRefExpr":
                raise Unsupported("only the address of a variable is supported")
            name = self.variable(children[0])
            self._reduce("addr", node, name=name)
            return Pointer(name), None
        elif kind == "UnaryOperator" and node.get("opcode") in {"+", "-"} and len(children) == 1 and not depth:
            operand = self._integer_operand(children[0])
            value = _integer(operand if node["opcode"] == "+" else -operand)
        elif kind == "BinaryOperator" and node.get("opcode") in {"+", "-", "*", "/", "%"} and len(children) == 2:
            _reject_pointer_operator(node)
            value = self._arithmetic(node["opcode"], self._integer_operand(children[0]),
                                     self._integer_operand(children[1]))
        else:
            raise Unsupported(f"unsupported expression: {kind} {node.get('opcode', '')}".rstrip())
        self._reduce("eval", node, value=value)
        return value, None

    def _integer_operand(self, node: dict) -> int:
        value, _ = self.rvalue(node)
        if not isinstance(value, int):
            raise Unsupported("pointer arithmetic and comparison are not supported")
        return value

    def _braces(self, node: dict, depth: int) -> Value:
        """`{}`, `{x}` and `int{}`; empty braces value-initialize to 0 or a null pointer."""
        children = node.get("inner", [])
        if node["kind"] == "CXXFunctionalCastExpr":
            if len(children) != 1 or children[0].get("kind") != "InitListExpr" or children[0].get("inner"):
                raise Unsupported("only empty int{} functional initialization is supported")
            value = 0
        elif len(children) > 1:
            raise Unsupported("multiple initializer elements are unsupported")
        elif children:
            value, _ = self.rvalue(children[0])
        else:
            value = Pointer() if depth else 0
        self._reduce("eval", node, value=value)
        return value

    @staticmethod
    def _arithmetic(operation: str, left: int, right: int) -> int:
        if operation in {"/", "%"}:
            if right == 0 or (left == MIN_INT and right == -1):
                raise Unsupported("undefined integer division")
            quotient = (abs(left) // abs(right)) * (-1 if (left < 0) != (right < 0) else 1)
            return _integer(quotient if operation == "/" else left - quotient * right)
        return _integer({"+": left + right, "-": left - right, "*": left * right}[operation])


def _strip_parentheses(node: dict) -> dict:
    while node.get("kind") == "ParenExpr" and len(node.get("inner", [])) == 1:
        node = node["inner"][0]
    return node


def _operand_is_pointer(node: dict) -> bool:
    return "*" in node.get("type", {}).get("qualType", "")


def _reject_pointer_operator(node: dict) -> None:
    """Pointer arithmetic and comparison need array or address-order semantics: not drawn."""
    if node.get("kind") == "BinaryOperator" and (
            _operand_is_pointer(node) or any(map(_operand_is_pointer, node.get("inner", [])))):
        raise Unsupported("pointer arithmetic and comparison are not supported")


# Statements -------------------------------------------------------------------------------

@dataclass
class Statement:
    """One statement of main: its text, what it evaluates, and its effect on memory or output.

    `source` is the statement's text and `span` its evaluated part, for the code highlight.
    `pane` is the statement in the lessons' notation (`int b{ a };` reads `int b = a`); the
    other spans index it: `expr` is the evaluated part, `result` the expression whose value is
    written or printed, and `destination` the name of the written variable once reduced.
    """
    source: str
    span: tuple[int, int] | None
    pane: str
    expr: tuple[int, int] | None = None
    result: tuple[int, int] | None = None
    value: Value | None = None
    reductions: list[Reduction] = field(default_factory=list)
    target: str | None = None
    destination: tuple[int, int] | None = None
    declared: str | None = None
    pointer: bool = False
    output_suffix: str | None = None


def _pane_parts(source: str, span: tuple[int, int]) -> tuple[str, str]:
    """The context around an evaluated span, with brace initialization read as assignment."""
    start, end = span
    prefix, suffix = source[:start], source[end:].rstrip().removesuffix(";").rstrip()
    # Empty value-initialization keeps its real `{}` and becomes an assignment of it.
    if re.fullmatch(r'\s*\{\s*\}\s*', source[start:end]) and re.fullmatch(_DECLARATION, prefix):
        prefix = prefix.rstrip() + ' = '
    if prefix.rstrip().endswith('{') and suffix.lstrip().startswith('}'):
        prefix = prefix.rstrip()[:-1].rstrip()
        prefix += ' ' if prefix.endswith('=') else ' = '
        suffix = suffix.lstrip()[1:]
    return prefix, suffix


def _cout_operands(node: dict) -> list[dict]:
    while node.get("kind") in {"ImplicitCastExpr", "ExprWithCleanups"} and len(node.get("inner", [])) == 1:
        node = node["inner"][0]
    if node.get("kind") == "DeclRefExpr" and node.get("referencedDecl", {}).get("name") == "cout":
        return []
    if node.get("kind") != "CXXOperatorCallExpr" or len(node.get("inner", [])) != 3:
        raise Unsupported("only std::cout insertion calls are supported")
    callee, left, right = node["inner"]
    while callee.get("kind") == "ImplicitCastExpr" and callee.get("inner"):
        callee = callee["inner"][0]
    if callee.get("referencedDecl", {}).get("name") != "operator<<":
        raise Unsupported("only stream insertion calls are supported")
    return _cout_operands(left) + [right]


def _is_manipulator(operand: dict) -> bool:
    """`std::endl` or a whitespace character: output that is not a value."""
    try:
        return bool(_output_suffix([operand]))
    except Unsupported:
        return False


def _output_suffix(operands: list[dict]) -> str:
    suffix = ""
    for operand in operands:
        while operand.get("kind") == "ImplicitCastExpr" and operand.get("inner"):
            operand = operand["inner"][0]
        if operand.get("referencedDecl", {}).get("name") == "endl":
            suffix += "\n"
        elif operand.get("kind") == "CharacterLiteral" and int(operand["value"]) in {9, 10, 32}:
            suffix += chr(int(operand["value"]))
        else:
            raise Unsupported("one integer output followed only by whitespace or endl is supported")
    return suffix


def _statement(node: dict, program: str, state: dict[str, Value | None]) -> Statement:
    """Analyze one statement against the state before it."""
    start, end = _bounds(node)
    if end < len(program) and program[end] == ";":
        end += 1
    source, mapping = _compact(program[start:end])
    left = declared = output_suffix = root = name_offset = None
    whole = pointer = False
    if node["kind"] == "DeclStmt":
        children = node.get("inner", [])
        if len(children) != 1 or children[0].get("kind") != "VarDecl":
            raise Unsupported("one scalar declaration per statement is required")
        variable = children[0]
        if any(child.get("kind", "").endswith("Attr") for child in variable.get("inner", [])):
            raise Unsupported("declaration attributes need a separate memory-layout visualization")
        pointer = _depth(variable) > 0
        declared = variable["name"]
        if declared.startswith("__course_") or declared in state:
            raise Unsupported("unique variable names are required")
        if variable.get("storageClass") or variable.get("constexpr"):
            raise Unsupported("static and constexpr storage are outside this category")
        name_offset = variable.get("loc", {}).get("offset")
        if name_offset is None:
            raise Unsupported("macro-expanded declarations are not supported")
        children = variable.get("inner", [])
        root = children[0] if children else None
        # Nonempty declaration braces are surrounding statement context, not the value.
        if root and root.get("kind") == "InitListExpr" and len(root.get("inner", [])) == 1:
            root = root["inner"][0]
    elif node["kind"] == "BinaryOperator" and node.get("opcode") == "=":
        left, root = node["inner"]
        _depth(left)
        if left.get("kind") == "ParenExpr" and _strip_parentheses(left).get("kind") == "DeclRefExpr":
            raise Unsupported("a parenthesized variable as assignment target is not supported")
        # A plain variable on the left is context; a dereference is evaluated with the rest.
        whole = left.get("kind") != "DeclRefExpr"
    elif node["kind"] == "CXXOperatorCallExpr":
        operands = _cout_operands(node)
        if not operands:
            raise Unsupported("empty output expression")
        root, output_suffix = operands[0], _output_suffix(operands[1:])
        if _is_manipulator(root):
            raise Unsupported("output without an integer value, such as a bare std::endl, is not supported")
        if _operand_is_pointer(root):
            raise Unsupported("printing a pointer prints its real, randomized address")
    else:
        raise Unsupported(f"unsupported statement: {node['kind']}")

    if root is None:
        return Statement(source, None, source.removesuffix(";").rstrip(), target=declared,
                         declared=declared, pointer=pointer)
    first, last = (start, _bounds(node)[1]) if whole else _bounds(root)
    span = (mapping[first - start], mapping[last - start])
    prefix, suffix = _pane_parts(source, span)
    text = source[slice(*span)]

    def to_pane(offset: int) -> int:
        position = mapping[offset - start]
        # The context before the evaluated part keeps its offsets; only its tail is rewritten.
        return position if position < span[0] else position - span[0] + len(prefix)

    def locate(item: dict) -> tuple[int, int]:
        return tuple(map(to_pane, _bounds(item)))

    evaluator = _Evaluator(state, locate)
    value, _ = evaluator.rvalue(root)
    target, destination = declared, None
    if declared:
        destination = (to_pane(name_offset), to_pane(name_offset) + len(declared))
    elif left is not None:
        target, destination = evaluator.lvalue(left), locate(left)
    elif not isinstance(value, int):
        raise Unsupported("only integer output is supported")
    return Statement(source, span, prefix + text + suffix, (len(prefix), len(prefix) + len(text)),
                     locate(root), value, evaluator.reductions, target, destination, declared, pointer,
                     output_suffix)


def _after(statement: Statement, state: dict[str, Value | None]) -> dict[str, Value | None]:
    after = dict(state)
    if statement.target is not None:
        after[statement.target] = statement.value
    return after


def _analyze(source: str, directory: Path) -> list[Statement]:
    program = "#include <iostream>\n#include <cstdint>\nusing namespace std;\nint main() {\n" + source + "\n}\n"
    ast = _main_ast(program, directory)
    statements, state = [], {}
    for node in ast.get("inner", []):
        if node.get("kind") == "ReturnStmt":
            children = node.get("inner", [])
            if (len(children) == 1 and children[0].get("kind") == "IntegerLiteral"
                    and children[0].get("value") == "0" and node is ast["inner"][-1]):
                continue
            raise Unsupported("only a final return 0 is supported")
        statement = _statement(node, program, state)
        statements.append(statement)
        if len(statements) > MAX_STATEMENTS:
            raise Unsupported("too many statements")
        state = _after(statement, state)
        if len(state) > MAX_VARIABLES:
            raise Unsupported("too many variables")
    if not state:
        raise Unsupported("a variable timeline requires at least one variable")
    return statements


# Memory -----------------------------------------------------------------------------------

def _size(pointer: bool) -> int:
    return POINTER_SIZE if pointer else INT_SIZE


def _normalize(addresses: dict[str, int], sizes: dict[str, int]) -> dict[str, int]:
    """Shift real addresses so the lowest sits at 64, keeping every alignment."""
    alignment = max(sizes.values())
    lowest = min(addresses.values())
    base = lowest - lowest % alignment
    return {name: FIRST_ADDRESS + address - base for name, address in addresses.items()}


def _static_layout(names: list[str], pointers: set[str]) -> dict[str, int]:
    """Where Clang -O0 places main's locals: downwards in declaration order, each aligned to its
    size, below main's return slot. Used only when the program is not run (probing)."""
    addresses, top = {}, -8
    for name in names:
        size = _size(name in pointers)
        top = (top - size) // size * size
        addresses[name] = top
    return addresses


def _observed(execution: Execution, predicted: list[dict],
              pointers: set[str]) -> tuple[dict[str, int], list[dict[str, Value | None]]]:
    """Interpret GDB's raw frames: real addresses, and values with pointers mapped to variables."""
    addresses = {}
    for row in execution.checkpoints:
        for name, cell in row.items():
            if addresses.setdefault(name, cell.address) != cell.address:
                raise Unsupported("variable address changed during the trace")
            if cell.pointer != (name in pointers) or cell.size != _size(cell.pointer):
                raise Unsupported(f"runtime storage of {name} is not the expected int or pointer")
    if len(set(addresses.values())) != len(addresses):
        raise Unsupported("runtime locations are not distinct objects")
    owners = {address: name for name, address in addresses.items()}
    states = []
    for row, expected in zip(execution.checkpoints, predicted):
        state = {}
        for name, cell in row.items():
            if cell.value is None:
                state[name] = None
            elif not cell.pointer:
                state[name] = cell.value
            elif cell.value == 0:
                state[name] = Pointer()
            elif owners.get(cell.value) in row:
                state[name] = Pointer(owners[cell.value])
            else:
                raise Unsupported(f"runtime value of {name} is not the address of a variable")
        if state != expected:
            different = sorted(name for name in state if state[name] != expected.get(name))
            raise Unsupported("runtime verification failed: " + ", ".join(different) + " disagree")
        states.append(state)
    return addresses, states


# Rendering --------------------------------------------------------------------------------

class _Pane:
    """The pane as reductions replace parts of its original text, innermost first."""

    def __init__(self, text: str):
        self.original, self.edits = text, []  # (start, end, text) in original coordinates

    @property
    def text(self) -> str:
        parts, cursor = [], 0
        for start, end, new in self.edits:
            parts += [self.original[cursor:start], new]
            cursor = end
        return "".join(parts) + self.original[cursor:]

    def locate(self, start: int, end: int) -> list[int]:
        """Where the original `[start, end)` lies in the current text."""
        def shift(at):
            return at + sum(len(new) - (finish - begin) for begin, finish, new in self.edits if finish <= at)
        return [shift(start), shift(end)]

    def read(self, start: int, end: int) -> str:
        """The current text of the original `[start, end)`."""
        first, last = self.locate(start, end)
        return self.text[first:last]

    def replace(self, start: int, end: int, new: str) -> list[int]:
        """Replace the original `[start, end)`; returns the span it covered in the old text."""
        span = self.locate(start, end)
        self.edits = sorted([edit for edit in self.edits if not (start <= edit[0] and edit[1] <= end)]
                            + [(start, end, new)])
        return span


class _Renderer:
    """Turns analyzed statements and their (observed) states into unified trace steps."""

    def __init__(self, addresses: dict[str, int]):
        self.addresses = addresses
        self.order = sorted(addresses, key=addresses.get)
        self.steps, self.stdout = [], ""

    def show(self, value: Value) -> str:
        """A value as the pane writes it: a number, an address, or 0 for a null pointer."""
        return str(self.stored(value))

    def stored(self, value: Value) -> int:
        if isinstance(value, Pointer):
            return self.addresses[value.target] if value.target else 0
        return value

    def add(self, line: int, pane: _Pane, expr, state: dict, op=None, hold: float = 1.0) -> None:
        values = {name: None if name not in state else UNKNOWN if state[name] is None
                  else self.stored(state[name]) for name in self.order}
        targets = {name: value.target for name, value in state.items()
                   if isinstance(value, Pointer) and value.target}
        step = {"line": line, "pane": pane.text, "op": op, "stdout": self.stdout, "hold": hold,
                "values": values, "targets": targets}
        if expr:
            step["expr"] = pane.locate(*expr)
        self.steps.append(step)

    def statement(self, line: int, statement: Statement, before: dict, after: dict) -> None:
        pane, expr = _Pane(statement.pane), statement.expr
        writes = statement.target is not None and statement.result is not None
        self.add(line, pane, expr, before if writes else after)
        for reduction in statement.reductions:
            if reduction.kind == "read":
                text = self.show(before[reduction.name])
                op = {"kind": "read", "name": reduction.name, "value": text}
            elif reduction.kind == "addr":
                text = str(self.addresses[reduction.name])
                op = {"kind": "addr", "name": reduction.name, "value": text}
            elif reduction.kind == "deref":
                # The target is where the pointer's observed value points.
                text = before[reduction.name].target
                op = {"kind": "deref", "target": text, "via": reduction.name}
            else:
                text = reduction.spelling or self.show(reduction.value)
                op = {"kind": "eval", "value": text}
            if pane.read(*reduction.span) != text:
                op["span"] = pane.replace(*reduction.span, text)
                self.add(line, pane, expr, before, op)
        if statement.result is None:
            return
        # A literal spelled otherwise (`0x10`, `1'000`) settles on its decimal value.
        if isinstance(statement.value, int) and pane.read(*statement.result) != str(statement.value):
            op = {"kind": "eval", "value": str(statement.value),
                  "span": pane.replace(*statement.result, str(statement.value))}
            self.add(line, pane, expr, before, op)
        span, text = pane.locate(*statement.result), pane.read(*statement.result)
        if statement.output_suffix is not None:
            self.stdout += text + statement.output_suffix
            self.add(line, pane, expr, after, {"kind": "print", "value": text, "span": span}, 1.2)
            return
        name, old = statement.target, before.get(statement.target)
        op = {"kind": "write", "name": name, "value": text, "span": span,
              "destination": pane.locate(*statement.destination)}
        # Redirecting a pointer holds longer, so the moved arc registers.
        redirected = isinstance(old, Pointer) and old.target and old != after[name]
        self.add(line, pane, expr, after, op, 1.6 if redirected else 1.2)


def trace(source: str, *, runtime: bool = True) -> dict:
    """Trace a snippet into a validated unified-format trace, rejecting unsupported constructs.

    With `runtime=False` (probing) nothing is executed: values are the predicted ones and the
    layout is Clang's usual -O0 layout.
    """
    body = _body(source)
    with tempfile.TemporaryDirectory(prefix="course-expression-") as temporary:
        directory = Path(temporary)
        statements = _analyze(body, directory)
        predicted, state = [], {}
        for statement in statements:
            state = _after(statement, state)
            predicted.append(state)
        names = [statement.declared for statement in statements if statement.declared]
        pointers = {statement.declared for statement in statements if statement.pointer}
        if runtime:
            scopes = [[(name, value is not None) for name, value in row.items()] for row in predicted]
            execution = execute([statement.source for statement in statements], scopes, directory)
            addresses, states = _observed(execution, predicted, pointers)
        else:
            addresses, states = _static_layout(names, pointers), predicted
    addresses = _normalize(addresses, {name: _size(name in pointers) for name in names})
    renderer, previous = _Renderer(addresses), {}
    for line, (statement, after) in enumerate(zip(statements, states)):
        renderer.statement(line, statement, previous, after)
        previous = after
    if runtime and renderer.stdout != execution.stdout:
        raise Unsupported("runtime output disagrees with the expression trace")
    renderer.steps[-1]["hold"] = 3
    variables = [scalar(name, addresses[name], _size(name in pointers), "ptr" if name in pointers else "int",
                        names.index(name)) for name in renderer.order]
    result = {"format": FORMAT, "source": [statement.source for statement in statements],
              "spans": [list(statement.span) if statement.span else None for statement in statements],
              "variables": variables, "steps": renderer.steps}
    try:
        validate(result)
    except FormatError as exc:
        # A tracer defect must still fail closed, never publish a malformed trace.
        raise Unsupported(f"the tracer produced an invalid trace: {exc}") from exc
    return result
