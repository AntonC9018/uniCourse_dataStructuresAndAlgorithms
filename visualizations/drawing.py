"""Shared style/layout primitives, consumed by SVG and the native Manim adapter."""
from dataclasses import dataclass
from html import escape
import re

from model import Timeline

WIDTH, HEIGHT = 1280, 720
BG, PANEL, FG, MUTED = "#101722", "#192331", "#eef3fa", "#a0afc2"
READ, WRITE = "#9cbaff", "#f5e58b"
FONT = "DejaVu Sans Mono"
CELL = 112
ARROW_HEAD = 10
EVAL_CENTER = (313, 493)


@dataclass(frozen=True)
class Rect:
    x: float
    y: float
    w: float
    h: float
    fill: str
    stroke: str = "none"
    width: float = 1


@dataclass(frozen=True)
class Text:
    x: float
    y: float
    value: str
    size: float = 24
    color: str = FG


@dataclass(frozen=True)
class Line:
    x: float
    y: float
    end_x: float
    end_y: float
    color: str
    width: float = 2


def memory_center(timeline: Timeline, name: str) -> tuple[float, float]:
    index = next(i for i, var in enumerate(timeline.variables) if var.name == name)
    return (876, 240 + index * 160)


def frame(timeline: Timeline, index: int) -> list[Rect | Text | Line]:
    step = timeline.steps[index]
    shapes = [
        Rect(0, 0, WIDTH, HEIGHT, BG),
        Text(48, 65, timeline.title, 32),
        Text(1030, 65, f"{index + 1:02} / {len(timeline.steps):02}", 22, MUTED),
        Line(48, 95, 1232, 95, MUTED),
        Rect(48, 132, 530, 258, PANEL),
        Rect(48, 420, 530, 150, PANEL),
        Text(70, 452, "C++  →", 18, MUTED),
        Text(EVAL_CENTER[0] - len(step.expression) * 30 * 0.602 / 2,
             507, step.expression, 30),
        Text(652, 150, "int / 4 B", 20, MUTED),
        Text(1040, 150, "hex / B", 18, MUTED),
    ]
    for i, source in enumerate(timeline.source):
        y = 184 + i * 52
        if i == step.line:
            shapes += [Rect(59, y - 30, 508, 44, "#2e4059"),
                       Rect(59, y - 30, 4, 44, READ)]
        shapes.append(Text(76, y, str(i + 1), 20, MUTED))
        # Split identifiers so variable colors also survive in the SVG output.
        x = 116
        colors = {v.name: v.color for v in timeline.variables}
        for token in re.split(r"(\b[a-zA-Z_]\w*\b)", source):
            shapes.append(Text(x, y, token, 25, colors.get(token, FG)))
            x += len(token) * 25 * 0.602
    for i, (var, value) in enumerate(zip(timeline.variables, step.values)):
        y = 230 + i * 160
        active = var.name in (step.read, step.write)
        edge = WRITE if var.name == step.write else READ if active else var.color
        shapes += [Text(652, y - 36, var.name, 26, var.color),
                   Text(690, y - 36, "= " + (str(value) if value is not None else "·"),
                        26, FG if value is not None else MUTED)]
        octets = value.to_bytes(var.size, "little", signed=True) if value is not None else None
        for offset in range(var.size):
            x = 652 + offset * CELL
            shapes += [Rect(x, y - 17, CELL, 54, PANEL, edge, 3 if active else 1),
                       Text(x + 39, y + 18, f"{octets[offset]:02X}" if octets else "··",
                            25, FG if octets else MUTED),
                       Text(x + 39, y + 63, str(var.address + offset), 17, MUTED)]
        if active:
            # Read: arrow out of memory. Write: arrow into memory. Color is redundant.
            start, end = (1148, 1122) if step.write else (1122, 1148)
            shapes += [Line(start, y + 9, end, y + 9, edge, 3),
                       Line(end, y + 9, end + (ARROW_HEAD if step.write else -ARROW_HEAD),
                            y - 1, edge, 3),
                       Line(end, y + 9, end + (ARROW_HEAD if step.write else -ARROW_HEAD),
                            y + 19, edge, 3)]
    shapes += [Rect(652, 500, 530, 70, PANEL),
               Text(672, 544, "stdout  > " + step.stdout, 23),
               Text(48, 644, "int: 4 B    ptr: 8 B    LE    @64", 19, MUTED),
               Text(48, 681, "·· : ∅     → : R     ← : W", 19, MUTED)]
    return shapes


def svg(shapes: list, title: str = "") -> str:
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" '
           f'width="{WIDTH}" height="{HEIGHT}" role="img">',
           f"<title>{escape(title)}</title>"]
    for s in shapes:
        if isinstance(s, Rect):
            out.append(f'<rect x="{s.x}" y="{s.y}" width="{s.w}" height="{s.h}" '
                       f'fill="{s.fill}" stroke="{s.stroke}" stroke-width="{s.width}"/>')
        elif isinstance(s, Text):
            out.append(f'<text x="{s.x}" y="{s.y}" font-family="{FONT},monospace" '
                       f'font-size="{s.size}" fill="{s.color}" xml:space="preserve">'
                       f'{escape(s.value)}</text>')
        else:
            out.append(f'<line x1="{s.x}" y1="{s.y}" x2="{s.end_x}" y2="{s.end_y}" '
                       f'stroke="{s.color}" stroke-width="{s.width}"/>')
    return "\n".join(out) + "\n</svg>\n"
