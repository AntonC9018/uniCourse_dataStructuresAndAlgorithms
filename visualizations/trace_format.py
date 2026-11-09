"""The unified trace format (version 1) shared by the tracer and the site player.

A trace lists the source lines, the objects in memory and the visible evaluation states.
`validate` checks a trace; `Builder` writes traces by hand, the way the lessons explain an
evaluation. The compiler-backed tracer (`tracing.py`) emits the format directly.
`player/README.md` documents every field.
"""
from __future__ import annotations

from dataclasses import dataclass
import re

FORMAT = 1
SCALAR_KINDS = ('int', 'ptr')
OPERATIONS = ('read', 'addr', 'deref', 'eval', 'write', 'print')
UNKNOWN = '?'
IDENTIFIER = re.compile(r'[A-Za-z_]\w*')


class FormatError(ValueError):
    """A trace does not follow the unified format."""


_WHITESPACE_SPELLINGS = {'std::endl': '\n', 'endl': '\n', "'\\n'": '\n', "'\\t'": '\t', "' '": ' '}


def whitespace_output(spelling: str) -> str | None:
    """What an output operand that is no value prints (`std::endl` a newline), else None."""
    return _WHITESPACE_SPELLINGS.get(spelling)


# Building blocks ------------------------------------------------------------------------------

def scalar(name: str, address: int, size: int = 4, kind: str = 'int', color: int = 0) -> dict:
    return {'name': name, 'address': address, 'size': size, 'kind': kind, 'color': color}


def struct(name: str, type_: str, address: int, size: int, fields: list[dict],
           color: int = 0) -> dict:
    """`size` includes any padding; `fields` come from `field()`."""
    return {'name': name, 'type': type_, 'address': address, 'size': size, 'kind': 'struct',
            'color': color, 'fields': fields}


def field(name: str, offset: int, size: int = 4, kind: str = 'int', color: int = 0) -> dict:
    return {'name': name, 'offset': offset, 'size': size, 'kind': kind, 'color': color}


def leaves(variables: list[dict]) -> dict[str, dict]:
    """Every cell that holds a value: scalars by name, struct fields as `variable.field`."""
    cells = {}
    for variable in variables:
        if variable['kind'] == 'struct':
            for item in variable['fields']:
                cells[variable['name'] + '.' + item['name']] = item
        else:
            cells[variable['name']] = variable
    return cells


def addresses(variables: list[dict]) -> dict[str, int]:
    """The address of every variable and every struct field (`variable.field`)."""
    result = {}
    for variable in variables:
        result[variable['name']] = variable['address']
        for item in variable['fields'] if variable['kind'] == 'struct' else ():
            result[variable['name'] + '.' + item['name']] = variable['address'] + item['offset']
    return result


def cells_of(variables: list[dict], name: str) -> list[str]:
    """The leaves a name covers: a struct's fields, or the leaf itself."""
    for variable in variables:
        if variable['name'] == name and variable['kind'] == 'struct':
            return [name + '.' + item['name'] for item in variable['fields']]
    return [name]


# Validation -----------------------------------------------------------------------------------

def _check(condition: bool, where: str, message: str) -> None:
    if not condition:
        raise FormatError(f'{where}: {message}')


def _keys(value, where: str, required: set[str], optional: set[str] = frozenset()) -> None:
    _check(isinstance(value, dict), where, 'expected an object')
    missing, unknown = required - value.keys(), value.keys() - required - optional
    _check(not missing, where, f'missing {sorted(missing)}')
    _check(not unknown, where, f'unknown {sorted(unknown)}')


def _natural(value, where: str, positive: bool = False) -> None:
    _check(type(value) is int and value >= (1 if positive else 0), where,
           'expected a positive integer' if positive else 'expected a non-negative integer')


def _span(value, text: str, where: str, empty: bool = False) -> tuple[int, int]:
    _check(isinstance(value, list) and len(value) == 2 and all(type(v) is int for v in value),
           where, 'expected [start, end]')
    start, end = value
    _check(0 <= start <= end <= len(text) and (empty or start < end), where,
           f'{value} is outside {text!r}')
    return start, end


def _variables(variables, where: str) -> dict[str, dict]:
    _check(isinstance(variables, list) and variables, where, 'expected a nonempty list')
    names, ranges = set(), []
    for index, variable in enumerate(variables):
        here = f'{where}[{index}]'
        struct_ = isinstance(variable, dict) and variable.get('kind') == 'struct'
        common = {'name', 'address', 'size', 'kind', 'color'}
        _keys(variable, here, common | ({'type', 'fields'} if struct_ else set()))
        _check(bool(IDENTIFIER.fullmatch(str(variable['name']))), here, 'name is not an identifier')
        _check(variable['name'] not in names, here, f'duplicate variable {variable["name"]!r}')
        names.add(variable['name'])
        _natural(variable['address'], here + '.address')
        _natural(variable['size'], here + '.size', positive=True)
        _natural(variable['color'], here + '.color')
        ranges.append((variable['address'], variable['address'] + variable['size'], variable['name']))
        if not struct_:
            _check(variable['kind'] in SCALAR_KINDS, here, f'kind must be one of {SCALAR_KINDS} or struct')
            continue
        _check(isinstance(variable['type'], str) and variable['type'], here, 'type must be a name')
        fields = variable['fields']
        _check(isinstance(fields, list) and fields, here + '.fields', 'expected a nonempty list')
        seen, end = set(), 0
        for position, item in enumerate(fields):
            spot = f'{here}.fields[{position}]'
            _keys(item, spot, {'name', 'offset', 'size', 'kind', 'color'})
            _check(bool(IDENTIFIER.fullmatch(str(item['name']))), spot, 'name is not an identifier')
            _check(item['name'] not in seen, spot, f'duplicate field {item["name"]!r}')
            seen.add(item['name'])
            _check(item['kind'] in SCALAR_KINDS, spot, f'kind must be one of {SCALAR_KINDS}')
            _natural(item['offset'], spot + '.offset')
            _natural(item['size'], spot + '.size', positive=True)
            _natural(item['color'], spot + '.color')
            _check(item['offset'] >= end, spot, 'fields must be ordered and must not overlap')
            end = item['offset'] + item['size']
        _check(end <= variable['size'], here, 'fields exceed the struct size')
    ranges.sort()
    for (_, end, left), (start, _, right) in zip(ranges, ranges[1:]):
        _check(start >= end, where, f'{left!r} and {right!r} overlap')
    return leaves(variables)


@dataclass(frozen=True)
class _Storage:
    """Lookups over validated variables: `cells` by leaf, `addresses` by variable or leaf."""
    variables: list[dict]
    cells: dict[str, dict]
    addresses: dict[str, int]

    def cells_of(self, name: str) -> list[str]:
        return cells_of(self.variables, name)


def _value(value, where: str) -> None:
    _check(value is None or value == UNKNOWN or type(value) is int, where,
           'a value is an integer, "?" (declared, unknown) or null (no storage yet)')


def _replacement(before: str, after: str, span: tuple[int, int], where: str) -> str:
    """The text that replaced `before[start:end]` in `after`; the rest must be unchanged."""
    start, end = span
    tail = len(before) - end
    _check(len(after) >= start + tail and after[:start] == before[:start]
           and after[len(after) - tail:] == before[end:], where,
           f'{after!r} is not {before!r} with {before[start:end]!r} replaced')
    replaced = after[start:len(after) - tail]
    _check(bool(replaced), where, 'the replacement is empty')
    return replaced


_LITERAL = re.compile(r'-?\d+')


def _stored(text: str, where: str) -> list:
    """The cell values an operation's text stands for: one per field for `{…}`, `nullptr` as 0."""
    braced = text.startswith('{') and text.endswith('}')
    items = [item.strip() for item in text[1:-1].split(',')] if braced else [text]
    result = []
    for item in items:
        _check(item in ('nullptr', UNKNOWN) or bool(_LITERAL.fullmatch(item)), where,
               f'{text!r} is not a value: expected an integer, nullptr, "?" or {{…}} of them')
        result.append(0 if item == 'nullptr' else item if item == UNKNOWN else int(item))
    return result


def _memory(op: dict, step: dict, previous: dict, storage: _Storage, where: str) -> None:
    """An operation's value agrees with memory: a read shows what `name` held before the step,
    a write what it holds after, and an address is where `name` is stored."""
    kind, name = op['kind'], op['name']
    if kind == 'addr':
        address = storage.addresses[name]
        _check(_stored(op['value'], where) == [address], where + '.value',
               f'the address of {name} is {address}, not {op["value"]!r}')
        return
    cells = storage.cells_of(name)
    values = (step if kind == 'write' else previous)['values']
    expected = [values[cell] for cell in cells]
    shown = str(expected[0]) if len(cells) == 1 else '{' + ', '.join(map(str, expected)) + '}'
    when = 'after the write' if kind == 'write' else 'before the read'
    _check(_stored(op['value'], where) == expected, where + '.value',
           f'{name} holds {shown} {when}, not {op["value"]!r}')


def _pointers(step: dict, storage: _Storage, where: str) -> None:
    """Targets agree with memory: only pointers have one, a pointer with a target holds its
    address, and a pointer holding a nonzero value has a target."""
    for name, target in step['targets'].items():
        _check(storage.cells.get(name, {}).get('kind') == 'ptr', f'{where}.targets.{name}',
               'only pointers have targets')
        _check(target in storage.addresses, f'{where}.targets.{name}', f'unknown variable {target!r}')
    for name, cell in storage.cells.items():
        if cell['kind'] != 'ptr':
            continue
        value, target = step['values'][name], step['targets'].get(name)
        if target is not None:
            address = storage.addresses[target]
            _check(value == address, f'{where}.targets.{name}',
                   f'{name} holds {value!r}, but {target} is at {address}')
        else:
            _check(type(value) is not int or value == 0, f'{where}.targets.{name}',
                   f'{name} holds the address {value} but points nowhere')


def _operation(op, step: dict, previous: dict, storage: _Storage, where: str) -> None:
    _check(isinstance(op, dict) and op.get('kind') in OPERATIONS, where,
           f'kind must be one of {OPERATIONS}')
    kind = op['kind']
    fields = {'read': {'name', 'value', 'span'}, 'addr': {'name', 'value', 'span'},
              'deref': {'target', 'via', 'span'}, 'eval': {'value', 'span'},
              'write': {'name', 'value', 'span', 'destination'}, 'print': {'value', 'span'}}[kind]
    _keys(op, where, fields | {'kind'})
    for key in fields & {'name', 'target', 'via', 'value'}:
        _check(isinstance(op[key], str) and op[key], f'{where}.{key}', 'expected text')
    for key in ('name', 'via'):
        if key in op:
            _check(op[key] in storage.addresses, f'{where}.{key}', f'unknown variable {op[key]!r}')
    if kind == 'deref':
        _check(op['target'] in storage.addresses, where + '.target',
               f'unknown variable {op["target"]!r}')
        _check(storage.cells.get(op['via'], {}).get('kind') == 'ptr', where + '.via', 'must be a pointer')
        pointee = previous['targets'].get(op['via'])
        _check(pointee is not None and (op['target'] == pointee
                                        or op['target'].startswith(pointee + '.')),
               where, f'{op["via"]} does not point to {op["target"]}')
    if kind in ('read', 'addr', 'deref', 'eval'):
        span = _span(op['span'], previous['pane'], where + '.span')
        replaced = _replacement(previous['pane'], step['pane'], span, where)
        expected = op['target'] if kind == 'deref' else op['value']
        _check(replaced == expected, where, f'the replacement {replaced!r} is not {expected!r}')
    else:
        _unchanged_pane(op, step, previous, where)
    if kind in ('read', 'addr', 'write'):
        _memory(op, step, previous, storage, where)


def _unchanged_pane(op: dict, step: dict, previous: dict, where: str) -> None:
    """A write or print keeps the pane; its spans cover what it stores or prints.

    Whitespace output is no value: its span covers its spelling, such as `std::endl`.
    """
    kind = op['kind']
    _check(step['pane'] == previous['pane'], where, f'a {kind} does not change the pane')
    start, end = _span(op['span'], step['pane'], where + '.span')
    covered = step['pane'][start:end]
    _check(covered == op['value'] or (kind == 'print' and whitespace_output(covered) == op['value']),
           where + '.span', 'does not cover the value')
    if kind == 'write':
        start, end = _span(op['destination'], step['pane'], where + '.destination')
        _check(step['pane'][start:end] == op['name'], where + '.destination', 'does not cover the name')
    else:
        printed = step['stdout'][len(previous['stdout']):]
        _check(printed.startswith(op['value']) and not printed[len(op['value']):].strip(),
               where, 'stdout must grow by the printed value and optional whitespace')


def _changes(step: dict, previous: dict, storage: _Storage, where: str) -> None:
    op = step['op'] or {}
    written = set(storage.cells_of(op['name'])) if op.get('kind') == 'write' else set()
    for name, value in step['values'].items():
        old = previous['values'][name]
        _check(value == old or name in written or (not op and old is None and value == UNKNOWN),
               f'{where}.values.{name}', 'only a write, or a declaration ("?"), changes a value')
    for name in set(step['targets']) | set(previous['targets']):
        _check(step['targets'].get(name) == previous['targets'].get(name) or name in written,
               f'{where}.targets.{name}', 'only a write changes where a pointer points')
    _check(step['stdout'] == previous['stdout'] or op.get('kind') == 'print',
           where + '.stdout', 'only a print changes the output')


def _layout(trace) -> None:
    _keys(trace, 'layout', {'format', 'kind', 'records'})
    _check(trace['format'] == FORMAT, 'layout.format', f'expected {FORMAT}')
    records = trace['records']
    _check(isinstance(records, list) and records, 'layout.records', 'expected nonempty list')
    names = set()
    for record in records:
        _keys(record, 'record', {'name', 'size', 'alignment', 'fields'})
        name = record['name']
        _check(isinstance(name, str) and bool(IDENTIFIER.fullmatch(name)), 'record', 'invalid name')
        _check(name not in names, 'record', 'duplicate name')
        names.add(name)
        _natural(record['size'], name + '.size', positive=True)
        _natural(record['alignment'], name + '.alignment', positive=True)
        align = record['alignment']
        _check(align in (1, 4, 8), name, 'invalid alignment')
        fields = record['fields']
        _check(isinstance(fields, list) and fields, name, 'expected nonempty fields')
        seen, end = set(), 0
        for item in fields:
            _keys(item, name, {'name', 'offset', 'size', 'kind', 'type'})
            _check(isinstance(item['name'], str) and bool(IDENTIFIER.fullmatch(item['name'])),
                   name, 'invalid field name')
            _check(item['name'] not in seen, name, 'duplicate field')
            seen.add(item['name'])
            _check(isinstance(item['type'], str) and bool(item['type']), name, 'invalid field type')
            _check(item['kind'] in SCALAR_KINDS, name, 'invalid field kind')
            _natural(item['offset'], name + '.offset')
            _natural(item['size'], name + '.size', positive=True)
            size = item['size']
            _check(size in (1, 4, 8) and (item['kind'] != 'ptr' or size == 8), name,
                   'unsupported field size')
            # Plain layouts align each scalar to its size and pad only as much as that needs.
            _check(item['offset'] == _round_up(end, size), name,
                   f'field {item["name"]} must start at offset {_round_up(end, size)}')
            end = item['offset'] + size
        widest = max(item['size'] for item in fields)
        _check(align == widest, name, f'alignment must be {widest}, the widest field')
        _check(record['size'] == _round_up(end, align), name,
               f'size must be {_round_up(end, align)}, the last field end rounded to alignment')


def _round_up(value: int, alignment: int) -> int:
    return -(-value // alignment) * alignment


def validate(trace) -> None:
    """Raise `FormatError` unless `trace` is a well-formed, self-consistent version 1 trace."""
    if isinstance(trace, dict) and trace.get('kind') == 'layout':
        _layout(trace)
        return
    _keys(trace, 'trace', {'format', 'source', 'variables', 'steps'}, {'title', 'spans'})
    _check(trace['format'] == FORMAT, 'trace.format', f'expected {FORMAT}')
    source = trace['source']
    _check(isinstance(source, list) and source and all(isinstance(line, str) for line in source),
           'trace.source', 'expected nonempty list of lines')
    if 'title' in trace:
        _check(isinstance(trace['title'], str), 'trace.title', 'expected text')
    if 'spans' in trace:
        _check(isinstance(trace['spans'], list) and len(trace['spans']) == len(source),
               'trace.spans', 'expected one entry per source line')
        for index, span in enumerate(trace['spans']):
            if span is not None:
                _span(span, source[index], f'trace.spans[{index}]')
    variables = trace['variables']
    cells = _variables(variables, 'trace.variables')
    storage = _Storage(variables, cells, addresses(variables))
    steps = trace['steps']
    _check(isinstance(steps, list) and steps, 'trace.steps', 'expected a nonempty list')
    previous = None
    for index, step in enumerate(steps):
        where = f'trace.steps[{index}]'
        _keys(step, where, {'line', 'pane', 'values', 'targets', 'stdout', 'hold', 'op'}, {'expr'})
        _check(type(step['line']) is int and 0 <= step['line'] < len(source), where + '.line',
               'not a source line')
        _check(isinstance(step['pane'], str), where + '.pane', 'expected text')
        if step.get('expr') is not None:
            _span(step['expr'], step['pane'], where + '.expr', empty=True)
        _check(isinstance(step['values'], dict) and step['values'].keys() == cells.keys(),
               where + '.values', f'expected exactly {sorted(cells)}')
        for name, value in step['values'].items():
            _value(value, f'{where}.values.{name}')
        _check(isinstance(step['targets'], dict), where + '.targets', 'expected an object')
        _pointers(step, storage, where)
        _check(isinstance(step['stdout'], str), where + '.stdout', 'expected text')
        _check(type(step['hold']) in (int, float) and step['hold'] >= 0, where + '.hold',
               'expected seconds')
        if previous is None:
            _check(step['op'] is None, where + '.op', 'the first step has no operation')
        else:
            if step['op'] is not None:
                _operation(step['op'], step, previous, storage, where + '.op')
            _changes(step, previous, storage, where)
        previous = step


# Hand-written traces --------------------------------------------------------------------------

class Builder:
    """Evaluation states in the lessons' notation: `pa->f1 = 7` → `64->f1 = 7` → `a.f1 = 7`.

    Each call appends one step. Tokens are found in the current pane by name, so a statement
    is written once and then reduced in place.
    """

    def __init__(self, source: list[str], variables: list[dict], title: str | None = None):
        self.source, self.variables, self.title = source, variables, title
        self.cells = leaves(variables)
        self.values = {name: None for name in self.cells}
        self.targets: dict[str, str] = {}
        self.steps: list[dict] = []
        self.pane, self.line, self.stdout = '', 0, ''
        self.carry = None

    def _add(self, op=None, hold=1.0):
        self.steps.append({'line': self.line, 'pane': self.pane, 'values': dict(self.values),
                           'targets': dict(self.targets), 'op': op, 'stdout': self.stdout,
                           'hold': hold})

    def _value(self, name: str) -> str:
        if name in self.values:
            return str(self.values[name])
        return '{' + ', '.join(str(self.values[cell]) for cell in cells_of(self.variables, name)) + '}'

    def _find(self, token: str) -> int:
        pattern = re.escape(token)
        if token[0].isalnum() or token[0] == '_':
            pattern = r'(?<![\w.>])' + pattern
        if token[-1].isalnum() or token[-1] == '_':
            pattern += r'(?![\w.])'
        match = re.search(pattern, self.pane)
        if not match:
            raise ValueError(f'{token!r} is not in {self.pane!r}')
        return match.start()

    def _replace(self, token: str, new: str) -> list[int]:
        start = self._find(token)
        self.pane = self.pane[:start] + new + self.pane[start + len(token):]
        return [start, start + len(token)]

    def statement(self, line: int, pane: str | None = None):
        """Copy a source line into the pane; brace initialization reads as an assignment."""
        self.line = line
        self.pane = pane or re.sub(r'(\w)\s*\{\s*(.*?)\s*\}$', r'\1 = \2', self.source[line].rstrip(';'))
        self._add()
        return self

    def declare(self, name: str):
        """An uninitialized object: its storage exists, but its value is unknown."""
        for cell in cells_of(self.variables, name):
            self.values[cell] = UNKNOWN
        self.steps[-1]['values'] = dict(self.values)
        return self

    def read(self, name: str, token: str | None = None):
        value = self._value(name)
        span = self._replace(token or name, value)
        self._carry(span, name)
        self._add({'kind': 'read', 'name': name, 'value': value, 'span': span})
        return self

    def _carry(self, span: list[int], source) -> None:
        """Remember what the right-hand side holds, so a write copies pointer targets."""
        if span[0] >= self.pane.rfind('= ') + 2 * ('= ' in self.pane):
            self.carry = source

    def address(self, name: str):
        value = str(self._address(name))
        span = self._replace('&' + name, value)
        self._carry(span, ('address', name))
        self._add({'kind': 'addr', 'name': name, 'value': value, 'span': span})
        return self

    def _address(self, name: str) -> int:
        owner, _, member = name.partition('.')
        variable = next(item for item in self.variables if item['name'] == owner)
        if not member:
            return variable['address']
        return variable['address'] + next(item['offset'] for item in variable['fields']
                                          if item['name'] == member)

    def deref(self, token: str, target: str, via: str):
        span = self._replace(token, target)
        self._carry(span, None)
        self._add({'kind': 'deref', 'target': target, 'via': via, 'span': span})
        return self

    def evaluate(self, token: str, value: int):
        self._add({'kind': 'eval', 'value': str(value), 'span': self._replace(token, str(value))})
        return self

    def write(self, name: str, hold: float = 1.2):
        start = self.pane.rindex('= ') + 2
        text = self.pane[start:]
        values = text.strip('{}').split(', ') if text.startswith('{') else [text]
        cells = cells_of(self.variables, name)
        sources = cells_of(self.variables, self.carry) if isinstance(self.carry, str) else [None] * len(cells)
        for cell, value, source in zip(cells, values, sources):
            # Memory holds numbers: a null pointer is stored, and shown, as 0.
            self.values[cell] = 0 if value == 'nullptr' else int(value) if value.lstrip('-').isdigit() else value
            self.targets.pop(cell, None)
            if isinstance(self.carry, tuple):
                self.targets[cell] = self.carry[1]
            elif source in self.targets:
                self.targets[cell] = self.targets[source]
        self.carry = None
        target = re.search(r'(?<![\w.])' + re.escape(name) + r'(?=\s*=)', self.pane).start()
        self._add({'kind': 'write', 'name': name, 'value': text, 'span': [start, len(self.pane)],
                   'destination': [target, target + len(name)]}, hold)
        return self

    def print(self, name: str, hold: float = 1.2):
        self.read(name)
        value = self._value(name)
        start = self.pane.index('<< ') + 3
        self.stdout += value + ('\n' if 'endl' in self.pane else '')
        self._add({'kind': 'print', 'value': value, 'span': [start, start + len(value)]}, hold)
        return self

    def build(self) -> dict:
        self.steps[-1]['hold'] = 3
        trace = {'format': FORMAT, 'source': self.source, 'variables': self.variables,
                 'steps': self.steps}
        if self.title:
            trace['title'] = self.title
        validate(trace)
        return trace
