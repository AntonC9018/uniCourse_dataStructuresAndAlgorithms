"""Layout eligibility gates that must remain true even for compiler-valid inputs."""
import copy
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'player'))
import fixtures  # noqa: E402
import generate  # noqa: E402
from generate import applicable  # noqa: E402
from tracing import Unsupported  # noqa: E402


class LayoutEligibilityTests(unittest.TestCase):
    def setUp(self):
        # Addresses a 64, b 68, p 72: contiguous, the pointer aligned.
        self.trace = fixtures.reassign()

    def changed(self, **addresses):
        trace = copy.deepcopy(self.trace)
        for variable in trace['variables']:
            variable['address'] = addresses.get(variable['name'], variable['address'])
        return trace

    def test_ordinary_examples_fit(self):
        applicable(self.trace)
        applicable(fixtures.double_pointer())

    def test_alignment_padding_above_a_pointer_fits(self):
        # Clang places `int a; int* p;` as p 64..72, padding, a 76..80.
        applicable(self.changed(p=64, b=80, a=76))

    def test_address_gaps_cannot_be_drawn_as_adjacent_cells(self):
        for addresses in ({'b': 72, 'p': 80}, {'p': 80}):
            with self.subTest(addresses), self.assertRaisesRegex(Unsupported, 'noncontiguous'):
                applicable(self.changed(**addresses))

    def test_names_must_fit_under_their_cells(self):
        trace = copy.deepcopy(self.trace)
        renamed = {'a': 'copiedValue', 'b': 'copiedPointer'}
        for variable in trace['variables']:
            variable['name'] = renamed.get(variable['name'], variable['name'])
        with self.assertRaisesRegex(Unsupported, 'do not fit'):
            generate._memory_fits(trace['variables'])

    def test_long_sources_and_wide_panes_are_rejected(self):
        trace = copy.deepcopy(self.trace)
        trace['source'] = trace['source'] * 2
        with self.assertRaisesRegex(Unsupported, 'source exceeds'):
            applicable(trace)
        trace = copy.deepcopy(self.trace)
        trace['steps'][-1]['pane'] = 'x' * 32
        with self.assertRaisesRegex(Unsupported, 'pane'):
            applicable(trace)


class RevisionTests(unittest.TestCase):
    def test_every_imported_tracer_module_is_hashed(self):
        hashed = {path.name for path in generate.TRACER_SOURCES}
        local = {path.stem for path in ROOT.glob('*.py')}
        pending, seen = ['generate'], set()
        while pending:
            name = pending.pop()
            if name in seen:
                continue
            seen.add(name)
            self.assertIn(name + '.py', hashed, f'{name} is imported by the tracer but not hashed')
            text = (ROOT / (name + '.py')).read_text()
            imported = set(re.findall(r'^\s*(?:from|import)\s+(\w+)', text, flags=re.MULTILINE))
            pending.extend(imported & local)


if __name__ == '__main__':
    unittest.main()
