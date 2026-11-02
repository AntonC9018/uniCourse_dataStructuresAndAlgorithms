"""Render static snapshots with stdlib only; animation runs through Manim."""
from pathlib import Path

from drawing import frame, svg
from model import TIMELINES

OUTPUT = Path(__file__).parent / "renders"

if __name__ == "__main__":
    OUTPUT.mkdir(exist_ok=True)
    for timeline in TIMELINES:
        for index in range(len(timeline.steps)):
            target = OUTPUT / f"{timeline.name}-{index:02}.svg"
            target.write_text(svg(frame(timeline, index), timeline.title))
        (OUTPUT / f"{timeline.name}.svg").write_text(
            svg(frame(timeline, len(timeline.steps) - 1), timeline.title))
