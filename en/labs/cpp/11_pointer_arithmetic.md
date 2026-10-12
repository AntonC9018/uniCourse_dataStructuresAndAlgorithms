---
slug: en/cpp/labs/pointer-arithmetic
---
<!-- course-site-backlink:start -->
[This lesson on the website](https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms/en/cpp/labs/pointer-arithmetic/)
<!-- course-site-backlink:end -->
# Pointer arithmetic

- [Video covering the basics and providing more in-depth information](https://www.youtube.com/watch?v=9AhNOjjyAwU&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=14)

## Concepts

- What happens when you add a number to a pointer
- What subtracting two pointers yields
- UB when pointers do not point into the same memory block
- Integer representations of addresses and `reinterpret_cast`
- Field offsets
- stack

## Examples to aid understanding

For fragments without `main`, include `<array>` and `<iostream>` and place the code in `main`.

### 1. Moving a pointer by 1
```cpp
std::array<int, 2> arr{};
int* p = &arr[0];
p = p + 1;
*p = 2;

std::cout << arr[1];
std::cout << std::endl;
```

<details>
<summary>Answer</summary>

`p + 1` advances the pointer by 1 element—that is, by 1 `int`, which is typically 4 bytes.

After this code executes, `p` equals `&arr[1]`.
Reading from `*p` is equivalent to reading from `arr[1]`.
</details>

### 2. Returning the next array element address

```cpp
#include <array>
#include <iostream>

int* nextElement(int* current)
{
    return current + 1;
}

int main()
{
    std::array<int, 3> arr{ 4, 7, 9 };
    int* next{ nextElement(&arr[0]) };
    *next = 8;
    std::cout << arr[1] << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `8`.
The call returns an `int*` pointing to `arr[1]`, so writing through `next` changes that element.
The array belongs to `main` and still exists after the function returns.
The caller must ensure that a next element exists before dereferencing the returned pointer.
</details>


### 3. Accessing an array element through an expression
```cpp
std::array<int, 2> arr{};
int* p = &arr[0];
*(p + 1) = 6;

std::cout << *p << std::endl;
std::cout << arr[1] << std::endl;
```

<details>
<summary>Answer</summary>

A pointer produced by an expression can be used just like one stored in an ordinary variable.

Note that `*(p + 1)` *does not change `p`*; it creates a *temporary address offset from `p`*.
`*p` reads `0` from the first array element.
</details>

### 4. Subtracting pointers
```cpp
std::array<int, 2> arr{};
int* pStart = &arr[0];
int* p = pStart + 1;

ptrdiff_t x = p - pStart;
std::cout << x;
std::cout << std::endl;

ptrdiff_t x1 = pStart - p;
std::cout << x1;
std::cout << std::endl;
```

<details>
<summary>Answer</summary>

The `-` operator applied to two pointers gives the number of elements between them.
The result can also be negative.

The code will print 1 and then -1.
</details>

### 5. (advanced level): Subtracting addresses
```cpp
#include <cstdint>
#include <array>
#include <iostream>

int main()
{
   std::array<int, 2> arr{};
   int* a = &arr[0];
   int* b = &arr[1];
   uintptr_t a1 = reinterpret_cast<uintptr_t>(a);
   uintptr_t b1 = reinterpret_cast<uintptr_t>(b);
   ptrdiff_t x = static_cast<ptrdiff_t>(b1 - a1);

   std::cout << x;
   std::cout << std::endl;
}
```

<details>
<summary>Answer</summary>

`uintptr_t`, when available, is an unsigned integer type capable of holding a converted object pointer.
`reinterpret_cast` performs this pointer-to-integer conversion.

The operation `b1 - a1` treats the addresses as numbers.
The expression no longer retains information about the original pointer types.
Instead, it operates on the pointers' numeric values.

On implementations that map addresses to byte positions, the result is `sizeof(int)`, typically `4`.
The pointer-to-integer mapping is implementation-defined, so this numeric distance is not universally guaranteed.
</details>

### 6. Field address relative to a structure address
```cpp
#include <cstdint>
#include <iostream>

struct A
{
    int f;
};

int main()
{
    A a { };
    A* pa { &a };
    int* pf { &pa->f };
    uintptr_t fieldAddress{ reinterpret_cast<uintptr_t>(pf) };
    uintptr_t objectAddress{ reinterpret_cast<uintptr_t>(pa) };
    uintptr_t diff{ fieldAddress - objectAddress };
    std::cout << diff << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `0` on implementations where pointer-to-integer conversion preserves equal addresses.
For this simple structure, the first field and the structure have the same address.
`reinterpret_cast<uintptr_t>` converts each pointer to an integer representation of its address.
The subtraction here is integer arithmetic, not subtraction of pointers to different objects.
The pointer-to-integer mapping is implementation-defined; it does not generally guarantee byte distances.
</details>

### 7. (advanced level): Field offsets
```cpp
#include <cstddef>
#include <iostream>

struct A
{
    int a;
    int b;
};

int main()
{
    std::cout << offsetof(A, a) << std::endl;
    std::cout << offsetof(A, b) << std::endl;
}
```

<details>
<summary>Answer:</summary>

`offsetof` is evaluated at compile time and gives the byte
offset of a specified field from the beginning of a structure.

It prints `0` for `a`; the offset of `b` is typically `4` when `int` occupies 4 bytes.
The exact offset depends on the implementation and its alignment rules.
</details>

### 8. The array object and its first element (advanced)

```cpp
#include <array>
#include <cstdint>
#include <iostream>

int main()
{
    std::array<int, 2> arr{ 1, 2 };
    uintptr_t elementAddress{ reinterpret_cast<uintptr_t>(arr.data()) };
    uintptr_t arrayAddress{ reinterpret_cast<uintptr_t>(&arr) };
    uintptr_t diff{ elementAddress - arrayAddress };
    std::cout << diff << std::endl;
}
```

<details>
<summary>Answer</summary>

On common implementations it prints `0`: the first element starts at the beginning of the array object.
The standard does not require this layout for `std::array`, so this result is not a portable guarantee.
`arr.data()` has type `int*`, while `&arr` has type `std::array<int, 2>*`.
Converting them to integers permits numeric subtraction, but does not change these original pointer types.
Casting both pointers to byte pointers would not make their subtraction valid:
pointer subtraction requires pointers into the same array, or its one-past position.
</details>

### 9. Advanced level: addresses of local variables
```cpp
#include <cstdint>
#include <iostream>

uintptr_t f()
{
    int a;
    return reinterpret_cast<uintptr_t>(&a);
}

uintptr_t g()
{
    int b;
    return reinterpret_cast<uintptr_t>(&b);
}

int main()
{
    uintptr_t f1 { f() };
    uintptr_t f2 { f() };
    uintptr_t g1 { g() };

    std::cout << f1 << std::endl;
    std::cout << f2 << std::endl;
    std::cout << g1 << std::endl;
}
```

<details>
<summary>Answer</summary>

The C++ language does not guarantee this, and you should not rely on it, but
the same address will likely be printed 3 times.

This happens because memory for local variables is allocated on the stack
and is released after a function call ends.
When subsequent functions are called, their local variables
**will likely reuse memory that was allocated for local variables in an earlier function call**.
That is why the local variables in these calls will likely have the same address.
</details>

### 10. Reading past a one-element array (advanced)

```cpp
std::array<int, 1> value{ 5 };
int* p{ value.data() };
int* past{ p + 1 };
std::cout << *past << std::endl;
```

<details>
<summary>Answer</summary>

Forming the one-past pointer is valid; dereferencing it is undefined behavior.
There is no defined output to predict.
The pointer does not become valid just because another object might occupy nearby memory.
</details>

### 11. Writing past an array (advanced)

```cpp
std::array<int, 2> arr{};
int* past{ arr.data() + arr.size() };
*past = 7;
```

<details>
<summary>Answer</summary>

`past` is a valid one-past pointer, but writing through it is undefined behavior.
Only indices from zero up to `arr.size() - 1` identify elements.
There is no extra element available at the one-past address.
</details>
