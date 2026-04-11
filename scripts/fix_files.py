#!/usr/bin/env python3
"""
Fix markdown heading numbers to match filename and resequence H3 headings.

Usage: python fix_headings.py <file.md> [<file.md> ...]
       python fix_headings.py *.md

Filename format: XX_NAME.md  (XX = zero-padded number, e.g. 01_variables.md)

Rules applied:
  - H1 (# N. Title): the number N is replaced with the integer from XX in the filename
  - H3 (### N. Title): all H3 numbers are resequenced 1, 2, 3, ... in order of appearance
"""

import re
import sys
from pathlib import Path


def fix_file(filepath: Path) -> None:
    # --- Derive expected H1 number from filename ---
    match = re.match(r'^(\d+)_', filepath.name)
    if not match:
        print(f"SKIP  {filepath.name}  (filename does not match XX_NAME.md pattern)")
        return

    h1_number = int(match.group(1))   # e.g. "01" -> 1

    original = filepath.read_text(encoding='utf-8')
    lines = original.splitlines(keepends=True)

    h3_counter = 0
    h1_fixed = False
    changed = False
    result = []

    for line in lines:
        # --- Fix H1: "# <number>. <rest>" ---
        h1_match = re.match(r'^(#\s+)(\d+)(\.\s+.+)', line)
        if h1_match and not h1_fixed:
            old_num = int(h1_match.group(2))
            if old_num != h1_number:
                line = f"{h1_match.group(1)}{h1_number}{h1_match.group(3)}"
                print(f"  H1 : {old_num} -> {h1_number}")
                changed = True
            h1_fixed = True
            result.append(line)
            continue

        # --- Fix H3: "### <number>. <rest>" ---
        h3_match = re.match(r'^(###\s+)(\d+)(\.\s+.+)', line)
        if h3_match:
            h3_counter += 1
            old_num = int(h3_match.group(2))
            if old_num != h3_counter:
                line = f"{h3_match.group(1)}{h3_counter}{h3_match.group(3)}"
                print(f"  H3 : {old_num} -> {h3_counter}")
                changed = True
            result.append(line)
            continue

        result.append(line)

    if changed:
        filepath.write_text(''.join(result), encoding='utf-8')
        print(f"FIXED {filepath.name}  (H1={h1_number}, H3 headings={h3_counter})")
    else:
        print(f"OK    {filepath.name}  (no changes needed, H1={h1_number}, H3 headings={h3_counter})")


def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_headings.py <file.md> [<file.md> ...]")
        sys.exit(1)

    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.exists():
            print(f"ERROR {arg}: file not found")
            continue
        if path.suffix.lower() != '.md':
            print(f"SKIP  {arg}: not a .md file")
            continue
        fix_file(path)


if __name__ == '__main__':
    main()
