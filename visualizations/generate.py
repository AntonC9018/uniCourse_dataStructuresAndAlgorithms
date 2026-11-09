#!/usr/bin/env python3
"""Compiler-backed adapter consumed by course maintenance (local rendering only)."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
TEMPLATE = 'expression-timeline'


def revision() -> str:
    """Version the renderer, without storing a source hash on lesson tags."""
    digest = hashlib.sha256()
    for name in ('generate.py', 'tracing.py', 'model.py', 'layout-prototype.py',
                 'export-layout-svg.cjs', 'package-lock.json'):
        digest.update(name.encode())
        digest.update((ROOT / name).read_bytes())
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


def render(timeline, output: Path) -> None:
    """Export the settled final state as a static SVG; the interactive player replaces video."""
    page = runpy.run_path(str(ROOT / 'layout-prototype.py'))['PAGE']
    payload = asdict(timeline)
    payload['output_label'] = ''  # Generated assets are shared across lesson languages.
    html = page.replace('__TRACES__', json.dumps([payload]).replace('<', chr(92) + 'u003c'))
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='course-visualization-') as directory:
        document = Path(directory) / 'timeline.html'
        document.write_text(html)
        env = dict(os.environ, VISUALIZATION_INPUT=str(document), VISUALIZATION_OUTPUT=str(output))
        subprocess.run(['node', str(ROOT / 'export-layout-svg.cjs'), 'expression'],
                       env=env, check=True, timeout=300)
    if not output.is_file() or output.stat().st_size == 0:
        raise RuntimeError('renderer did not produce an asset')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('probe', 'trace', 'render', 'revision'))
    parser.add_argument('--source', type=Path)
    parser.add_argument('--output', type=Path)
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
    elif args.operation == 'trace':
        print(json.dumps(asdict(timeline)))
    else:
        if not args.output:
            parser.error('--output is required for render')
        render(timeline, args.output)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
