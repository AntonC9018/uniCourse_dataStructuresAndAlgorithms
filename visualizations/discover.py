#!/usr/bin/env python3
"""Find eligible C++ examples and add minimal, localized, answer-only visualization tags."""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
import shutil
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'course_maintenance'))
from publishing.config import load_config
from publishing.visualization_traces import markdown_files
from publishing.visualization_tags import CPP_LANGUAGES, scan_document
from generate import applicable
from tracing import Unsupported, trace


SUMMARIES = {'en': 'Execution trace', 'ru': 'Выполнение по шагам'}


def discover(repo: Path, *, apply: bool = False) -> dict:
    if not (os.environ.get('CLANGXX') or shutil.which('clang++')):
        raise RuntimeError('Clang is required for discovery; put clang++ on PATH or set CLANGXX')
    config = load_config(repo)
    if config.visualizations is None:
        raise ValueError('configure visualizations in course-publishing.json first')
    cache, selected, skipped = {}, [], []
    for path in markdown_files(repo, config.visualizations):
        original = path.read_text()
        scanned = scan_document(original, path)
        if scanned.errors:
            raise ValueError('\n'.join(scanned.errors))
        tagged = {tag.source.start for tag in scanned.tags}
        insertions = []
        for fence in scanned.fences:
            if fence.depth or fence.language not in CPP_LANGUAGES:
                continue
            if fence.source not in cache:
                try:
                    applicable(trace(fence.source, runtime=False), fence.source)
                    cache[fence.source] = None
                except Unsupported as exc:
                    cache[fence.source] = str(exc)
            reason = cache[fence.source]
            entry = {'path': path.relative_to(repo).as_posix(), 'line': fence.line,
                     'source': fence.source}
            if reason:
                skipped.append(dict(entry, reason=reason))
                continue
            selected.append(dict(entry, already_tagged=fence.start in tagged))
            if fence.start in tagged:
                continue
            language = next((lang.code for lang in config.languages
                             if path.is_relative_to(repo / lang.root)), 'en')
            summary = SUMMARIES.get(language, SUMMARIES['en'])
            # Blank lines on both sides keep the block apart from an answer that follows.
            after = '' if original[fence.end:].startswith(('\n', '\r\n')) else '\n'
            insertions.append((fence.end, '\n<details>\n<summary>' + summary + '</summary>\n\n'
                               '<!-- <visualization> -->\n\n'
                               '<!-- </visualization> -->\n\n</details>\n' + after))
        if apply and insertions:
            for at, markup in reversed(insertions):
                original = original[:at] + markup + original[at:]
            path.write_text(original)
    return {'selected': selected, 'skipped': skipped,
            'unique_supported_sources': sum(reason is None for reason in cache.values()),
            'skip_reasons': dict(Counter(entry['reason'] for entry in skipped))}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--course-repo', type=Path, default=ROOT)
    parser.add_argument('--apply', action='store_true', help='write tags; default is a read-only inventory')
    parser.add_argument('--report', type=Path, help='write the full eligibility inventory as JSON')
    args = parser.parse_args()
    try:
        report = discover(args.course_repo.resolve(), apply=args.apply)
    except (ValueError, RuntimeError, OSError) as exc:
        print(f'error: {exc}', file=sys.stderr)
        return 1
    for entry in report['selected']:
        print(f"{entry['path']}:{entry['line']}: "
              + ('already tagged' if entry['already_tagged'] else 'eligible'))
    print(f"{len(report['selected'])} examples; {report['unique_supported_sources']} shared assets")
    if args.report:
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
