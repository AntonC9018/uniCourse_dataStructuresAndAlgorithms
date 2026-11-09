"""Static, compiler-derived layouts; never execute the example's statements."""
from pathlib import Path
import tempfile

from records import layouts
from toolchain import Unsupported
from tracing import _body, _main_ast
from trace_format import FORMAT, validate


def trace(source: str) -> dict:
    body = _body(source)
    with tempfile.TemporaryDirectory(prefix='course-layout-') as temporary:
        program = ('#include <iostream>\n#include <cstdint>\n#include <cstddef>\n'
                   'using namespace std;\nint main() {\n' + body + '\n}\n')
        records = layouts(_main_ast(program, Path(temporary)), Path(temporary), layout_only=True)
    if not records:
        raise Unsupported('layout requires at least one plain struct definition')
    result = {'format': FORMAT, 'kind': 'layout', 'records': [
        {'name': record.name, 'size': record.size, 'alignment': record.alignment,
         'fields': record.fields} for record in records.values()]}
    validate(result)
    return result
