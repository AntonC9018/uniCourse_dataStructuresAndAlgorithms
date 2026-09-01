# Variables and Types

- [Video about variables and types](https://www.youtube.com/watch?v=6ML34OuwZrc&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=6)
- [Video on the basics and more in-depth material (up to pointers)](https://www.youtube.com/watch?v=9AhNOjjyAwU&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=14)
- [Video about type conversions (up to pointers)](https://www.youtube.com/watch?v=imkDyDE7Tkw&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=28)

## Concepts

- A variable as an abstraction of a memory cell
- Relative locations of variables in RAM
- Variable definitions and declarations
- Operations on variables (reading and writing)
- Uninitialized variables, garbage data
- UB (undefined behavior)
- Initialization syntax
- Value
- Expressions and their evaluation
- Data types: signedness (negative values) and size
- Conversions between numeric types (`static_cast`)
- Integer overflow

<!-- ## Practice --> 

## Understanding the examples

Explain what happens in the following code snippets.
Also, run the code to verify your reasoning.

> When `main` is not shown, place the code in a typical source file with a `main` function:
> ```cpp
> #include <iostream>
> #include <cstdint>
>
> int main()
> {
>     // сюда
> }
> ```

### 1. Variable definition
```cpp
int a = 5;
std::cout << a << std::endl;
```

<details>
<summary>What type is <code>a</code>?</summary>

`int`. The type comes before the variable name.

`int` means that an *integer* can be stored in `a`.
</details>

### 2. Variable declaration
```cpp
int a;
std::cout << a << std::endl;
```

<details>
<summary>Answer</summary>

This code will not compile if the `-Werror` and `-Wall` flags are passed to the compiler.
Without them, it will compile and run, but the result may not be what you expect.

`a` is an *uninitialized variable*.
It is important to understand that this **does not mean** that `a` has no value.
`a` must have a value, since `a` is merely an abstraction of a
memory cell, and a memory cell **cannot be empty**.

An uninitialized variable in C++ is a variable
into which no value has yet been deliberately written.

Declaring a variable merely allocates a memory cell for that variable.
That cell may have been used by another variable before.
Such memory can retain its old value
from a previous use.
For this reason, **a variable may contain any number**,
and, as the programmer, you cannot rely on what it will contain.

> The contents of an uninitialized variable
> are also called **garbage data**.

<details>
<summary>Why can a memory cell not be empty?</summary>

Because memory consists of bytes, and each byte consists of 8 bits.
Bits can store either 0 or 1, and nothing else.
They cannot store “nothing”.
Accordingly, a byte is made up entirely of bits,
each of which is either 0 or 1.

You might decide that 0 is “nothing”, but that is not always the case.
0 can be deliberately written into a bit. 

If 0 and “nothing” were the same thing,
you would not be able to distinguish the two
by reading a bit in isolation.
Was it 0 because nothing has been written there yet,
or because someone deliberately wrote it there earlier?
</details>

</details>

<details>
<summary>What happens if you read from variable <code>a</code>?</summary>

Since `a` is uninitialized, you will obtain whatever value
was in the memory before it was allocated to `a`.

However, reading from an uninitialized variable is considered UB (undefined behavior),
which by definition means that anything can happen,
and the compiler is allowed to assume that such a read is impossible.
</details>

### 3. Defining a variable with the same name
```cpp
int a = 5;
int a = 6;
std::cout << a << std::endl;
```

<details>
<summary>Correct answer:</summary>

You cannot define two variables with the same name.
You can overwrite the values of existing variables.
</details>

### 4. Assigning one variable to another
```cpp
int a = 5;
int b = 6;
a = b;
b = 7;
std::cout << a << std::endl;
```

<details>
<summary>Correct answer:</summary>

`6` is written to `a` on line 3.
Writing `7` to `b` on line 4 does not affect `a`'s memory cell.

It is important to remember that instructions execute one after another, from top to bottom.

It is also important to remember that assigning one variable to another does not link their cells.
`a = b` copies the value in cell `b` into cell `a`.
This is a one-time action; the cells will not be linked after this line executes.
No matter how you change `b` afterwards, it will not affect `a`.
</details>

<details>
<summary>What is the type of expression <code>b</code>?</summary>

The expression `b` in `a = b` means “read the value of the variable `b`”.
The phrase “the type of an expression” is shorthand for
“the static (known at compile time) type of the value
obtained when evaluating the expression”.
Here, it is the same as the type of variable `b`.

The code compiles because the type of variable `a` (`int`), into which
the result of the expression `b` is written, **is compatible with the type of expression `b`** (also `int`).
</details>

### 5. Assigning an expression to a variable
```cpp
int a = 5;
int b = a + 6;
a = 7;
std::cout << b << std::endl;
```
<details>
<summary>Correct answer:</summary>

On line 2, the *result of the expression* on the right-hand side of the assignment (`a + 6`) is written to `b`.
Evaluating this expression means turning it into a single *value*.

`a + 6` -> `5 + 6` -> `11`

The result of evaluating the expression is the value 11, which is written to cell `b`.

Further changes to `a` do not affect the previous operation, since its *result* has already been stored in `b`.
</details>

### 6. String value
```cpp
int a = "abc";
```

<details>
<summary>Correct answer:</summary>

The compiler reports a type incompatibility error.

You cannot write the string literal `"abc"` to a cell that stores an `int`.
</details>

### 7. Uniform initialization
```cpp
int a{5};
```

<details>
<summary>Correct answer:</summary>

This syntax is largely equivalent to the following:
```cpp
int a = 5;
```

It differs in that the compiler reports an error
when an assignment could result in a loss of information.

For example, the following code compiles if no compiler flags are provided.
When run, the number `5` will be stored in `a` (the fractional part will be discarded).
```cpp
int a = 5.6;
```

If curly braces are used instead, it will not compile.
This strictness can help us notice possible mistakes.
```cpp
int a{ 5.6 };
```
</details>

### 8. The `sizeof` operator
```cpp
std::cout << sizeof(int) << std::endl;
std::cout << sizeof(uint8_t) << std::endl;
int a;
std::cout << sizeof(a) << std::endl;
```
<details>
<summary>Answer:</summary>

`sizeof` is evaluated at compile time and yields the size, in bytes, of a variable or type.

For example:
- `sizeof(int)` produces `4`;
- `sizeof(a)` is equivalent to `sizeof(тип_а)`, that is, `sizeof(int)`, that is, `4`;
- `sizeof(uint8_t)` produces `1` (8 bits — 1 byte).

</details>

### 9. `auto`

What type will `a` have in this example?
```cpp
auto a = 5;
```

<details>
<summary>What does <code>auto</code> mean?</summary>

`auto` means that the type is automatically inferred from the right-hand side of the definition.
Since the right-hand side is an integer literal, `a` will have type `int`.

You can think of `auto` as being replaced with `int` during compilation.
</details>

### 10. `auto` with uniform initialization

```cpp
auto a{ 5 };
```

<details>
<summary>Answer</summary>

This is the same as in the previous example.
</details>

### 11. `auto` and `static_cast`

```cpp
auto a{ static_cast<uint8_t>(5) };
```

<details>
<summary>What does <code>static_cast&lt;uint8_t&gt;</code> do?</summary>

`static_cast<uint8_t>(5)` is an expression
whose result is the number `5` of type `uint8_t`.

- `static_cast` says, “convert the result of an expression from one type to another”.
- `<uint8_t>` indicates the type to convert to.
- `(5)` in parentheses specifies the expression whose result must be converted.

So the following happens:
- The expression in parentheses (`(5)`) is evaluated, producing the number `5` of type `int`.
- A `static_cast` to the type specified between `<...>`, namely `uint8_t`, is performed.
  Since `5` fits in 1 byte, it converts without any problem.
- `static_cast<uint8_t>(5)` is replaced with the number `5` of type `uint8_t`.
- `auto` infers the type of the initializer expression and is replaced with `uint8_t`.
</details>

### 12. `static_cast` to a larger type

```cpp
uint8_t a{ 5 };
int b{ static_cast<int>(a) };
```

<details>
<summary>Answer</summary>

An implicit conversion equivalent to `static_cast<int>` occurs here, even though it is not written explicitly.
Since every value that can be stored in `a` also fits in `b`,
you can assign `a` directly to `b`,
which performs the conversion from `uint8_t` to `int` automatically.
</details>


### 13. `static_cast` 
```cpp
#include <cstdint>
#include <iostream>

int main()
{
    uint32_t a{ 256 };
    uint8_t b{ static_cast<uint8_t>(a) };
    uint32_t c{ b };
    std::cout << c << std::endl;
}
```

<details>
<summary>What does <code>static_cast&lt;uint8_t&gt;</code> do?</summary>

In this example, `static_cast<uint8_t>` takes only the least significant byte of the number in `a`,
discarding the upper 3 bytes. This is called truncation.

Without `static_cast<uint8_t>`,
the conversion occurs implicitly.
The compiler does not report an error in this case
if no warning flags are passed during compilation.

> To have the compiler detect and reject such situations,
> pass warning flags during compilation, for example:
> ```
> g++ test.cpp -Wall -Werror -Wconversion
> ```
> 
> In addition, you can use brace initialization.
> The following will also not compile:
> ```cpp
> uint8_t b { 256 }; // narrowing conversion
> ```
> 
> And the following will probably produce a warning:
> ```cpp
> uint32_t a { 256 };
> uint8_t b { a }; // narrowing conversion
> ```

  
</details>

<details>
<summary>Correct answer:</summary>

`static_cast<uint8_t>` truncates the value in `a`,
leaving only the last byte (the least significant byte).

The result is 0, because 256 is represented as `1 0000 0000` in binary,
and truncating this number to 8 bits leaves only `0000 0000`,
discarding the leading 1.
</details>

<details>
<summary>What happens if a different value is stored in <code>a</code>?</summary>

- Value 257: `1 0000 0001` is stored, becoming `0000 0001` after truncation.
- Value 258: `1 0000 0010` is stored, becoming `0000 0010` after truncation.
- Value 511: `1 1111 1111` is stored, becoming `1111 1111` after truncation.
- Value 512: `10 0000 0000` is stored, becoming `0000 0000` after truncation.
</details>

### 14. Bitwise operation (advanced level)
```cpp
#include <cstdint>
#include <iostream>

int main()
{
    uint8_t a{ 0 };
    uint8_t b{ ~a };
    int32_t c{ b };
    std::cout << c;
}
```

<details>
<summary>

What does `~` do?

</summary>

It is a bitwise operator that inverts every bit in the binary representation of a number:
it turns each 0 into 1 and each 1 into 0.
For example, `1010 0011` -> `0101 1100`.
</details>

<details>
<summary>Correct answer</summary>

- 0 is stored in an 8-bit variable.
- The `~` operator is applied to the 8-bit value 0: `0000 0000` -> `1111 1111` (255).
- The result is stored in the 8-bit variable `b`.
- The result is stored unchanged in the 32-bit variable `c` (for printing).

</details>

### 15. Changing the sign (advanced level)
```cpp
#include <cstdint>
#include <iostream>

int main()
{
    uint8_t a{ 255 };
    int8_t b{ static_cast<int8_t>(a) };
    int32_t c{ b };
    std::cout << c;
}
```

<details>

<summary>

What does `static_cast<int8_t>` do?

</summary>

In this example, it interprets the unchanged bit representation of the number stored in `a` as a signed integer.

For example, if `a` is 0, the result will be 0, because `0000 0000`
is 0 as both a signed and an unsigned integer.

If `a` is 128, that is, `1000 0000`, it becomes `-128`, because `1000 0000`
represents -128 as a signed number.
</details>

<details>

<summary>

What happens when a smaller signed `int8_t` value is assigned to `int32_t`?

</summary>

If the value is negative, the result will also be negative (the upper bits are filled with 1s).
For example, -1 is written as `1111 1111` in 8 bits,
and becomes `1111 1111 1111 1111 1111 1111 1111 1111` in 32 bits,
which is also -1.

If the value is positive, the result will also be positive (the upper bits are filled with 0s).
For example, 10 is written as `0000 1010` in 8 bits,
and becomes `0000 0000 0000 0000 0000 0000 0000 1010` in 32 bits,
which is also 10.

In short, `int32_t` will always store *the same numeric value*.
</details>

<details>
<summary>Correct answer:</summary>

- 255 is written to `a` as `1111 1111`.
- `1111 1111` is converted unchanged to `b`, and as a signed number it is -1.
- The value -1 is stored in `c` as -1 (see the explanation above for how).
</details>

### 16. Swapping variables
```cpp
int a { 1 };
int b { 2 };
a = b;
b = a;
std::cout << a << std::endl;
std::cout << b << std::endl;
```

<details>
<summary>Answer</summary>

At first glance, this code looks like an attempt to swap the values of `a` and `b`, so that
`a` contains `2` and `b` contains `1`.

However, `a = b` overwrites `a`, and its old value, `1`, is lost.

The correct code would be:
```cpp
int a { 1 };
int b { 2 };
// временная переменная
int temp { a };
a = b;
b = temp;
```
</details>
