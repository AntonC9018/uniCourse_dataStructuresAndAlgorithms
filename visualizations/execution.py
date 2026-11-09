"""Run a whitelisted statement list under GDB and observe main's frame after every statement.

The program calls `__course_checkpoint(i, …)` after statement `i`; a GDB breakpoint there reads
the requested variables from main's frame. Observations are raw (real addresses and stored
bits); the tracer interprets and verifies them. Nothing here decides what is supported.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from toolchain import Unsupported, run, tool


@dataclass(frozen=True)
class Cell:
    """One variable as GDB saw it: its real address, size, whether it is a pointer, its bits."""
    address: int
    size: int
    pointer: bool
    value: int | None
    object_address: int | None = None
    object_size: int | None = None


@dataclass(frozen=True)
class Execution:
    checkpoints: list[dict[str, Cell]]
    stdout: str


_PROGRAM = """#include <iostream>
#include <cstdint>
using namespace std;
__attribute__((noinline)) void __course_checkpoint(int position, ...) {
 asm volatile("" : : : "memory");
}
int main() {
"""

# Runs inside GDB. `expected[i]` lists the variables in scope after statement i and whether
# their value is defined; undefined (uninitialized) values are never read.
_SCRIPT = '''import gdb, json, shlex
expected, output, report = json.loads(EXPECTED), OUTPUT, REPORT
records, failures, exits = [], [], []
class Checkpoint(gdb.Breakpoint):
    def stop(self):
        try:
            current = gdb.newest_frame()
            position = int(current.read_var("position"))
            frame = current.older()
            row = {}
            for name, defined in expected[position]:
                owner, _, member = name.partition('.')
                value = frame.read_var(owner)
                object_address, object_size = int(value.address), int(value.type.sizeof)
                if member:
                    value = value[member]
                kind = value.type.strip_typedefs().code
                if value.address is None or kind not in (gdb.TYPE_CODE_INT, gdb.TYPE_CODE_PTR):
                    raise RuntimeError("unsupported storage for " + name)
                row[name] = {"address": int(value.address), "size": int(value.type.sizeof),
                             "pointer": kind == gdb.TYPE_CODE_PTR,
                             "value": int(value) if defined else None}
                if member:
                    row[name].update(object_address=object_address, object_size=object_size)
            records.append({"position": position, "variables": row})
        except Exception as error:
            failures.append(str(error))
        return False
Checkpoint("__course_checkpoint", internal=True)
gdb.events.exited.connect(lambda event: exits.append(getattr(event, "exit_code", None)))
gdb.execute("set pagination off")
gdb.execute("set confirm off")
gdb.execute("run > " + shlex.quote(output))
with open(report, "w") as handle:
    json.dump({"records": records, "failures": failures, "exits": exits}, handle)
'''


def execute(statements: list[str], expected: list[list[tuple[str, bool]]],
            directory: Path) -> Execution:
    """Compile `statements` as main's body at -O0 and observe every checkpoint under GDB."""
    body = []
    for index, (statement, scope) in enumerate(zip(statements, expected)):
        body.append(statement)
        body.append(f"__course_checkpoint({', '.join([str(index)] + ['&' + name for name, _ in scope])});")
    path, binary = directory / "runtime.cpp", directory / "runtime"
    path.write_text(_PROGRAM + "\n".join(body) + "\n}\n")
    compilation = run([tool("CLANGXX", "clang++"), "-std=c++20", "-g", "-O0",
                       "-fno-omit-frame-pointer", str(path), "-o", str(binary)])
    if compilation.returncode:
        raise Unsupported("whitelisted runtime program did not compile")
    output, report, script = directory / "stdout.txt", directory / "report.json", directory / "verify.py"
    script.write_text(_SCRIPT.replace("EXPECTED", repr(json.dumps(expected)))
                      .replace("OUTPUT", repr(str(output))).replace("REPORT", repr(str(report))))
    result = run([tool("GDB", "gdb"), "--batch", "-nx", "--quiet", "-ex",
                  "set auto-load safe-path /nonexistent", "-x", str(script), str(binary)])
    if result.returncode or not report.is_file():
        raise Unsupported("GDB could not collect the runtime trace")
    observed = json.loads(report.read_text())
    records = observed["records"]
    if (observed["failures"] or observed["exits"] != [0]
            or [row["position"] for row in records] != list(range(len(expected)))):
        reason = "; ".join(observed["failures"]) or "missing checkpoints or abnormal program exit"
        raise Unsupported("runtime verification failed: " + reason)
    checkpoints = [{name: Cell(**cell) for name, cell in row["variables"].items()} for row in records]
    return Execution(checkpoints, output.read_text())
