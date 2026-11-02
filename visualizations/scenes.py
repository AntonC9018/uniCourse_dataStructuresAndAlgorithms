"""Native Manim adapter for the same primitives serialized by the SVG renderer."""
from functools import cache

from manim import Scene, FadeIn, Text as ManimText, RoundedRectangle, VGroup
from manim import Rectangle, Line as ManimLine, config

from drawing import WIDTH, HEIGHT, BG, FG, PANEL, FONT, EVAL_CENTER, frame, memory_center
from drawing import Rect, Text, Line
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

    def badge(self, value):
        text = ManimText(str(value), font=FONT, font_size=24, color=FG)
        box = RoundedRectangle(width=max(0.8, text.width + 0.3), height=0.5,
                               corner_radius=0.06, fill_color=PANEL, fill_opacity=1,
                               stroke_color=FG, stroke_width=1)
        return VGroup(box, text)

    def construct(self):
        current = None
        for index, step in enumerate(self.timeline.steps):
            # Writes move the evaluated value before revealing the changed bytes.
            if step.write and step.transfer is not None and current is not None:
                badge = self.badge(step.transfer).move_to(point(EVAL_CENTER))
                self.add(badge)
                self.play(badge.animate.move_to(
                    point(memory_center(self.timeline, step.write))), run_time=0.75)
                self.remove(badge)
            following = VGroup(*(mobject(s).copy() for s in frame(self.timeline, index)))
            self.play(FadeIn(following), run_time=0.25)
            if current is not None:
                self.remove(current)
            current = following
            if step.read and step.transfer is not None:
                badge = self.badge(step.transfer).move_to(
                    point(memory_center(self.timeline, step.read)))
                self.add(badge)
                self.play(badge.animate.move_to(point(EVAL_CENTER)), run_time=0.75)
                self.remove(badge)
            self.wait(step.hold)


class ExpressionTimeline(TimelineScene):
    timeline = EXPRESSION


class SwapTimeline(TimelineScene):
    timeline = SWAP
