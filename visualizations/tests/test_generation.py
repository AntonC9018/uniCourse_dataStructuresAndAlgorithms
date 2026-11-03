"""Layout eligibility gates that must remain true even for compiler-valid inputs."""
from dataclasses import replace
from pathlib import Path
import os
import shutil
import tempfile
import xml.etree.ElementTree as ET
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from generate import applicable, render
from model import EXPRESSION
from tracing import Unsupported, trace


class LayoutEligibilityTests(unittest.TestCase):
    def test_address_gaps_cannot_be_drawn_as_adjacent_cells(self):
        variables = (EXPRESSION.variables[0], replace(EXPRESSION.variables[1], address=76))
        with self.assertRaisesRegex(Unsupported, 'noncontiguous'):
            applicable(replace(EXPRESSION, variables=variables))

    def test_ordinary_contiguous_example_fits(self):
        applicable(EXPRESSION)


@unittest.skipUnless((os.environ.get('CLANGXX') or shutil.which('clang++'))
                     and os.environ.get('COURSE_MANAGEMENT_CHROMIUM_EXECUTABLE')
                     and shutil.which('node'), 'local compiler/browser renderer dependencies required')
class PaneInitializationTests(unittest.TestCase):
    def test_compiler_valid_initializers_render_valid_pane_statements(self):
        for source, expected in [('int a = {5}; int b=a;', 'inta=5;'),
                                 ('int const a{}; int b=a;', 'intconsta=0;')]:
            with self.subTest(source=source), tempfile.TemporaryDirectory() as directory:
                timeline=trace(source, runtime=False)
                timeline=replace(timeline, steps=tuple(s for s in timeline.steps if s.line==0))
                output=Path(directory)/'state.svg'
                render(timeline,output,'static')
                root=ET.parse(output).getroot()
                pane=root.find(".//{*}g[@data-evaluation='open']")
                self.assertIsNotNone(pane)
                self.assertEqual(''.join(pane.itertext()).replace(' ',''),expected)
                self.assertEqual(root[0].get('fill'),'#101722')


if __name__ == '__main__':
    unittest.main()
