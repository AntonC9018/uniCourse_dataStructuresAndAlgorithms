"""Manual traces for the #57 design prototype; no C++ interpreter."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Variable:
    name: str
    address: int
    size: int = 4
    color: str = "#61d4c4"


@dataclass(frozen=True)
class Step:
    line: int
    expression: str
    values: tuple[int | None, ...]
    read: str | None = None
    write: str | None = None
    transfer: int | None = None
    stdout: str = ""
    hold: float = 1.2


@dataclass(frozen=True)
class Timeline:
    name: str
    title: str
    source: tuple[str, ...]
    variables: tuple[Variable, ...]
    steps: tuple[Step, ...]


VARIABLES = (Variable("a", 64), Variable("b", 68, color="#ffbd69"))
EXPRESSION = Timeline(
    "expression", "a + 6",
    ("int a{5};", "int b{a + 6};", "a = 7;", "std::cout << b;"),
    VARIABLES,
    (
        Step(0, "5", (None, None)),
        Step(0, "5", (5, None), write="a", transfer=5),
        Step(1, "a + 6", (5, None), read="a"),
        Step(1, "5 + 6", (5, None), read="a", transfer=5),
        Step(1, "11", (5, None)),
        Step(1, "11", (5, 11), write="b", transfer=11),
        Step(2, "7", (5, 11)),
        Step(2, "7", (7, 11), write="a", transfer=7),
        Step(3, "b", (7, 11), read="b"),
        Step(3, "11", (7, 11), read="b", transfer=11),
        Step(3, "11", (7, 11), stdout="11", hold=3.5),
    ),
)
SWAP = Timeline(
    "swap", "a = b; b = a;",
    ("int a{1};", "int b{2};", "a = b;", "b = a;"),
    VARIABLES,
    (
        Step(0, "1", (None, None)),
        Step(0, "1", (1, None), write="a", transfer=1),
        Step(1, "2", (1, None)),
        Step(1, "2", (1, 2), write="b", transfer=2),
        Step(2, "b", (1, 2), read="b"),
        Step(2, "2", (1, 2), read="b", transfer=2),
        Step(2, "2", (2, 2), write="a", transfer=2),
        Step(3, "a", (2, 2), read="a"),
        Step(3, "2", (2, 2), read="a", transfer=2),
        Step(3, "2", (2, 2), write="b", transfer=2, hold=3.5),
    ),
)
TIMELINES = (EXPRESSION, SWAP)
