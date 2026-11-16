---
slug: en/cpp/labs/preprocessor
---
<!-- course-site-backlink:start -->
[This lesson on the website](https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms/en/cpp/labs/preprocessor/)
<!-- course-site-backlink:end -->
# Preprocessor

- [Video about compilation phases][video].

The preprocessor runs before the compiler checks C++ types and expressions.
It expands macros, chooses which conditional sections to keep, and includes other files.
This lab covers macros first, then includes. Here, including means `#include`, not C++ modules.

Use GCC's C++ driver, `g++`, for these examples. Save each program as `main.cpp`.
Each numbered example is independent unless it explicitly reuses files from another example.
Run commands from the directory containing those files.

```sh
g++ -std=c++20 -E main.cpp
```

`-E` stops after preprocessing and writes the result to standard output.
Actually run it and inspect the output before opening the answer.
Lines beginning with `#` in that output record source locations; they are not your original
directives.
Add `-P` to hide those markers when comparing short examples:

```sh
g++ -std=c++20 -E -P main.cpp
```

To compile and run a valid example instead:

```sh
g++ -std=c++20 main.cpp -o app
./app
```

Unless a task asks otherwise, predict the preprocessed code, whether it compiles,
and what it prints. A successful `-E` command alone does not mean the C++ code is valid.

## 1. Macros

### 1. Comments

```cpp
// A comment before main.
int main()
{
    int a = 2 /* another comment */ + 3;
}
```

<details>
<summary>Answer</summary>

The comments disappear. They are replaced with whitespace, so surrounding tokens do not join.
The compiler sees an initialization equivalent to `int a = 2 + 3;`.
The program compiles and prints nothing.
</details>

### 2. A constant macro

```cpp
#include <iostream>
#define NUMBER 5

int main()
{
    auto a = NUMBER;
    std::cout << a << std::endl;
}
```

<details>
<summary>Answer</summary>

`NUMBER` is replaced with `5`, so the initialization becomes `auto a = 5;`.
`a` has type `int`, and the program prints `5`.
The `#define` line itself does not remain as a C++ declaration.
`#include <iostream>` produces a lot of output; find `main` near the end.
</details>

### 3. A typed constant

```cpp
#include <iostream>
#define NUMBER 5
constexpr double number = 5;

int main()
{
    auto a = NUMBER;
    auto b = number;
    std::cout << a / 2 << std::endl;
    std::cout << b / 2 << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `2` and `2.5`.
`NUMBER` becomes the integer literal `5`, so `a` is an `int`.
`number` remains a name in the preprocessed code; its declared type makes `b` a `double`.
Integer division discards the fractional part; floating-point division preserves it here.
A macro has replacement tokens rather than its own C++ type.
A `constexpr` variable is a typed C++ object whose initializer is a constant expression.
</details>

### 4. A macro that declares a variable

What exactly does `-E -P` produce?

```cpp
#define MAKE_A int a = 5

int main()
{
    MAKE_A;
}
```

<details>
<summary>Answer</summary>

`MAKE_A;` becomes `int a = 5;` inside `main`.
There is no function call. The compiler receives an ordinary variable definition.
This compiles and prints nothing.
</details>

### 5. Using the same macro twice

```cpp
#define MAKE_A int a = 5

int main()
{
    MAKE_A;
    MAKE_A;
}
```

<details>
<summary>Answer</summary>

Preprocessing succeeds, but compilation fails: `int a = 5;` appears twice in the same scope.
The second line defines `a` again. Separate nested blocks would allow separate variables.
</details>

### 6. A function called twice

```cpp
void makeA()
{
    int a = 5;
}

int main()
{
    makeA();
    makeA();
}
```

<details>
<summary>Answer</summary>

This compiles. Each call has its own local `a`, whose lifetime ends when the call returns.
The preprocessor leaves the function and its calls alone.
Trying to use `a` in `main` would fail: that name belongs to the function's scope.
</details>

### 7. Changing the variable afterwards

```cpp
#include <iostream>
#define MAKE_A int a = 5

int main()
{
    MAKE_A;
    a = 8;
    std::cout << a << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `8`. Expansion declares an ordinary, mutable local variable in `main`.
The fact that its definition came from a macro does not make `a` a constant.
</details>

### 8. A macro as an initializer

```cpp
#include <iostream>
struct Point
{
    int x;
    int y;
};
#define START Point{ 2, 3 }

int main()
{
    Point p = START;
    std::cout << p.x << ' ' << p.y << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `2 3`. The initialization becomes `Point p = Point{ 2, 3 };`.
Replacement tokens can form a whole expression, including a struct initialization.
</details>

### 9. Parentheses in replacement text

```cpp
#include <iostream>
#define NUMBER (5)

int main()
{
    std::cout << NUMBER << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `5`. `NUMBER` expands to `(5)`.
These parentheses are part of the replacement text; they do not make the macro callable.
</details>

### 10. A macro has no block scope

```cpp
#include <iostream>

int main()
{
    {
#define NUMBER 5
        int a = NUMBER;
    }
    std::cout << NUMBER << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `5`. The preprocessor does not use C++ block scope for macros.
The definition applies to subsequent source tokens until `#undef` or the end of this translation
unit.
The local variable `a` belongs to the inner block, but the macro `NUMBER` does not.
</details>

### 11. Redefinition

```cpp
#define NUMBER 5
#define NUMBER 8

int main()
{
    int a = NUMBER;
}
```

<details>
<summary>Answer</summary>

This is an invalid redefinition: the new replacement differs from the old one.
GCC normally warns and continues using `8`; do not rely on that acceptance.
An effectively identical redefinition is allowed. To deliberately replace a definition, write:

```cpp
#undef NUMBER
#define NUMBER 8
```

`#undef` removes the macro definition; it does not change variables already initialized.
See [GCC's redefinition rules][redefinition].
</details>

### 12. A macro with an empty parameter list

```cpp
#include <iostream>
#define NUMBER() 5

int main()
{
    std::cout << NUMBER() << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `5`. `NUMBER()` is a function-like macro with no parameters.
The opening parenthesis must immediately follow its name in the definition.
At the use site, parentheses are needed to trigger expansion.
Replacing `NUMBER()` in `main` with `NUMBER` would leave that name unexpanded and fail compilation.
</details>

### 13. The same declaration through a function-like macro

```cpp
#include <iostream>
#define MAKE_A() int a = 5

int main()
{
    MAKE_A();
    std::cout << a << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `5`. `MAKE_A();` expands to `int a = 5;`.
Function-like syntax does not give a macro a function's local scope.
Using it twice in this block would still redefine `a`.
</details>

### 14. Replacing a keyword: a dangerous experiment

```cpp
#define true false

int main()
{
    bool a = true;
}
```

<details>
<summary>Answer</summary>

On GCC, `-E -P` shows `bool a = false;`: even this spelling can be replaced.
However, C++ forbids defining a macro whose name is a keyword such as `true`.
This is an intentionally invalid experiment, not a supported technique.
It can silently alter code that follows it, including included headers.
Never do this in real code; remove the definition before continuing the lab.
</details>

### 15. Arithmetic without parentheses

```cpp
#include <iostream>
#define ADD(a, b) a + b

int main()
{
    std::cout << ADD(2, 3) << std::endl;
}
```

<details>
<summary>Answer</summary>

The expression becomes `std::cout << 2 + 3 << std::endl;`, and prints `5`.
Arguments are substituted into the replacement text.
The parentheses around the argument list do not remain around the resulting expression.
</details>

### 16. More arithmetic, still the expected result

```cpp
#include <iostream>
#define ADD(a, b) a + b

int main()
{
    std::cout << ADD(2 * 3, 4 * 5) << std::endl;
}
```

<details>
<summary>Answer</summary>

It expands to `2 * 3 + 4 * 5`, so it prints `26`.
Multiplication binds more tightly than addition. The missing parentheses happen not to hurt here.
</details>

### 17. Now the missing parentheses matter

```cpp
#include <iostream>
#define ADD(a, b) a + b
#define MULTIPLY(a, b) a * b

int main()
{
    std::cout << 2 * ADD(3, 4) << std::endl;
    std::cout << MULTIPLY(2 + 3, 4 + 5) << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `10` and `19`.
The first expression becomes `2 * 3 + 4`, not `2 * (3 + 4)`.
The second becomes `2 + 3 * 4 + 5`, not `(2 + 3) * (4 + 5)`.
Both the whole replacement and its individual arguments need protection.
</details>

### 18. Parentheses around everything

```cpp
#include <iostream>
#define ADD(a, b) ((a) + (b))
#define MULTIPLY(a, b) ((a) * (b))

int main()
{
    std::cout << 2 * ADD(3, 4) << std::endl;
    std::cout << MULTIPLY(2 + 3, 4 + 5) << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `14` and `45`.
The expressions expand to `2 * ((3) + (4))` and `((2 + 3) * (4 + 5))`.
The inner parentheses protect the arguments; the outer ones protect the result.
</details>

### 19. Ordinary functions instead

```cpp
#include <iostream>
int add(int a, int b)
{
    return a + b;
}

int multiply(int a, int b)
{
    return a * b;
}

int main()
{
    std::cout << 2 * add(3, 4) << std::endl;
    std::cout << multiply(2 + 3, 4 + 5) << std::endl;
}
```

<details>
<summary>Answer</summary>

It also prints `14` and `45`.
Function arguments are expressions evaluated to initialize parameters.
The body operates on those parameters, not on tokens pasted into the caller's expression.
Use a function when you want function behavior.
</details>

### 20. Discarding a section

```cpp
#include <iostream>
int main()
{
#if false
    this is not valid C++;
#endif
    std::cout << 5 << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `5`. `#if false` discards the section before the compiler checks C++ syntax.
The invalid statement is absent from the preprocessed output.
In C++, `#if` recognizes `false` and `true`; `#if 0` and `#if 1` also work.
</details>

### 21. A preprocessor condition

```cpp
#include <iostream>
int main()
{
#if 2 + 3 == 5
    std::cout << "yes" << std::endl;
#else
    std::cout << "no" << std::endl;
#endif
}
```

<details>
<summary>Answer</summary>

It prints `yes`. The preprocessor evaluates this integer constant expression
and keeps only the first branch. No runtime `if` remains.
</details>

### 22. A condition based on a macro

```cpp
#include <iostream>
#define LEVEL 2

int main()
{
#if LEVEL >= 2
    std::cout << "details" << std::endl;
#else
    std::cout << "brief" << std::endl;
#endif
}
```

<details>
<summary>Answer</summary>

It prints `details`. `LEVEL` expands to `2` before the condition is evaluated.
Changing the definition to `1` selects the other branch when preprocessing again.
</details>

### 23. A C++ variable is not a macro

```cpp
#include <iostream>
constexpr int level = 2;

int main()
{
#if level >= 2
    std::cout << "details" << std::endl;
#else
    std::cout << "brief" << std::endl;
#endif
}
```

<details>
<summary>Answer</summary>

It prints `brief`. Even `constexpr` does not make a C++ variable visible to the preprocessor.
In this `#if`, the remaining identifier `level` is treated as `0`, giving `0 >= 2`.
Use a normal C++ `if` to test a C++ variable. GCC's `-Wundef` helps catch such mistakes.
</details>

### 24. Checking whether a macro exists

```cpp
#include <iostream>
#define FEATURE 0

int main()
{
#ifdef FEATURE
    std::cout << "defined" << std::endl;
#else
    std::cout << "missing" << std::endl;
#endif
}
```

<details>
<summary>Answer</summary>

It prints `defined`. `#ifdef FEATURE` checks whether the macro exists, not its value.
It is equivalent to `#if defined(FEATURE)`. By contrast, `#if FEATURE` would test `0`.
</details>

### 25. Checking whether a macro is absent

```cpp
#include <iostream>
#ifndef LIMIT
#define LIMIT 10
#endif

int main()
{
    std::cout << LIMIT << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `10`: `LIMIT` was absent, so the definition is kept.
`#ifndef LIMIT` means `#if !defined(LIMIT)`.
If `LIMIT` had already been defined as `20`, this section would leave it alone and print `20`.
</details>

## 2. Includes

`#include` asks the preprocessor to process another file at that position.
Its contents become part of the same translation unit: the source file after preprocessing.
The included file can itself contain includes, macros, and conditional sections.
For each example, create the files shown; do not carry unrelated files over from earlier examples.

### 26. An empty file

`empty.h`:

```cpp
// Nothing here yet.
```

`main.cpp`:

```cpp
#include "empty.h"

int main()
{
}
```

<details>
<summary>Answer</summary>

The header contributes no C++ declarations or statements. Its comment disappears too.
Without `-P`, location markers still show that another file was visited.
The program compiles and prints nothing.
</details>

### 27. A function in another file, without an include

`number.h`:

```cpp
int number()
{
    return 7;
}
```

`main.cpp`:

```cpp
#include <iostream>

int main()
{
    std::cout << number() << std::endl;
}
```

<details>
<summary>Answer</summary>

Compilation fails because `number` has not been declared in `main.cpp`.
The preprocessor does not search nearby files for missing declarations.
Merely saving `number.h` beside `main.cpp` does not make it part of the program.
</details>

### 28. Including the function before use

`number.h`:

```cpp
int number()
{
    return 7;
}
```

`main.cpp`:

```cpp
#include <iostream>
#include "number.h"

int main()
{
    std::cout << number() << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `7`. The preprocessed file contains the definition of `number` before `main`.
For this small one-source-file program, putting the definition in the header works.
How to share declarations and definitions across several source files belongs to the linker lab.
</details>

### 29. Including the function after use

`number.h`:

```cpp
int number()
{
    return 7;
}
```

`main.cpp`:

```cpp
#include <iostream>

int main()
{
    std::cout << number() << std::endl;
}

#include "number.h"
```

<details>
<summary>Answer</summary>

Compilation fails: the definition appears after the call, with no earlier declaration.
Including a file does not move its contents to the top. Move the include before `main`.
</details>

### 30. A standard C++ header

```cpp
#include <iostream>

int main()
{
    std::cout << 7 << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `7`. `<iostream>` supplies declarations needed to use the stream library.
Inspect `-E` output: this one include brings in many other headers on a typical implementation.
The resulting size does not mean all that text becomes executable instructions.
</details>

### 31. A C library facility, with its C++ header

```cpp
#include <cstdio>

int main()
{
    std::printf("%d\n", 7);
}
```

<details>
<summary>Answer</summary>

It prints `7`. `<cstdio>` is the C++ header for C-style input and output,
with `printf` available in namespace `std`.
</details>

### 32. The corresponding C header

```cpp
#include <stdio.h>

int main()
{
    printf("%d\n", 7);
}
```

<details>
<summary>Answer</summary>

It prints `7`. The compatibility header `<stdio.h>` provides `printf` in the global namespace.
The corresponding C++ spelling is `<cstdio>` with `std::printf`.
Do not rely on either header also providing the name in the other namespace.
</details>

### 33. Using the function without its header

```cpp
int main()
{
    printf("%d\n", 7);
}
```

<details>
<summary>Answer</summary>

Standard C++ requires a declaration before this call. GCC rejects it because `printf`
is undeclared. Add `<cstdio>` and use `std::printf`, or include `<stdio.h>`.
A library being installed does not make its declarations automatically visible.
</details>

For these search exercises, assume a normal GCC installation with no extra include-path
environment variables or flags. The paths named below are ordinary project directories,
not directories that GCC already treats as system include directories.

### 34. A local file with angle brackets

`settings.h`:

```cpp
constexpr int number = 7;
```

`main.cpp`:

```cpp
#include <settings.h>

int main()
{
    return number;
}
```

<details>
<summary>Answer</summary>

With `g++ -std=c++20 -E main.cpp`, header lookup fails: `settings.h` is not found.
Angle brackets do not first search the directory of the including file.
They can still find project headers if you add that directory to the search path, for example `-I
.`.
See [GCC's search-path rules][search].
</details>

### 35. A standard header with quotes

```cpp
#include "iostream"

int main()
{
    std::cout << 7 << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `7`, provided no earlier search directory contains a different file named `iostream`.
For quotes, GCC first searches the directory containing the including file, then quote-only
paths, then the paths used for angle brackets. Standard headers can therefore be found too.
Prefer angle brackets for standard headers so an accidental nearby file does not take priority.
</details>

### 36. Adding one include directory

Compile with `g++ -std=c++20 -I config main.cpp -o app`. What value is printed?

`config/settings.h`:

```cpp
constexpr int number = 11;
```

`main.cpp`:

```cpp
#include <settings.h>
#include <iostream>

int main()
{
    std::cout << number << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `11`. `-I config` adds `config` to the header search path.
The preprocessor looks for `config/settings.h`, not for a file named just `config`.
`number` remains a C++ variable name in the output; its definition comes from that header.
</details>

### 37. Quotes: nearby file or include directory?

Compile with `g++ -std=c++20 -I config main.cpp -o app`. Which header wins?

`settings.h`:

```cpp
constexpr int number = 7;
```

`config/settings.h`:

```cpp
constexpr int number = 11;
```

`main.cpp`:

```cpp
#include "settings.h"
#include <iostream>

int main()
{
    std::cout << number << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `7`: the directory containing `main.cpp` is searched before `-I config`.
Changing this include to `<settings.h>` selects the `config` copy and prints `11`.
The nearby copy is not an automatic candidate for the angle-bracket form.
</details>

### 38. Two include directories

Compare `g++ -std=c++20 -I first -I second main.cpp -o app` with the reversed order.

`first/settings.h`:

```cpp
constexpr int number = 11;
```

`second/settings.h`:

```cpp
constexpr int number = 22;
```

`main.cpp`:

```cpp
#include <settings.h>
#include <iostream>

int main()
{
    std::cout << number << std::endl;
}
```

<details>
<summary>Answer</summary>

With `-I first -I second`, it prints `11`. Reverse the flags and it prints `22`.
GCC searches these `-I` directories from left to right and stops at the first match.
It does not combine both headers just because their names match.
</details>

### 39. The file is absent from all search paths

Run `g++ -std=c++20 -I config -E main.cpp`. Does `-E` succeed?

`config/settings.h`:

```cpp
constexpr int number = 11;
```

`main.cpp`:

```cpp
#include <missing.h>

int main()
{
}
```

<details>
<summary>Answer</summary>

Preprocessing fails with a diagnostic such as `missing.h: No such file or directory`.
`-I` adds places to search; it cannot supply a file that does not exist in any of them.
Correct the include name or provide the missing header in a searched directory.
</details>

### 40. Removing the standard C++ include paths

Run `g++ -std=c++20 -nostdinc++ -E main.cpp`. Where does it fail?

```cpp
#include <iostream>

int main()
{
    std::cout << 7 << std::endl;
}
```

<details>
<summary>Answer</summary>

On a conventional GCC installation, preprocessing fails because `iostream` cannot be found.
`-nostdinc++` removes the default C++ header directories, while retaining other system paths.
Some packaged compiler wrappers add their own explicit paths; inspect `-v` if yours still finds it.
This option is different from `-nostdinc`, which removes all default system include directories.
</details>

### 41. Restoring the directories manually

Reuse the previous `main.cpp`. How can `-I` make preprocessing succeed again?

<details>
<summary>Answer</summary>

First record the paths printed between `#include <...> search starts here:` and
`End of search list.` by a normal preprocessing run:

```sh
g++ -std=c++20 -E -v main.cpp -o normal.ii
```

On a typical Linux installation, the removed C++ paths resemble these three directories.
Replace them with the actual paths from your own output:

```sh
g++ -std=c++20 -nostdinc++ \
    -I /usr/include/c++/VERSION \
    -I /usr/include/TARGET/c++/VERSION \
    -I /usr/include/c++/VERSION/backward \
    -E main.cpp -o restored.ii
```

Now preprocessing succeeds if the needed directories have all been restored.
Adding only the directory containing `iostream` may not suffice:
that header itself includes implementation headers such as `bits/c++config.h`,
which can live in a target-specific directory.
The exact layout depends on the installation; do not copy another machine's version number.
See [GCC's directory options][directories].
</details>

### 42. Using gcc instead of g++

Reuse the program containing `<iostream>`. Compare:

```sh
gcc -std=c++20 -E main.cpp -o main.ii
gcc -std=c++20 -c main.cpp -o main.o
gcc main.o -o app
```

Which stage fails? Does `gcc` really omit C++ include paths for a `.cpp` file?

<details>
<summary>Answer</summary>

The first two commands normally succeed on a conventional GCC installation.
The `.cpp` extension tells `gcc` to use C++, including its usual C++ header search paths.
The last command normally fails during **linking**, with unresolved C++ library symbols.
`gcc` does not automatically link the C++ standard library; `g++` does.
Use `g++` for the complete C++ build. See [GCC's explanation of its C++ driver][driver].

To see a language-selection failure instead, try:

```sh
gcc -x c -E main.cpp
```

Here `-x c` explicitly selects C, whose default search paths normally do not include
C++ headers such as `iostream`. That is different from plain `gcc main.cpp`.
Compiler wrappers may customize search paths; use `-v` to inspect yours.
</details>

[video]: https://www.youtube.com/watch?v=CEl6YS4XhQQ&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=12
[redefinition]: https://gcc.gnu.org/onlinedocs/cpp/Undefining-and-Redefining-Macros.html
[search]: https://gcc.gnu.org/onlinedocs/cpp/Search-Path.html
[directories]: https://gcc.gnu.org/onlinedocs/gcc/Directory-Options.html
[driver]: https://gcc.gnu.org/onlinedocs/gcc/Invoking-G_002b_002b.html
