"""Shared style/layout primitives, consumed by SVG and the native Manim adapter."""
from dataclasses import dataclass
from html import escape
import re

from model import Timeline

WIDTH, HEIGHT = 1280, 720
BG, PANEL, FG, MUTED = "#101722", "#192331", "#eef3fa", "#a0afc2"
READ, WRITE = "#9cbaff", "#f5e58b"
FONT = "DejaVu Sans Mono"
WORD_WIDTH = 224
MEMORY_X, MEMORY_RIGHT, MEMORY_TOP = 652, 1182, 112
MEMORY_ROW_HEIGHT = 142
SLOT_HEIGHT = 64
EVAL_X, EVAL_BASELINE, EVAL_SIZE = 100, 466, 30


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


def memory_layout(timeline: Timeline) -> list[Rect]:
    """Pack whole variables into rows, keeping every integer slot intact."""
    x, y = MEMORY_X, MEMORY_TOP
    slots = []
    for var in timeline.variables:
        width = WORD_WIDTH * var.size / 4
        if width > MEMORY_RIGHT - MEMORY_X:
            raise ValueError("Split oversized objects into integer-sized slots before layout")
        if x + width > MEMORY_RIGHT:
            x, y = MEMORY_X, y + MEMORY_ROW_HEIGHT
        slots.append(Rect(x, y, width, SLOT_HEIGHT, PANEL))
        x += width
    return slots


def memory_center(timeline: Timeline, name: str) -> tuple[float, float]:
    index = next(i for i, var in enumerate(timeline.variables) if var.name == name)
    slot = memory_layout(timeline)[index]
    return (slot.x + slot.w / 2, slot.y + 42 - EVAL_SIZE * 0.36)


def centered_text(center_x: float, baseline: float, value: str,
                  size: float = 26, color: str = FG) -> Text:
    return Text(center_x - len(value) * size * 0.602 / 2, baseline, value, size, color)


def expression_text(expression: str) -> Text:
    # A stable left edge keeps the other operands still when a read changes width.
    return Text(EVAL_X, EVAL_BASELINE, expression, EVAL_SIZE)


def expression_value(expression: str, start: int = 0, length: int | None = None) -> Text:
    value = expression[start:] if length is None else expression[start:start + length]
    return Text(EVAL_X + start * EVAL_SIZE * 0.602, EVAL_BASELINE, value, EVAL_SIZE)


def colored_text(timeline: Timeline, text: Text) -> list[Text]:
    colors = {v.name: v.color for v in timeline.variables}
    x = text.x
    tokens = []
    for token in re.split(r"(\b[a-zA-Z_]\w*\b)", text.value):
        if token:
            tokens.append(Text(x, text.y, token, text.size, colors.get(token, text.color)))
        x += len(token) * text.size * 0.602
    return tokens


def source_expression(timeline: Timeline, line: int, write: str | None = None) -> Text:
    if write:
        match = re.search(r"\b" + re.escape(write) + r"\b", timeline.source[line])
        start, end = match.span()
    else:
        start, end = timeline.expression_spans[line]
    return Text(116 + start * 25 * 0.602, 116 + line * 52,
                timeline.source[line][start:end], 25)


def memory_value(timeline: Timeline, name: str, value: int) -> Text:
    slot = memory_layout(timeline)[next(i for i,v in enumerate(timeline.variables) if v.name == name)]
    return centered_text(slot.x + slot.w / 2, slot.y + 42, str(value), EVAL_SIZE)


def frame(timeline: Timeline, index: int, *, show_expression: bool = True,
          phase: str = "after", hide_values: tuple[str, ...] = ()) -> list[Rect | Text | Line]:
    step = timeline.steps[index]
    previous = timeline.steps[max(0, index - 1)]
    values = previous.values if phase == "transfer" and step.write else step.values
    expression = previous.expression if phase == "transfer" and step.read else step.expression
    shapes = [
        Rect(0, 0, WIDTH, HEIGHT, BG),
        Rect(48, 64, 530, 258, PANEL),
        Rect(48, 368, 530, 150, PANEL),
        Text(70, 404, "Expression evaluation", 20, MUTED),
    ]
    if show_expression:
        shapes.extend(colored_text(timeline, expression_text(expression)))
    for i, source in enumerate(timeline.source):
        y = 116 + i * 52
        if i == step.line:
            selected = source_expression(timeline, i, step.write)
            span_width = len(selected.value) * selected.size * 0.602
            highlight = WRITE if step.write else READ
            shapes += [Rect(59, y - 30, 4, 44, highlight),
                       Rect(selected.x - 3, y - 30, span_width + 6, 40, "#2e4059"),
                       Line(selected.x - 3, y + 10,
                            selected.x + span_width + 3, y + 10, highlight, 2)]
        shapes.append(Text(76, y, str(i + 1), 20, MUTED))
        shapes.extend(colored_text(timeline, Text(116, y, source, 25)))
    for var, value, slot in zip(timeline.variables, values, memory_layout(timeline)):
        live = value is not None or var.name in step.declared
        if not live and not (phase == "transfer" and var.name == step.write):
            continue
        active = step.transfer is not None and var.name in (step.read, step.write)
        edge = WRITE if var.name == step.write and active else READ if active else var.color
        if phase == "after" and var.name in step.focus:
            edge = FG
            active = True
        # Addresses label the beginning of storage; names label the whole variable.
        shapes += [Text(slot.x, slot.y - 16, str(var.address), 18, MUTED),
                   centered_text(slot.x + slot.w / 2, slot.y + slot.h + 34,
                                 var.name, 26, var.color)]
        if timeline.byte_detail:
            octets = value.to_bytes(var.size, "little", signed=True) if value is not None else None
            cell_width = slot.w / var.size
            for offset in range(var.size):
                x = slot.x + offset * cell_width
                shapes += [Rect(x, slot.y, cell_width, slot.h, PANEL, edge, 3 if active else 1),
                           centered_text(x + cell_width / 2, slot.y + 42,
                                         "" if var.name in hide_values else
                                         f"{octets[offset]:02X}" if octets else "?", 25,
                                         FG if octets else MUTED)]
        else:
            display = "" if var.name in hide_values else str(value) if value is not None else "?"
            shapes += [Rect(slot.x, slot.y, slot.w, slot.h, PANEL, edge, 3 if active else 1),
                       centered_text(slot.x + slot.w / 2, slot.y + 42,
                                     display, EVAL_SIZE, FG if value is not None else MUTED)]
    if step.stdout:
        shapes.append(Text(70, 650, "Output: " + step.stdout, 26))
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
