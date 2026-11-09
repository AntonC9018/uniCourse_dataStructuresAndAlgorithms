"""Layout eligibility gates that must remain true even for compiler-valid inputs."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import generate
from generate import applicable
from model import EXPRESSION
from tracing import Unsupported


class LayoutEligibilityTests(unittest.TestCase):
    def test_address_gaps_cannot_be_drawn_as_adjacent_cells(self):
        variables = (EXPRESSION.variables[0], replace(EXPRESSION.variables[1], address=76))
        with self.assertRaisesRegex(Unsupported, 'noncontiguous'):
            applicable(replace(EXPRESSION, variables=variables))

    def test_ordinary_contiguous_example_fits(self):
        applicable(EXPRESSION)


class RevisionTests(unittest.TestCase):
    def test_every_imported_tracer_module_is_hashed(self):
        hashed = {path.name for path in generate.TRACER_SOURCES}
        root = Path(generate.__file__).parent
        local = {path.stem for path in root.glob('*.py')}
        for name in ('generate.py', 'tracing.py'):
            imports = {line.split()[1].split('.')[0] for line in (root / name).read_text().splitlines()
                       if line.startswith(('import ', 'from ')) and not line.startswith('from __future__')}
            for module in imports & local:
                self.assertIn(module + '.py', hashed, f'{name} imports {module} but it is not hashed')


if __name__ == '__main__':
    unittest.main()
