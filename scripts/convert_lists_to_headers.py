import re
import sys
from pathlib import Path


def convert_lists_to_headers(text: str) -> str:
    lines = text.split('\n')
    result = []
    counter = 0
    i = 0

    while i < len(lines):
        line = lines[i]

        # Match a list item: optional leading spaces, then 1+ digits, then . or )
        # Capture the rest of the line after the number+punctuation
        m = re.match(r'^(\d+)[.)]\s*(.*)', line)
        if m:
            counter += 1
            rest = m.group(2).strip()
            if not rest:
                result.append(f'### {counter}.')
            elif rest.startswith('```'):
                result.append(f'### {counter}.')
                result.append(rest)
            else:
                result.append(f'### {counter}. {rest}')
        else:
            result.append(line)

        i += 1

    return '\n'.join(result)


def process_file(path: Path) -> None:
    original = path.read_text(encoding='utf-8')
    converted = convert_lists_to_headers(original)
    out_path = Path(path.name)
    out_path.write_text(converted, encoding='utf-8')
    print(f'Written: {out_path}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python convert_lists_to_headers.py <file1.md> [file2.md ...]')
        sys.exit(1)
    for arg in sys.argv[1:]:
        process_file(Path(arg))
