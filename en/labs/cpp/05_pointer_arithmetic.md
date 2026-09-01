# Pointer arithmetic

- [Video covering the basics and providing more in-depth information](https://www.youtube.com/watch?v=9AhNOjjyAwU&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=14)

## Concepts

- What happens when you add a number to a pointer
- What subtracting two pointers yields
- UB when pointers do not point into the same memory block
- stack

## Examples to aid understanding

### 1. Moving a pointer by 1
```cpp
int arr[2]{};
int* p = arr;
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

### 2. Accessing an array element through an expression
```cpp
int arr[2]{};
int* p = arr;
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

### 3. Subtracting pointers
```cpp
int arr[2]{};
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

### 4. (advanced level): Subtracting addresses
```cpp
#include <cstdint>
#include <iostream>

int main()
{
   int arr[2]{};
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

### 5. (advanced level): Going beyond a variable's bounds
```cpp
int a = 5;
int b = 6;
int* pa = &a;
int* pb = pa + 1;

std::cout << *pb;
std::cout << std::endl;
```

<details>
<summary>Answer</summary>

Technically, this is considered UB (undefined behavior).
It might print 6, the value of variable `b`.
</details>

### 6. (advanced level): Going beyond an array's bounds
```cpp
int a[2]{};
int b = 6;
int* p = &a[2];
*p = 7;

std::cout << b;
std::cout << std::endl;
```

<details>
<summary>Answer</summary>

This is essentially the same situation as above.
Remember that going beyond an array's bounds can reach memory occupied by another variable.
Going beyond an array's bounds does not necessarily cause a runtime error in C++
and is not automatically prevented at runtime.

In this example, it might print 7.
</details>

### 7. Array assignment (1)
```cpp
int arr1[2]{ 1, 2 };
int arr2[2]{ 3, 4 };
arr1 = arr2;
```
<details>
<summary>Answer</summary>

Although it might seem that this should copy every element
from `arr2` to `arr1`, the program will not compile.
This syntax simply does not work in C++.
</details>

### 8. Array assignment (2)
```cpp
int arr1[2]{ 1, 2 };
int arr2[2]{ 3, 4 };
*arr1 = *arr2;
```
<details>
<summary>Answer</summary>

In `*arr1 = *arr2`, the array names are used as expressions.
In this case, they are treated as pointers to their first elements.
Accordingly, this overwrites `arr1[0]` with `arr2[0]`, that is, with `3`.
</details>

<!-- Missing: different pointer type -->
