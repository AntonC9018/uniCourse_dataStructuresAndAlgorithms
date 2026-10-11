---
slug: en/cpp/labs/numeric-conversions
---
<!-- course-site-backlink:start -->
[This lesson on the website](https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms/en/cpp/labs/numeric-conversions/)
<!-- course-site-backlink:end -->
# Numeric conversions

- [Video about type conversions (up to
pointers)](https://www.youtube.com/watch?v=imkDyDE7Tkw&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=28)

## Concepts

- Explicit and implicit conversions between numeric types
- `static_cast` and the type of its result
- Conversion to larger and smaller integer types
- Signedness and integer representation
- Bitwise operations (advanced)

## Comprehension questions

Explain the type and value produced by each conversion.
Run examples with defined behavior to check your reasoning.
For fragments without `main`, use the source-file wrapper from the [variables lab](02_variables.md).

### 1. `auto` and `static_cast`

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

### 2. `static_cast` to a larger type

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

### 3. `static_cast` of a negative number to a larger type

```cpp
int8_t a{ -3 };
int b{ static_cast<int>(a) };
```

<details>
<summary>Answer</summary>

Just like in the previous example, the conversion happens implicitly even without `static_cast`,
because every value stored in `a` fits in `b`.

The conversion preserves the value and therefore the sign:
since `a` is negative, the upper bits of `b` are filled with 1.
`-3` is `1111 1101` in 8 bits
and `1111 1111 1111 1111 1111 1111 1111 1101` in 32 bits.
</details>


### 4. `static_cast`
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

The same value with all 32 bits written out,
and each hexadecimal digit placed under its 4 bits:
```
0000 0000  0000 0000  0000 0001  0000 0000
0    0     0    0     0    1     0    0
```

How to read this notation: the top row holds the bits, split into groups of 4
(one group per hexadecimal digit, with a wider gap between whole bytes);
the bottom row holds the hexadecimal digit for the 4 bits directly above it.
Reading the bottom row gives `0x00000100`, which is 256.
Truncation to `uint8_t` keeps only the last byte (`0000 0000`), so the result is 0.
</details>

<details>
<summary>What happens if a different value is stored in <code>a</code>?</summary>

- Value 257: `1 0000 0001` is stored, becoming `0000 0001` after truncation.
- Value 258: `1 0000 0010` is stored, becoming `0000 0010` after truncation.
- Value 511: `1 1111 1111` is stored, becoming `1111 1111` after truncation.
- Value 512: `10 0000 0000` is stored, becoming `0000 0000` after truncation.
</details>

### 5. Bitwise operation (advanced level)
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

Written out with each hexadecimal digit under its 4 bits:
```
a:
0000 0000
0    0

b:
1111 1111
F    F

c:
0000 0000  0000 0000  0000 0000  1111 1111
0    0     0    0     0    0     F    F
```

Since `b` is unsigned, the most significant bit counts as just another positive bit,
so the upper 3 bytes of `c` are filled with 0 (zero extension):
`c` holds `0x000000FF`, and the program prints 255.
A signed type, by contrast, is going to interpret the most significant bit
as having a negative coefficient,
which is why extending a negative value fills the upper bits with 1s instead.

</details>

### 6. Changing the sign (advanced level)
```cpp
#include <cstdint>
#include <iostream>

int main()
{
    uint8_t a{ 127 };
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

- 127 is written to `a` as `0111 1111`.
- `0111 1111` is converted unchanged to `b`, and as a signed number it is 127.
- The value 127 is stored in `c` as 127 (see the explanation above for how).

Written out with each hexadecimal digit under its 4 bits:
```
a, b:
0111 1111
7    F

c:
0000 0000  0000 0000  0000 0000  0111 1111
0    0     0    0     0    0     7    F
```

Since `b` is positive, the upper 3 bytes of `c` are filled with 0:
`c` holds `0x0000007F`, so the program prints 127.
</details>
