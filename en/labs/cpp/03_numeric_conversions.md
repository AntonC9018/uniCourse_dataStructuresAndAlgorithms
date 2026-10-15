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
> When `main` is not shown, place the code in a typical source file with a `main` function:
> ```cpp
> #include <iostream>
> #include <cstdint>
>
> int main()
> {
>     // your code here
> }
> ```

### 1. `auto` and `static_cast`

```cpp
auto a{ static_cast<uint8_t>(5) };
```

<details>
<summary>Changing the type of a value</summary>

`static_cast<uint8_t>(5)` converts the value `5` to type `uint8_t`. The type in `<...>` says what to convert to; the expression in `(...)` supplies the value. `auto` then chooses `uint8_t` for `a`.
</details>

<details>
<summary>Answer</summary>

`a` has type `uint8_t` and value `5`.
</details>

### 2. A cast changes the expression type

```cpp
int value{ 7 };
double half{ static_cast<double>(value) / 2 };
int integerHalf{ value / 2 };
std::cout << value << std::endl;
std::cout << half << std::endl;
std::cout << integerHalf << std::endl;
```

<details>
<summary>Dividing whole numbers or fractional numbers</summary>

Converting `value` to `double` gives `7.0` for the first division, so dividing by `2` gives `3.5`. It does not change `value` itself. In `value / 2`, both numbers are still integers, so the fractional part is discarded and the result is `3`.
</details>

<details>
<summary>Answer</summary>

Prints `7`, `3.5`, and `3` on separate lines.
</details>

<details>
<summary>Why the second number becomes double too</summary>

When one side of this division is a `double`, C++ converts the other side to `double` too. Here the first division works like `7.0 / 2.0`.
</details>

### 3. `static_cast` to a larger type

```cpp
uint8_t a{ 5 };
int b{ static_cast<int>(a) };
```

<details>
<summary>Converting to a type with more room</summary>

Every `uint8_t` value fits in `int`, so this conversion keeps the number unchanged. Here `b` gets the same `5` as `a`. You could also write `int b{ a };`: the compiler would do the conversion automatically.
</details>

<details>
<summary>Answer</summary>

`b` has type `int` and value `5`.
</details>

### 4. `static_cast` of a negative number to a larger type

```cpp
int8_t a{ -3 };
int b{ static_cast<int>(a) };
```

<details>
<summary>Keeping a negative value</summary>

An `int` can store every `int8_t` value, including negative ones. Converting `a` keeps its value `-3`; giving the number more bits does not change its sign.
</details>

<details>
<summary>Answer</summary>

`b` has type `int` and value `-3`.
</details>

<details>
<summary>How the bits keep a negative number</summary>

For a negative number, the added upper bits are filled with `1`. For example, `-3` is `1111 1101` in 8 bits and `1111 1111 1111 1111 1111 1111 1111 1101` in 32 bits.
</details>

### 5. `static_cast`
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
<summary>Keeping only eight bits</summary>

`uint8_t` can store values from `0` to `255`. Converting a larger number to it keeps only the lowest 8 bits. Here `256` is `1 0000 0000` in binary. Keeping the last 8 bits leaves `0000 0000`, which is `0`. Copying that into `c` does not change it.
</details>

<details>
<summary>Answer</summary>

Prints `0`.
</details>

<details>
<summary>What happens if a different value is stored in <code>a</code>?</summary>

- Value 257: `1 0000 0001` is stored, becoming `0000 0001` after truncation.
- Value 258: `1 0000 0010` is stored, becoming `0000 0010` after truncation.
- Value 511: `1 1111 1111` is stored, becoming `1111 1111` after truncation.
- Value 512: `10 0000 0000` is stored, becoming `0000 0000` after truncation.
</details>

<details>
<summary>What if you leave out the cast?</summary>

`uint8_t b{ a };` is rejected because the value might not fit. Writing `static_cast<uint8_t>(a)` explicitly tells the compiler to perform the conversion even if some bits are lost.
</details>

### 6. Bitwise operation (advanced level)
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
<summary>Flipping bits</summary>

`~` changes each `0` bit to `1` and each `1` to `0`. For example, `1010 0011` becomes `0101 1100`. There is a catch: C++ first converts the small `uint8_t` value to `int`, so `~a` is an `int`, not an 8-bit value. The braces in `uint8_t b{ ~a };` reject that conversion back to eight bits.
</details>

<details>
<summary>Answer</summary>

Does not compile as standard C++: the conversion in `uint8_t b{ ~a };` is not allowed.
</details>

<details>
<summary>How to keep the eight flipped bits</summary>

Ask explicitly for the conversion back to `uint8_t`:
```cpp
uint8_t b{ static_cast<uint8_t>(~a) };
```
The lowest 8 bits are then `1111 1111`, or `255`. With this change, the program prints `255`.
</details>

### 7. Changing the sign (advanced level)
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
<summary>Converting between unsigned and signed values</summary>

`uint8_t` stores numbers from `0` to `255`; `int8_t` stores numbers from `-128` to `127`. The value `127` fits in both, so converting it keeps the value. Copying it into the larger `int32_t` also keeps `127`.
</details>

<details>
<summary>Answer</summary>

Prints `127`.
</details>

<details>
<summary>What happens with other values?</summary>

In C++20 and later, converting `128` (`1000 0000`) to `int8_t` gives `-128`: the same bits represent a negative number in the signed type. Before C++20, the result of such an out-of-range conversion depends on the compiler. A value that fits, such as `127` here, stays unchanged.
</details>
