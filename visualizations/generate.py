#!/usr/bin/env python3
"""Compiler-backed tracer adapter consumed by course maintenance.

`trace` prints one example's trace in the unified player format (`trace_format.py`), run and
verified under GDB; `probe` says, without running anything, whether an example is supported;
`revision` versions every trace.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
TEMPLATE = 'expression-timeline'
# Everything a trace's bytes depend on, besides the toolchain.
TRACER_SOURCES = tuple(ROOT / name for name in
                       ('generate.py', 'tracing.py', 'execution.py', 'records.py',
                        'toolchain.py', 'trace_format.py', 'layout.py'))

# What the player draws legibly inside a lesson column.
MAX_VARIABLES, MAX_LINES, MAX_COLUMNS = 5, 10, 32
MAX_PANE, MAX_OUTPUT_LINES, MAX_OUTPUT_COLUMNS = 31, 4, 21
# The player's memory geometry (`player.js`): the row's width, the widest byte, the gap between
# variables, and the advance of a 26-unit variable name.
MEMORY_WIDTH, MAX_BYTE, VARIABLE_GAP, NAME_ADVANCE = 600, 28, 10.5, 26 * 0.602
DECLARATION = re.compile(r'\s*(?:const\s+)?(?:int|auto)\b')


def revision() -> str:
    """Change whenever a trace could change: tracer sources and the pinned toolchain."""
    digest = hashlib.sha256()
    for path in (*TRACER_SOURCES, ROOT.parent / 'flake.nix', ROOT.parent / 'flake.lock'):
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _memory_fits(variables: list[dict]) -> None:
    """Storage is drawn to scale: only alignment padding between cells, names that fit."""
    from tracing import Unsupported
    cells = sorted(variables, key=lambda variable: variable['address'])
    for lower, higher in zip(cells, cells[1:]):
        # Locals are allocated downwards, each aligned to its size, so padding sits above
        # a cell and is smaller than it.
        if not 0 <= higher['address'] - lower['address'] - lower['size'] < lower['size']:
            raise Unsupported('noncontiguous storage needs a separate memory-layout visualization')
    extent = cells[-1]['address'] + cells[-1]['size'] - cells[0]['address']
    byte = min(MAX_BYTE, (MEMORY_WIDTH - VARIABLE_GAP * (len(cells) - 1)) / extent)
    centre = [(variable['address'] - cells[0]['address'] + variable['size'] / 2) * byte + VARIABLE_GAP * i
              for i, variable in enumerate(cells)]
    for i in range(len(cells) - 1):
        room = centre[i + 1] - centre[i]
        if (len(cells[i]['name']) + len(cells[i + 1]['name'])) * NAME_ADVANCE / 2 + 8 > room:
            raise Unsupported(f"the names {cells[i]['name']} and {cells[i + 1]['name']} do not fit under their cells")


_LITERAL = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')
_COMMENT = re.compile(r'//.*')


def _spacing_survives(snippet: str) -> bool:
    """Whether the tracer's whitespace collapsing leaves every line as written.

    Indentation and line breaks are layout; a run of spaces inside a statement
    is something the example may be asking about, such as `int     *     d`.
    """
    return not any(re.search(r'\S[ \t]{2,}\S', _COMMENT.sub('', _LITERAL.sub('""', line)).strip())
                   for line in snippet.splitlines())


def applicable(trace: dict, snippet: str) -> None:
    """Reject traces the player cannot draw legibly, or that need no illustration."""
    from tracing import Unsupported
    if not _spacing_survives(snippet):
        raise Unsupported('the trace would collapse spacing inside a statement')
    variables, steps, source = trace['variables'], trace['steps'], trace['source']
    if len(variables) > MAX_VARIABLES:
        raise Unsupported(f'the memory row holds at most {MAX_VARIABLES} variables')
    if len(source) > MAX_LINES or max(map(len, source)) > MAX_COLUMNS:
        raise Unsupported(f'source exceeds the approved layout: {MAX_LINES} lines, {MAX_COLUMNS} columns')
    _memory_fits(variables)
    if max(len(step['pane']) for step in steps) > MAX_PANE:
        raise Unsupported(f'evaluated statement exceeds the approved {MAX_PANE}-column pane')
    output = steps[-1]['stdout'].splitlines()
    if len(output) > MAX_OUTPUT_LINES or any(len(line) > MAX_OUTPUT_COLUMNS for line in output):
        raise Unsupported('output exceeds the approved four-line output area')
    ops = [step['op'] for step in steps if step['op']]
    writes = [step for step in steps if step['op'] and step['op']['kind'] == 'write']
    reads = [op for op in ops if op['kind'] in ('read', 'addr', 'deref')]
    # A single initialized cell alone needs no illustration. Empty initialization is
    # deliberately kept: its contrast with uninitialized storage is the lesson.
    empty_init = any('{}' in line.replace(' ', '') for line in source)
    assignments = [step for step in writes if not DECLARATION.match(source[step['line']])]
    if not reads and len(writes) <= 1 and not assignments:
        raise Unsupported('a lone memory cell without a copy or state change needs no visualization')
    if len(variables) == 1 and len(writes) == 1 and not empty_init and not assignments:
        raise Unsupported('a lone literal-initialized cell and print need no visualization')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('probe', 'trace', 'revision'))
    parser.add_argument('--source', type=Path)
    parser.add_argument('--template', default=TEMPLATE)
    args = parser.parse_args()
    if args.operation == 'revision':
        print(revision())
        return 0
    if not args.source:
        parser.error('--source is required')
    from tracing import Unsupported, trace
    try:
        if args.template not in (TEMPLATE, 'layout'):
            raise Unsupported(f'unknown template {args.template!r}')
        if args.template == 'layout':
            from layout import trace as layout_trace
            result = layout_trace(args.source.read_text())
        else:
            snippet = args.source.read_text()
            result = trace(snippet, runtime=args.operation != 'probe')
            applicable(result, snippet)
    except Unsupported as exc:
        if args.operation == 'probe':
            print(json.dumps({'supported': False, 'reason': str(exc)}))
            return 0
        print(f'unsupported: {exc}', file=sys.stderr)
        return 1
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f'error: {exc}', file=sys.stderr)
        return 1
    if args.operation == 'probe':
        print(json.dumps({'supported': True, 'template': args.template}))
    else:
        print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
