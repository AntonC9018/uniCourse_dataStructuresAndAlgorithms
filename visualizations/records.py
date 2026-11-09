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


def canonical_type(node: dict) -> str:
    """The snippet's own resolution of a field type, after aliases visible in its scope."""
    qualified = node.get('type', {})
    return qualified.get('desugaredQualType', qualified.get('qualType', ''))


# Static layouts accept these spellings only when they resolve to a builtin integer type:
# a snippet may shadow `uint8_t` with an alias or a struct of the same name.
LAYOUT_SPELLINGS = ('uint8_t', 'int8_t', 'int', 'size_t', 'uint64_t',
                    'std::uint8_t', 'std::int8_t', 'std::size_t', 'std::uint64_t')
BUILTIN_INTEGERS = ('signed char', 'unsigned char', 'int', 'unsigned long', 'unsigned long long')


def _pointer(node: dict) -> bool:
    return canonical_type(node).endswith('*')


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
            qualified, canonical = type_spelling(child), canonical_type(child)
            allowed = qualified == 'int' or bool(re.fullmatch(r'int \*+', qualified))
            allowed |= any(qualified == record + ' *' for record in definitions)
            if layout_only:
                allowed = qualified in LAYOUT_SPELLINGS and canonical in BUILTIN_INTEGERS
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
    records, canonicals = {}, {}
    for block in result.stdout.split('*** Dumping AST Record Layout'):
        header = re.search(r'^\s*0 \| struct (\w+)\s*$', block, re.MULTILINE)
        if not header or header[1] not in definitions:
            continue
        name = header[1]
        sizes = re.search(r'\[sizeof=(\d+), dsize=\d+, align=(\d+),', block)
        # Direct members only: a nested record's own members are indented further.
        rows = re.findall(r'^\s*(\d+) \|   (\S.*?) (\w+)\s*$', block, re.MULTILINE)
        nodes = [c for c in definitions[name]['inner'] if c.get('kind') == 'FieldDecl']
        if not sizes or [member for _, _, member in rows] != [c['name'] for c in nodes]:
            raise Unsupported(f'Clang returned an incomplete layout for {name}')
        fields = []
        for (offset, _, member), node in zip(rows, nodes):
            fields.append({'name': member, 'offset': int(offset),
                           'kind': 'ptr' if _pointer(node) else 'int'})
            if layout_only:
                fields[-1]['type'] = type_spelling(node)
        records[name] = Record(name, int(sizes[1]), int(sizes[2]), fields)
        canonicals[name] = ['void *' if _pointer(node) else canonical_type(node) for node in nodes]
    if records.keys() != definitions.keys():
        raise Unsupported('Clang omitted a struct layout')
    # Field sizes are compiler-derived too, since the gap after a field can include padding.
    # A tiny companion translation unit evaluates sizeof for each field's canonical type:
    # builtin keywords and `void *` mean the same there as in the snippet's scope, whatever
    # the snippet's aliases shadow, and this avoids relying on the host Python ABI.
    types = sorted({canonical for fields in canonicals.values() for canonical in fields})
    probe = directory / 'sizes.cpp'
    probe.write_text(''.join(f'enum {{ __course_{i} = sizeof({value}) }};\n'
                             for i, value in enumerate(types)))
    sizes = run([tool('CLANGXX', 'clang++'), '-std=c++20', '-fsyntax-only', '-Xclang',
                 '-ast-dump=json', str(probe)])
    if sizes.returncode:
        raise Unsupported('Clang could not obtain field sizes')
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
        for item, canonical in zip(record.fields, canonicals[name]):
            item['size'] = values[f'__course_{types.index(canonical)}']
    return records
