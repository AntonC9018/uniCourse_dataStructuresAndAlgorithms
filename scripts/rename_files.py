import re
import sys
from pathlib import Path


PATTERN = re.compile(r'^(\d+)(?:_(\d+))?_(.+)$')


def parse_file(name: str):
    """Return (n1, n2, rest, suffix) or None if the file doesn't match the pattern."""
    stem = Path(name).stem
    suffix = Path(name).suffix
    m = PATTERN.match(stem)
    if not m:
        return None
    n1 = int(m.group(1))
    n2 = int(m.group(2)) if m.group(2) is not None else None
    rest = m.group(3)
    return n1, n2, rest, suffix


def sort_key(entry):
    n1, n2, *_ = entry[1]
    return (n1, n2 if n2 is not None else -1)


def main(directory: str = '.', dry: bool = False):
    d = Path(directory).resolve()

    matched = []
    for f in sorted(d.iterdir()):
        if not f.is_file():
            continue
        parsed = parse_file(f.name)
        if parsed is None:
            continue
        matched.append((f, parsed))

    if not matched:
        print('No matching files found.')
        return

    # Check for duplicates (same n1, n2)
    seen = {}
    duplicates = []
    for f, (n1, n2, rest, suffix) in matched:
        key = (n1, n2)
        if key in seen:
            duplicates.append((key, seen[key], f))
        else:
            seen[key] = f

    if duplicates:
        print('ERROR: Duplicate numbering detected — aborting, no files renamed.')
        for key, first, second in duplicates:
            n1, n2 = key
            label = f'{n1}_{n2}' if n2 is not None else str(n1)
            print(f'  [{label}]  {first.name}  <->  {second.name}')
        sys.exit(1)

    # Sort
    matched.sort(key=sort_key)

    pad = 2
    if len(matched) > 99:
        print(f'ERROR: {len(matched)} files found — zero-padding to 2 digits only supports up to 99.')
        sys.exit(1)

    mode_label = '[DRY RUN] ' if dry else ''
    print(f'{mode_label}Processing {len(matched)} file(s) in: {d}\n')

    for i, (f, (n1, n2, rest, suffix)) in enumerate(matched, start=1):
        new_name = f'{str(i).zfill(pad)}_{rest}{suffix}'
        new_path = d / new_name
        if f.name == new_name:
            print(f'  [unchanged]  {f.name}')
        elif dry:
            print(f'  {f.name}  ->  {new_name}')
        else:
            print(f'  {f.name}  ->  {new_name}')
            f.rename(new_path)

    if dry:
        print('\n(dry run — no files were renamed)')


def usage():
    print('Usage: python rename_ordered.py [--dry] [directory]')
    print()
    print('  --dry      Preview renames without making any changes')
    print('  directory  Target directory (default: current directory)')
    sys.exit(0)


if __name__ == '__main__':
    args = sys.argv[1:]

    if '--help' in args or '-h' in args:
        usage()

    dry = '--dry' in args
    args = [a for a in args if a != '--dry']

    target = args[0] if args else '.'
    main(target, dry=dry)
