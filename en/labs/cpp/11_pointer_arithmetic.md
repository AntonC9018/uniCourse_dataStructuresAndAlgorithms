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

`uintptr_t` is an integer type with the same size as an `int*` (probably 8 bytes).

The operation `b1 - a1` treats the addresses as numbers.
The expression no longer retains information about the original pointer types.
Instead, it operates on the pointers' numeric values.

The result will be 4 — the difference between the addresses in bytes.
</details>

### 6. Reading past a one-element array (advanced)

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

### 7. Writing past an array (advanced)

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
