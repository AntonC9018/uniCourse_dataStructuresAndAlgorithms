#!/usr/bin/env python3
"""Compiler-backed tracer adapter consumed by course maintenance.

`trace` prints one example's trace in the unified player format (`trace_format.py`);
`revision` versions every trace.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
TEMPLATE = 'expression-timeline'
# Everything a trace's bytes depend on, besides the toolchain.
TRACER_SOURCES = tuple(ROOT / name for name in ('generate.py', 'tracing.py', 'model.py', 'trace_format.py'))


def revision() -> str:
    """Change whenever a trace could change: tracer sources and the pinned toolchain."""
    digest = hashlib.sha256()
    for path in (*TRACER_SOURCES, ROOT.parent / 'flake.nix', ROOT.parent / 'flake.lock'):
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def applicable(timeline) -> None:
    from tracing import Unsupported
    if not timeline.variables or len(timeline.variables) > 3:
        raise Unsupported('this layout supports one to three integer variables')
    if len(timeline.source) > 6 or max(map(len, timeline.source)) > 30:
        raise Unsupported('source exceeds the approved layout: six lines, 30 columns')
    positions = sorted(variable.address for variable in timeline.variables)
    if any(right - left != 4 for left, right in zip(positions, positions[1:])):
        raise Unsupported('noncontiguous integer storage needs a separate memory-layout visualization')
    for step in timeline.steps:
        source = timeline.source[step.line]
        begin, end = timeline.expression_spans[step.line]
        prefix, suffix = source[:begin], source[end:]
        if prefix.rstrip().endswith('{') and suffix.lstrip().startswith('}'):
            prefix = prefix.rstrip()[:-1].rstrip()
            prefix += ' ' if prefix.endswith('=') else ' = '
            suffix = suffix.lstrip()[1:]
        elif source[begin:end].replace(' ', '') == '{}' and '=' not in prefix:
            prefix = prefix.rstrip() + ' = '
        if len(prefix + step.expression + suffix) > 31:
            raise Unsupported('evaluated statement exceeds the approved 31-column pane')
        if len(step.stdout.splitlines()) > 4 or any(len(line) > 21 for line in step.stdout.splitlines()):
            raise Unsupported('output exceeds the approved four-line output area')
    writes = [step for step in timeline.steps if step.write]
    reads = [step for step in timeline.steps if step.read and step.transfer is not None]
    # A single initialized cell alone needs no illustration. Empty initialization is
    # deliberately kept: its contrast with uninitialized storage is the lesson.
    empty_init = any('{}' in line.replace(' ', '') for line in timeline.source)
    assignments = [step for step in writes
                   if not timeline.source[step.line].lstrip().startswith(('int ', 'auto ', 'const '))]
    if not reads and len(writes) <= 1 and not assignments:
        raise Unsupported('a lone memory cell without a copy or state change needs no visualization')
    if len(timeline.variables) == 1 and len(writes) == 1 and not empty_init and not assignments:
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
        if args.template != TEMPLATE:
            raise Unsupported(f'unknown template {args.template!r}')
        timeline = trace(args.source.read_text(), runtime=args.operation != 'probe')
        applicable(timeline)
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
        print(json.dumps({'supported': True, 'template': TEMPLATE}))
    else:
        from trace_format import from_timeline
        print(json.dumps(from_timeline(timeline), sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
