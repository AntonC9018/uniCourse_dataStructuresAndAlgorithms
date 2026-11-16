---
slug: en/cpp/labs/preprocessor
---
<!-- course-site-backlink:start -->
[This lesson on the website](https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms/en/cpp/labs/preprocessor/)
<!-- course-site-backlink:end -->
# Preprocessor

- [Video about compilation phases][video].

Before the compiler ever looks at types and expressions, the preprocessor goes over the source text.
It expands macros, decides which conditional sections to keep, and pastes in other files.
This lab covers macros first, then includes. By "include" we mean `#include`, not C++ modules.

Use `g++`, GCC's C++ driver, for these examples, and save each program as `main.cpp`.
Every numbered example stands on its own unless it says it reuses files from another one.
Run the commands from the directory that contains those files.

```sh
g++ -std=c++20 -E main.cpp
```

`-E` stops right after preprocessing and prints the result.
Really do run it and look at the output before you open the answer.
The lines starting with `#` in that output only record where the code came from.
They are not your original directives. Add `-P` to hide them in short examples:

```sh
g++ -std=c++20 -E -P main.cpp
```

To compile and run a valid example:

```sh
g++ -std=c++20 main.cpp -o app
./app
```

Unless a task asks something else, predict the preprocessed code, whether it compiles,
and what it prints. Keep in mind that `-E` succeeding says nothing about whether the C++ is valid.

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

The comments disappear. Each one becomes whitespace, so the tokens around it don't stick together.
The compiler sees an initialization equivalent to `int a = 2 + 3;`.
The program compiles and prints nothing.
</details>

### 2. An unused macro

What does `-E -P` produce? Does defining the macro add anything to `main`?

```cpp
#define NUMBER 5

int main()
{
}
```

<details>
<summary>Answer</summary>

The preprocessed code contains only the empty `main` function.
`#define` tells the preprocessor what to substitute if it encounters `NUMBER` later.
Here `NUMBER` is never used, so there is nothing to substitute.
The definition does not create a variable or execute anything.
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
The `#define` line itself is gone; it does not turn into a C++ declaration.
`#include <iostream>` produces a lot of output, so look for `main` near the very end.
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
`number` stays a name in the preprocessed code, and its declared type makes `b` a `double`.
Integer division drops the fractional part, while floating-point division keeps it.
A macro is just replacement tokens and has no C++ type of its own.
A `constexpr` variable, on the other hand, is a real C++ object with a type,
whose initializer is a constant expression.
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
Nothing is called here. The compiler simply gets an ordinary variable definition.
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
The second line defines `a` again. Putting each use in its own nested block would avoid that.
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
The preprocessor doesn't touch the function or its calls.
Trying to use `a` in `main` would fail, since that name lives in the function's scope.
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

It prints `8`. The expansion declares an ordinary local variable in `main` that can be changed.
Coming from a macro does not make `a` a constant.
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
The replacement can be any sequence of tokens, including a whole struct initialization.
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
The parentheses are just part of the replacement text. They don't make the macro callable.
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

It prints `5`. The preprocessor knows nothing about C++ blocks.
A macro applies to everything after its definition,
until `#undef` or the end of the translation unit.
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

This redefinition is invalid, because the new replacement differs from the old one.
GCC usually just warns and goes on with `8`, but don't rely on that.
Repeating an identical definition is allowed. To replace a definition on purpose, write:

```cpp
#undef NUMBER
#define NUMBER 8
```

`#undef` removes the macro. Variables that were already initialized with it stay the same.
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
In the definition, the opening parenthesis must come right after the name, with no space.
At the use site, the parentheses are what triggers the expansion.
Writing plain `NUMBER` in `main` would leave the name unexpanded, and compilation would fail.
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
Looking like a function call does not give the macro a function's local scope.
Using it twice in this block would still define `a` twice.
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

With GCC, `-E -P` shows `bool a = false;`, so even a keyword gets replaced.
However, C++ forbids defining a macro named after a keyword such as `true`.
This is a deliberately invalid experiment, not a technique to use.
It silently changes all the code that follows, including included headers.
Never do this in real code, and remove the definition before moving on.
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

The line becomes `std::cout << 2 + 3 << std::endl;` and prints `5`.
The arguments are pasted into the replacement text as they are.
The parentheses around the argument list do not end up around the result.
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
Multiplication binds tighter than addition, so the missing parentheses happen not to matter here.
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
Both the whole replacement and each argument need their own parentheses.
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
The inner parentheses protect the arguments, and the outer ones protect the result.
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
A function's arguments are evaluated first, and their values initialize the parameters.
The body works with those parameters, not with tokens pasted into the caller's expression.
When you want something to behave like a function, write a function.
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

It prints `5`. `#if false` throws the section away before the compiler gets to check its syntax.
The invalid statement simply isn't in the preprocessed output.
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

It prints `yes`. The preprocessor computes the condition itself and keeps only the first branch.
No `if` is left to run when the program starts.
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
Change the definition to `1` and preprocess again, and the other branch is kept instead.
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

It prints `brief`. The preprocessor can't see C++ variables, not even `constexpr` ones.
Inside `#if`, any leftover identifier such as `level` counts as `0`, so the test is `0 >= 2`.
Use a normal C++ `if` to test a C++ variable. GCC's `-Wundef` warns about mistakes like this.
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

It prints `defined`. `#ifdef FEATURE` only checks that the macro exists, not what its value is.
It means the same as `#if defined(FEATURE)`. In contrast, `#if FEATURE` would test the `0`.
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

It prints `10`. `LIMIT` wasn't defined yet, so the definition inside is kept.
`#ifndef LIMIT` means `#if !defined(LIMIT)`.
Had `LIMIT` already been defined as `20`, this section would leave it alone and print `20`.
</details>

## 2. Includes

`#include` tells the preprocessor to process another file right at that spot.
That file's contents become part of the same translation unit, which is the source file after
preprocessing. The included file can have its own includes, macros, and conditional sections.
For each example, create exactly the files shown, and don't keep unrelated files from earlier ones.

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

The header adds no declarations or statements, and its comment disappears as well.
Without `-P`, the location markers still show that the preprocessor visited another file.
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

Compilation fails, because `number` was never declared in `main.cpp`.
Nobody goes looking through nearby files for missing declarations.
Just saving `number.h` next to `main.cpp` does not make it part of the program.
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

It prints `7`. In the preprocessed file, the definition of `number` comes before `main`.
For a small program with a single source file, keeping the definition in the header works fine.
Sharing code between several source files is a topic for the linker lab.
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

Compilation fails: the definition shows up after the call, and nothing declares it earlier.
An include doesn't hoist the file's contents to the top. Move the include above `main`.
</details>

### 29. Choosing which functions a header provides

Which function definitions remain in the `-E` output? Does the program compile?

`first.h`:

```cpp
#ifdef ENABLE_FIRST
int firstNumber()
{
    return 7;
}
#endif
```

`second.h`:

```cpp
#ifdef ENABLE_SECOND
int secondNumber()
{
    return 11;
}
#endif
```

`main.cpp`:

```cpp
#include <iostream>
#define ENABLE_FIRST
#include "first.h"
#include "second.h"

int main()
{
    std::cout << firstNumber() << std::endl;
}
```

<details>
<summary>Answer</summary>

Only `firstNumber` remains, and the program prints `7`.
When the preprocessor enters `first.h`, `ENABLE_FIRST` is already defined,
so it keeps the function inside that `#ifdef`.
`ENABLE_SECOND` is not defined, so it discards the function in `second.h`.
Calling `secondNumber` from `main` would fail to compile: no declaration of it remains.

The definition of `ENABLE_FIRST` has no replacement text, but that doesn't matter to `#ifdef`.
It only checks whether the macro exists.
A macro defined before an include can therefore change what that header contributes.
</details>

### 29. Defining the macro after the include

Keep the same two headers, but replace `main.cpp` with this version.
Which function definitions remain now?

`main.cpp`:

```cpp
#include <iostream>
#include "first.h"
#define ENABLE_FIRST
#include "second.h"

int main()
{
    std::cout << firstNumber() << std::endl;
}
```

<details>
<summary>Answer</summary>

Neither function definition remains, and compilation fails at the call to `firstNumber`.
When `first.h` is processed, `ENABLE_FIRST` is not defined yet, so its function is discarded.
Defining the macro afterwards does not make the preprocessor go back and reconsider that header.
`ENABLE_SECOND` is still absent, so the second header's function is discarded too.

The order matters: put a header's configuration defines before the include that uses them.
</details>

### 29. A macro defined in an earlier header

Replace the files with the versions below. There are no defines in `main.cpp` this time.
Does the macro from `first.h` affect `second.h`?

`first.h`:

```cpp
#define ENABLE_SECOND

int firstNumber()
{
    return 7;
}
```

`second.h`:

```cpp
#ifdef ENABLE_SECOND
int secondNumber()
{
    return 11;
}
#endif
```

`main.cpp`:

```cpp
#include <iostream>
#include "first.h"
#include "second.h"

int main()
{
    std::cout << firstNumber() << std::endl;
    std::cout << secondNumber() << std::endl;
}
```

<details>
<summary>Answer</summary>

Both functions remain, and the program prints `7` and `11`.
The preprocessor encounters `#define ENABLE_SECOND` while processing `first.h`.
Finishing that header does not remove the macro: it stays defined when `second.h` is processed.
It also stays defined in the rest of `main.cpp`, unless something removes it with `#undef`.

Swap the two includes, and `secondNumber` disappears, so its call fails to compile.
The preprocessor reaches its `#ifdef` before the definition in `first.h`.
Includes do not give macros their own scope; they are processed in order as part of one source file.
This does not automatically share macros with other source files compiled separately.

Libraries use configuration macros to let you control which optional functions or implementation
parts their headers provide. This is useful when it is an option the library documents:
define the macro before including the header that checks it.
An unrelated header can affect later includes too, so avoid generic macro names that might collide.
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

It prints `7`. `<iostream>` provides the declarations you need to use streams.
Look at the `-E` output: this single include usually pulls in many other headers.
That doesn't mean all of that text turns into machine instructions in your program.
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
and it puts `printf` in the `std` namespace.
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

It prints `7`. The compatibility header `<stdio.h>` puts `printf` in the global namespace.
The C++ way to write this is `<cstdio>` with `std::printf`.
Don't count on either header also making the name available in the other namespace.
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

C++ requires a declaration before this call, so GCC rejects it: `printf` is undeclared.
Include `<cstdio>` and use `std::printf`, or include `<stdio.h>`.
Having a library installed does not make its declarations visible on their own.
</details>

For the following search exercises, assume a normal GCC installation,
with no extra include-path environment variables or flags.
The directories named below are ordinary project folders, not ones GCC treats as system
include directories.

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

With `g++ -std=c++20 -E main.cpp`, the lookup fails: `settings.h` is not found.
Angle brackets don't start by searching the directory of the file doing the include.
They can still find project headers once you add that directory to the search path,
for example with `-I .`.
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

It prints `7`, as long as no earlier search directory has some other file named `iostream`.
With quotes, GCC first searches the directory of the including file, then the quote-only
paths, and then the paths used for angle brackets. That's why standard headers are found too.
Still, use angle brackets for standard headers, so a stray nearby file can't take their place.
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

It prints `11`. `-I config` adds the `config` directory to the header search path,
so the preprocessor finds `config/settings.h`.
`number` stays a C++ variable name in the output, and its definition comes from that header.
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

It prints `7`, because the directory of `main.cpp` is searched before `-I config`.
Change the include to `<settings.h>`, and the `config` copy wins, printing `11`.
The angle-bracket form doesn't look at the nearby copy at all.
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

With `-I first -I second`, it prints `11`. Swap the flags and it prints `22`.
GCC searches the `-I` directories from left to right and stops at the first match.
It doesn't merge the two headers just because they have the same name.
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
`-I` only adds places to look. It can't conjure a file that isn't in any of them.
Fix the include name, or put the missing header into one of the searched directories.
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

On a typical GCC installation, preprocessing fails because `iostream` can't be found.
`-nostdinc++` removes the default C++ header directories but keeps the other system paths.
Some packaged compiler wrappers add their own paths; check `-v` if yours still finds the header.
Don't confuse it with `-nostdinc`, which removes all the default system include directories.
</details>

### 41. Restoring the directories manually

Reuse the previous `main.cpp`. How can `-I` make preprocessing succeed again?

<details>
<summary>Answer</summary>

First, run the preprocessor normally with `-v` and note the paths printed between
`#include <...> search starts here:` and `End of search list.`:

```sh
g++ -std=c++20 -E -v main.cpp -o normal.ii
```

On a typical Linux installation, the removed C++ paths look like the three directories below.
Replace them with the real paths from your own output:

```sh
g++ -std=c++20 -nostdinc++ \
    -I /usr/include/c++/VERSION \
    -I /usr/include/TARGET/c++/VERSION \
    -I /usr/include/c++/VERSION/backward \
    -E main.cpp -o restored.ii
```

Once all the needed directories are back, preprocessing succeeds again.
Adding only the directory with `iostream` may not be enough:
that header includes internal headers such as `bits/c++config.h`,
which can live in a separate, target-specific directory.
The exact layout depends on the installation, so don't copy version numbers from another machine.
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

On a typical GCC installation, the first two commands succeed.
The `.cpp` extension tells `gcc` to treat the file as C++, with the usual C++ header paths.
The last command fails during **linking**, complaining about undefined C++ library symbols.
`gcc` does not link the C++ standard library automatically, while `g++` does.
So use `g++` for the whole C++ build. See [GCC's explanation of its C++ driver][driver].

To see a language-selection failure instead, try:

```sh
gcc -x c -E main.cpp
```

Here `-x c` forces the language to C, and C's default search paths normally don't contain
C++ headers such as `iostream`. Plain `gcc main.cpp` doesn't do this.
Compiler wrappers may change the search paths; use `-v` to see yours.
</details>

[video]: https://www.youtube.com/watch?v=CEl6YS4XhQQ&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=12
[redefinition]: https://gcc.gnu.org/onlinedocs/cpp/Undefining-and-Redefining-Macros.html
[search]: https://gcc.gnu.org/onlinedocs/cpp/Search-Path.html
[directories]: https://gcc.gnu.org/onlinedocs/gcc/Directory-Options.html
[driver]: https://gcc.gnu.org/onlinedocs/gcc/Invoking-G_002b_002b.html
