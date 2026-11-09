"""Whitelisted aggregate definitions and byte layouts supplied by Clang."""
from dataclasses import dataclass
from pathlib import Path
import json
import re

from toolchain import Unsupported, run, tool


@dataclass(frozen=True)
class Record:
    name: str
    size: int
    alignment: int
    fields: list[dict]


def type_spelling(node: dict) -> str:
    """Normalize elaborated struct names without discarding pointer or cv qualifiers."""
    qualified = node.get('type', {}).get('qualType', '')
    return re.sub(r'^(const )?struct ', r'\1', qualified)


def type_name(node: dict) -> str:
    return type_spelling(node).removeprefix('const ')


def layouts(ast: dict, directory: Path, *, layout_only: bool = False) -> dict[str, Record]:
    """Validate definitions before requesting layouts; never execute record methods."""
    definitions = {}
    for statement in ast.get('inner', []):
        for node in statement.get('inner', []) if statement.get('kind') == 'DeclStmt' else []:
            if node.get('kind') == 'CXXRecordDecl' and node.get('completeDefinition'):
                name = node.get('name')
                if not name or name in definitions:
                    raise Unsupported('structs require unique names')
                definitions[name] = node
    if not definitions:
        return {}
    for name, node in definitions.items():
        if node.get('tagUsed') != 'struct' or node.get('bases'):
            raise Unsupported('only plain aggregate structs without inheritance are supported')
        fields = []
        for child in node.get('inner', []):
            if child.get('isImplicit'):
                continue
            if child.get('kind') != 'FieldDecl':
                raise Unsupported(f'struct {name}: methods, attributes and nested types are unsupported')
            qualified = type_spelling(child)
            allowed = qualified == 'int' or bool(re.fullmatch(r'int \*+', qualified))
            allowed |= any(qualified == record + ' *' for record in definitions)
            if layout_only:
                allowed = qualified in ('uint8_t', 'int8_t', 'int', 'size_t', 'uint64_t',
                                        'std::uint8_t', 'std::int8_t', 'std::size_t', 'std::uint64_t')
                allowed |= bool(re.fullmatch(r'(?:const )?[\w:]+ \*+', qualified))
            if not allowed:
                raise Unsupported(f'struct {name}.{child.get("name")}: unsupported field type {qualified}')
            if child.get('isBitfield') or child.get('inner') or not child.get('name'):
                raise Unsupported(f'struct {name}: bitfields, attributes and default initializers are unsupported')
            fields.append(child)
        if not fields:
            raise Unsupported('empty structs are unsupported')
    result = run([tool('CLANGXX', 'clang++'), '-std=c++20', '-fsyntax-only', '-Xclang',
                  '-fdump-record-layouts-complete', str(directory / 'source.cpp')])
    if result.returncode:
        raise Unsupported('Clang could not obtain struct layouts')
    records = {}
    for block in result.stdout.split('*** Dumping AST Record Layout'):
        header = re.search(r'^\s*0 \| struct (\w+)\s*$', block, re.MULTILINE)
        if not header or header[1] not in definitions:
            continue
        name = header[1]
        sizes = re.search(r'\[sizeof=(\d+), dsize=\d+, align=(\d+),', block)
        rows = re.findall(r'^\s*(\d+) \|   (.+?) (\w+)\s*$', block, re.MULTILINE)
        fields = []
        for offset, qualified, member in rows:
            # Field sizes are compiler-derived too: the next pass uses sizeof, not offsets
            # (the gap after a field can include padding).
            fields.append({'name': member, 'offset': int(offset),
                           'kind': 'ptr' if '*' in qualified else 'int'})
            if layout_only:
                node = next(c for c in definitions[name]['inner']
                            if c.get('kind') == 'FieldDecl' and c['name'] == member)
                fields[-1]['type'] = type_spelling(node)
        if not sizes or [f['name'] for f in fields] != [
                c['name'] for c in definitions[name]['inner'] if c.get('kind') == 'FieldDecl']:
            raise Unsupported(f'Clang returned an incomplete layout for {name}')
        records[name] = Record(name, int(sizes[1]), int(sizes[2]), fields)
    if records.keys() != definitions.keys():
        raise Unsupported('Clang omitted a struct layout')
    # AST constant evaluation supplies sizeof for each allowed field type. Dumping a tiny
    # companion translation unit avoids relying on the host Python ABI.
    probe = directory / 'sizes.cpp'
    types = {'int': 'int', 'ptr': 'int*'}
    if layout_only:
        types.update({f'{name}_{i}': ('void*' if item['kind'] == 'ptr' else item['type'])
                      for name, record in records.items() for i, item in enumerate(record.fields)})
    probe.write_text('#include <cstdint>\n#include <cstddef>\nusing namespace std;\n'
                     + ''.join(f'enum {{ __course_{key} = sizeof({value}) }};\n'
                               for key, value in types.items()))
    sizes = run([tool('CLANGXX', 'clang++'), '-std=c++20', '-fsyntax-only', '-Xclang',
                 '-ast-dump=json', str(probe)])
    tree = json.loads(sizes.stdout)
    values = {}
    def walk(node):
        if node.get('kind') == 'EnumConstantDecl':
            def constant(item):
                if item.get('kind') == 'ConstantExpr':
                    return int(item['value'])
                return constant(item['inner'][0])
            values[node['name']] = constant(node)
        for child in node.get('inner', []):
            walk(child)
    walk(tree)
    for name, record in records.items():
        for i, item in enumerate(record.fields):
            key = f'{name}_{i}' if layout_only else item['kind']
            item['size'] = values['__course_' + key]
    return records
