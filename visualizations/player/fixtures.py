#!/usr/bin/env python3
"""Write the manual pointer and struct traces into `fixtures/` in the unified format.

They exercise pointer arcs, struct frames and dereference chains in the player until the
tracer supports pointers (#75) and structs (#76). Ints and fields take 4 bytes, pointers 8,
and addresses start at 64; struct layouts were checked against Clang's record layouts.
Run from the course root: python3 visualizations/player/fixtures.py
"""
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from trace_format import Builder, field, scalar, struct  # noqa: E402

FIXTURES = Path(__file__).with_name('fixtures')
# Colours by name, as in the pointer study: a teal, b amber, p violet, pp pink, q green.
A, B, P, PP, Q = range(5)


def write_through():
    t = Builder(['int a{ 1 };', 'int* b{ &a };', '*b = 2;', 'std::cout << a;'],
                [scalar('a', 64, color=A), scalar('b', 72, 8, 'ptr', B)], 'Write through a pointer')
    t.statement(0).write('a')
    t.statement(1).address('a').write('b')
    t.statement(2).read('b').deref('*64', 'a', 'b').write('a')
    t.statement(3).print('a')
    return t.build()


def reassign():
    t = Builder(['int a = 5;', 'int* p = &a;', '*p = 6;', 'int b = 7;', 'p = &b;', '*p = 8;',
                 'std::cout << a << std::endl;', 'std::cout << b << std::endl;'],
                [scalar('a', 64, color=A), scalar('b', 68, color=B), scalar('p', 72, 8, 'ptr', P)],
                'Reassigning a pointer')
    t.statement(0).write('a')
    t.statement(1).address('a').write('p')
    t.statement(2).read('p').deref('*64', 'a', 'p').write('a')
    t.statement(3).write('b')
    t.statement(4).address('b').write('p', hold=1.6)
    t.statement(5).read('p').deref('*68', 'b', 'p').write('b')
    t.statement(6).print('a')
    t.statement(7).print('b')
    return t.build()


def double_pointer():
    t = Builder(['int a = 5;', 'int b = 6;', 'int* p = &a;', 'int** pp = &p;', '**pp = 7;',
                 '*pp = &b;', '**pp = 8;', 'std::cout << a << std::endl;',
                 'std::cout << b << std::endl;'],
                [scalar('a', 64, color=A), scalar('b', 68, color=B), scalar('p', 72, 8, 'ptr', P),
                 scalar('pp', 80, 8, 'ptr', PP)], 'Pointer to a pointer')
    t.statement(0).write('a')
    t.statement(1).write('b')
    t.statement(2).address('a').write('p')
    t.statement(3).address('p').write('pp')
    t.statement(4).read('pp').deref('*72', 'p', 'pp').read('p').deref('*64', 'a', 'p').write('a')
    t.statement(5).address('b').read('pp').deref('*72', 'p', 'pp').write('p', hold=1.6)
    t.statement(6).read('pp').deref('*72', 'p', 'pp').read('p').deref('*68', 'b', 'p').write('b')
    t.statement(7).print('a')
    t.statement(8).print('b')
    return t.build()


def shared_target():
    t = Builder(['int a = 5;', 'int* p = &a;', 'int* q = p;', '*q = 6;',
                 'std::cout << *p << std::endl;'],
                [scalar('a', 64, color=A), scalar('p', 72, 8, 'ptr', P), scalar('q', 80, 8, 'ptr', Q)],
                'Two pointers to one variable')
    t.statement(0).write('a')
    t.statement(1).address('a').write('p')
    t.statement(2).read('p').write('q')
    t.statement(3).read('q').deref('*64', 'a', 'q').write('a')
    t.statement(4).read('p').deref('*64', 'a', 'p').print('a')
    return t.build()


# Field colours follow the field name, so `a.f1` and `b.f1` match.
F1, F2 = 0, 1


def two_ints():
    return [field('f1', 0, color=F1), field('f2', 4, color=F2)]


def adjacent_copy():
    # Lesson 05, example 6: two one-field structs right next to each other.
    t = Builder(['struct A { int f; };', 'A a{ 1 };', 'A b{ a };', 'a.f = 2;',
                 'std::cout << a.f << std::endl;', 'std::cout << b.f << std::endl;'],
                [struct('a', 'A', 64, 4, [field('f', 0)], 0),
                 struct('b', 'A', 68, 4, [field('f', 0)], 1)],
                'Initializing a structure from another')
    t.statement(1, 'a = {1}').write('a')
    t.statement(2).read('a').write('b', hold=1.6)
    t.statement(3).write('a.f')
    t.statement(4).print('a.f')
    t.statement(5).print('b.f')
    return t.build()


def copy_assignment():
    # Lesson 05, example 9.
    t = Builder(['struct A { int f1; int f2; };', 'A a;', 'a.f1 = 5;', 'a.f2 = 6;', 'A b;',
                 'b.f1 = 7;', 'b = a;', 'std::cout << b.f1 << std::endl;',
                 'std::cout << b.f2 << std::endl;'],
                [struct('a', 'A', 64, 8, two_ints(), 0), struct('b', 'A', 72, 8, two_ints(), 1)],
                'Assigning a structure')
    t.statement(1).declare('a')
    t.statement(2).write('a.f1')
    t.statement(3).write('a.f2')
    t.statement(4).declare('b')
    t.statement(5).write('b.f1')
    t.statement(6).read('a').write('b', hold=1.6)
    t.statement(7).print('b.f1')
    t.statement(8).print('b.f2')
    return t.build()


def arrow_operator():
    # Lesson 05, example 12.
    t = Builder(['struct A { int f1; int f2; };', 'A a;', 'a.f1 = 5;', 'A* pa = &a;',
                 '(*pa).f2 = 6;', 'pa->f1 = 7;', 'std::cout << a.f1 << std::endl;',
                 'std::cout << a.f2 << std::endl;'],
                [struct('a', 'A', 64, 8, two_ints(), 0), scalar('pa', 72, 8, 'ptr', 1)],
                'The -> operator')
    t.statement(1).declare('a')
    t.statement(2).write('a.f1')
    t.statement(3).address('a').write('pa')
    t.statement(4).read('pa').deref('(*64)', 'a', 'pa').write('a.f2')
    t.statement(5).read('pa').deref('64->f1', 'a.f1', 'pa').write('a.f1')
    t.statement(6).print('a.f1')
    t.statement(7).print('a.f2')
    return t.build()


def copy_through_pointer():
    # Lesson 05, example 11.
    t = Builder(['struct A { int f1; int f2; };', 'A a;', 'a.f1 = 5;', 'a.f2 = 6;',
                 'A* pa = &a;', 'a.f1 = 7;', 'A b = *pa;', 'std::cout << b.f1 << std::endl;'],
                [struct('a', 'A', 64, 8, two_ints(), 0), scalar('pa', 72, 8, 'ptr', 1),
                 struct('b', 'A', 80, 8, two_ints(), 2)],
                'Copying through a structure address')
    t.statement(1).declare('a')
    t.statement(2).write('a.f1')
    t.statement(3).write('a.f2')
    t.statement(4).address('a').write('pa')
    t.statement(5).write('a.f1')
    t.statement(6).read('pa').deref('*64', 'a', 'pa').read('a').write('b', hold=1.6)
    t.statement(7).print('b.f1')
    return t.build()


def field_address():
    # Lesson 05, example 7, with a second field so the field address differs from the struct's.
    t = Builder(['struct A { int f1; int f2; };', 'A a{};', 'int* b = &a.f2;', '*b = 5;',
                 'std::cout << a.f2 << std::endl;'],
                [struct('a', 'A', 64, 8, two_ints(), 0), scalar('b', 72, 8, 'ptr', 1)],
                'Field addresses')
    t.statement(1, 'a = {0, 0}').write('a')
    t.statement(2).address('a.f2').write('b')
    t.statement(3).read('b').deref('*68', 'a.f2', 'b').write('a.f2')
    t.statement(4).print('a.f2')
    return t.build()


def shallow_copy():
    # Lesson 05, example 26. Clang: sizeof(A) = 16, with 4 bytes of tail padding.
    def fields():
        return [field('pa', 0, 8, 'ptr', 0), field('a', 8, 4, 'int', 1)]
    t = Builder(['struct A { int* pa; int a; };', 'A s1 { .pa = nullptr, .a = 1 };',
                 's1.pa = &s1.a;', 'A s2 { s1 };', '*s2.pa = 2;',
                 'std::cout << s1.a << std::endl;', 'std::cout << s2.a << std::endl;'],
                [struct('s1', 'A', 64, 16, fields(), 0), struct('s2', 'A', 80, 16, fields(), 1)],
                'Copying a structure with a pointer field')
    t.statement(1, 's1 = {nullptr, 1}').write('s1')
    t.statement(2).address('s1.a').write('s1.pa')
    t.statement(3).read('s1').write('s2', hold=1.6)
    t.statement(4).read('s2.pa').deref('*72', 's1.a', 's2.pa').write('s1.a')
    t.statement(5).print('s1.a')
    t.statement(6).print('s2.a')
    return t.build()


TRACES = {
    'pointer-write-through': write_through, 'pointer-reassign': reassign,
    'pointer-double': double_pointer, 'pointer-shared-target': shared_target,
    'struct-adjacent-copy': adjacent_copy, 'struct-copy-assignment': copy_assignment,
    'struct-arrow': arrow_operator, 'struct-copy-through-pointer': copy_through_pointer,
    'struct-field-address': field_address, 'struct-shallow-copy': shallow_copy,
}


def render() -> dict[str, str]:
    """File name → content, deterministic so the committed fixtures can be checked."""
    return {name + '.json': json.dumps(build(), indent=1, sort_keys=True) + '\n'
            for name, build in TRACES.items()}


if __name__ == '__main__':
    FIXTURES.mkdir(exist_ok=True)
    for name, content in render().items():
        (FIXTURES / name).write_text(content)
        print(FIXTURES / name)
