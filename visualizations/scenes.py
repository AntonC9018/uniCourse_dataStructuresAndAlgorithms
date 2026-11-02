"""Native Manim adapter for the same primitives serialized by the SVG renderer."""
from functools import cache

from manim import Scene, Text as ManimText, Transform, VGroup
from manim import Rectangle, Line as ManimLine, config

from drawing import WIDTH, HEIGHT, BG, PANEL, FONT, EVAL_SIZE, frame, memory_center, expression_value
from drawing import Rect, Text, Line, source_expression, expression_text
from model import EXPRESSION, SWAP

config.pixel_width, config.pixel_height = WIDTH, HEIGHT
config.frame_rate = 24
config.background_color = BG
SCALE = config.frame_width / WIDTH


def point(position):
    x, y = position
    return [(x - WIDTH / 2) * SCALE, (HEIGHT / 2 - y) * SCALE, 0]


@cache
def mobject(shape):
    if isinstance(shape, Rect):
        return Rectangle(width=shape.w * SCALE, height=shape.h * SCALE,
                         fill_color=shape.fill, fill_opacity=1,
                         stroke_color=shape.stroke if shape.stroke != "none" else shape.fill,
                         stroke_width=shape.width if shape.stroke != "none" else 0).move_to(
                             point((shape.x + shape.w / 2, shape.y + shape.h / 2)))
    if isinstance(shape, Text):
        value = shape.value.strip()
        if not value:
            return VGroup()
        # Invisible M guards retain the font's cell width and baseline even for
        # punctuation-only tokens such as ";" and "··". Never stretch a glyph
        # to the width of its cell: a semicolon would become enormous.
        text = ManimText("M" + shape.value + "M", font=FONT, font_size=shape.size,
                         color=shape.color, disable_ligatures=True)
        text[0].set_opacity(0)
        text[-1].set_opacity(0)
        advance = shape.size * 0.602
        text.width = (len(shape.value) + 2) * advance * SCALE
        return text.move_to(point((shape.x + len(shape.value) * advance / 2,
                                   shape.y - shape.size * 0.36)))
    if isinstance(shape, Line):
        return ManimLine(point((shape.x, shape.y)), point((shape.end_x, shape.end_y)),
                         color=shape.color, stroke_width=shape.width)
    raise TypeError(shape)


class TimelineScene(Scene):
    """A subclass supplies a Timeline, with no renderer or layout overrides."""
    timeline = EXPRESSION

    def construct(self):
        current = None
        for index, step in enumerate(self.timeline.steps):
            if index == 0 or step.line != self.timeline.steps[index - 1].line:
                # Reveal the new source selection with an empty evaluation panel.
                # The source remains in place while its expression is copied.
                entry = VGroup(*(mobject(s).copy() for s in
                                 frame(self.timeline, index, show_expression=False)))
                if current is not None:
                    self.remove(current)
                self.add(entry)
                current = entry
                copied = mobject(source_expression(self.timeline, step.line)).copy()
                target = mobject(expression_text(step.expression)).copy()
                assert source_expression(self.timeline, step.line).value == step.expression
                self.add(copied)
                self.wait(0.35)
                self.play(Transform(copied, target), run_time=0.85)
                self.remove(copied)
            moving = None
            operand_mask = None
            if step.transfer is not None and current is not None:
                if step.read:
                    # The span refers to the variable in the preceding expression.
                    # Land at the replacement literal, before exposing the new state.
                    previous = self.timeline.steps[index - 1]
                    start, end = step.read_span
                    assert previous.expression[start:end] == step.read
                    operand = expression_value(previous.expression, start, end - start)
                    operand_mask = mobject(Rect(operand.x, operand.y - EVAL_SIZE,
                                                (end - start) * EVAL_SIZE * 0.602,
                                                EVAL_SIZE * 1.3, PANEL)).copy()
                    self.add(operand_mask)
                    literal = str(step.transfer)
                    assert step.expression == (previous.expression[:start] + literal
                                               + previous.expression[end:])
                    moving = mobject(expression_value(step.expression, start, len(literal))).copy()
                    destination = moving.get_center().copy()
                    moving.move_to(point(memory_center(self.timeline, step.read)))
                elif step.write:
                    moving = mobject(expression_value(step.expression)).copy()
                    destination = point(memory_center(self.timeline, step.write))
                if moving is not None:
                    self.add(moving)
                    self.play(moving.animate.move_to(destination), run_time=0.75)

            # Replace state between rendered frames. Fading an opaque background
            # faded the whole scene, including unchanged text and cells.
            following = VGroup(*(mobject(s).copy() for s in frame(self.timeline, index)))
            if operand_mask is not None:
                self.remove(operand_mask)
            if moving is not None:
                self.remove(moving)
            if current is not None:
                self.remove(current)
            self.add(following)
            current = following
            self.wait(step.hold)


class ExpressionTimeline(TimelineScene):
    timeline = EXPRESSION


class SwapTimeline(TimelineScene):
    timeline = SWAP
