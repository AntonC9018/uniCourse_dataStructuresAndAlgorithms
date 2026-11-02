"""Native Manim adapter for the same primitives serialized by the SVG renderer."""
from functools import cache
from dataclasses import replace

from manim import (Scene, Text as ManimText, Transform, VGroup, Arrow, VMobject,
                   MoveAlongPath, FadeOut, UP, ShowPassingFlash)
from manim import Rectangle, Line as ManimLine, config

from drawing import WIDTH, HEIGHT, BG, PANEL, FONT, EVAL_SIZE, frame, memory_center, expression_value
from drawing import (Rect, Text, Line, source_expression, expression_text, colored_text,
                     memory_layout, memory_value, READ, WRITE, FG, EVAL_X, EVAL_BASELINE)
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

    def text_group(self, text):
        return VGroup(*(mobject(s).copy() for s in colored_text(self.timeline, text)))

    def show_state(self, index, **kwargs):
        if self.current is not None:
            self.remove(self.current)
        self.current = VGroup(*(mobject(s).copy() for s in frame(self.timeline, index, **kwargs)))
        self.add(self.current)

    def slide(self, copied, positions, color, duration=1.25):
        points = [point(p) for p in positions]
        path = VMobject().set_points_as_corners(points)
        arrow = VGroup(*(ManimLine(a, b, color=color, stroke_width=2)
                             for a, b in zip(points[:-2], points[1:-1])),
                       Arrow(points[-2], points[-1], buff=0, color=color, stroke_width=2,
                             max_tip_length_to_length_ratio=0.15))
        self.add(arrow, copied)
        self.play(MoveAlongPath(copied, path), run_time=duration)
        self.remove(arrow)

    def copy_source(self, index):
        step = self.timeline.steps[index]
        self.show_state(index, show_expression=False)
        source = source_expression(self.timeline, step.line)
        assert source.value == step.expression
        copied = self.text_group(source)
        target = self.text_group(expression_text(step.expression))
        start = source.x + len(source.value) * source.size * 0.602 / 2
        end = EVAL_X + len(step.expression) * EVAL_SIZE * 0.602 / 2
        self.wait(0.35)
        # Leave the source through its right edge, then enter from below the
        # evaluation panel. Neither the copy nor its arrow crosses other lines.
        self.slide(copied, [(start, source.y - source.size * 0.36),
                            (604, source.y - source.size * 0.36),
                            (604, 550), (end, 550),
                            (end, EVAL_BASELINE - EVAL_SIZE * 0.36)], READ)
        self.play(Transform(copied, target), run_time=0.2)
        self.remove(copied)

    def transfer(self, index):
        step = self.timeline.steps[index]
        previous = self.timeline.steps[index - 1]
        name = step.read or step.write
        var = next(v for v in self.timeline.variables if v.name == name)
        slot = memory_layout(self.timeline)[self.timeline.variables.index(var)]
        memory = memory_center(self.timeline, name)
        hidden = (name,) if step.write else ()
        self.show_state(index, phase="transfer", hide_values=hidden)
        if step.write:
            old = previous.values[self.timeline.variables.index(var)]
            if old is not None:
                removed = mobject(memory_value(self.timeline, name, old)).copy()
                self.add(removed)
                # Only the overwritten glyph leaves; the slot and scene stay steady.
                self.play(FadeOut(removed, shift=UP * 0.45), run_time=0.45)
                self.wait(0.2)
            copied = self.text_group(expression_value(step.expression))
        else:
            start, end = step.read_span
            assert previous.expression[start:end] == name
            literal = str(step.transfer)
            assert step.expression == previous.expression[:start] + literal + previous.expression[end:]
            operand = expression_value(previous.expression, start, end - start)
            mask = mobject(Rect(operand.x, operand.y - EVAL_SIZE,
                                (end - start) * EVAL_SIZE * 0.602,
                                EVAL_SIZE * 1.3, PANEL)).copy()
            self.add(mask)
            copied = mobject(replace(expression_value(step.expression, start, len(literal)),
                                     color=var.color)).copy()
            copied.move_to(point(memory))
        destination = (EVAL_X + (step.read_span[0] + len(str(step.transfer)) / 2)
                       * EVAL_SIZE * 0.602 if step.read else
                       EVAL_X + len(step.expression) * EVAL_SIZE * 0.602 / 2,
                       EVAL_BASELINE - EVAL_SIZE * 0.36)
        # Use the outside edge of a slot to avoid its centered name. All memory
        # arrows share the gutter and enter the expression from below its text.
        edge_x = slot.x + slot.w - 18
        lane_y = slot.y + slot.h + 60
        route = [memory, (edge_x, memory[1]), (edge_x, lane_y), (620, lane_y),
                 (620, 550), (destination[0], 550), destination]
        if step.write:
            route.reverse()
        self.slide(copied, route, READ if step.read else WRITE)
        self.remove(copied)
        if step.read:
            self.remove(mask)

    def emphasize(self, names):
        outlines = []
        for var, slot in zip(self.timeline.variables, memory_layout(self.timeline)):
            if var.name in names:
                outline = mobject(Rect(slot.x - 4, slot.y - 4, slot.w + 8, slot.h + 8,
                                       PANEL, FG, 4)).copy().set_fill(opacity=0)
                outlines.append(ShowPassingFlash(outline, time_width=0.7))
        self.play(*outlines, run_time=1)

    def construct(self):
        self.current = None
        for index, step in enumerate(self.timeline.steps):
            if index == 0 or step.line != self.timeline.steps[index - 1].line:
                self.copy_source(index)
            if step.transfer is not None:
                self.transfer(index)
            self.show_state(index)
            if step.focus:
                self.emphasize(step.focus)
            self.wait(step.hold)


class ExpressionTimeline(TimelineScene):
    timeline = EXPRESSION


class SwapTimeline(TimelineScene):
    timeline = SWAP
