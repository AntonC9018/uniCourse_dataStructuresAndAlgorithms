"""Layout eligibility gates that must remain true even for compiler-valid inputs."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
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


if __name__ == '__main__':
    unittest.main()
