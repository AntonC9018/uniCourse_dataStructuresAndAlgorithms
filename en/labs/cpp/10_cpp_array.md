---
slug: en/cpp/labs/cpp-array
---
<!-- course-site-backlink:start -->
[This lesson on the website](https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms/en/cpp/labs/cpp-array/)
<!-- course-site-backlink:end -->
# C++ arrays (`std::array`)

- [Information](../../../en/06_arrays/doc.md)

## Concepts

- The advantage of C++ arrays over C arrays
- Copying and initializing arrays
- Indexing C++ arrays
- `data`
- Obtaining addresses of array elements
- Data types other than `int` for array elements


## Examples

For fragments without `main`, include `<array>` and `<iostream>` and place the code in `main`.

### 1. Obtaining the address of the first element

```cpp
std::array<int, 2> arr{ 1, 2 };
int* p{ arr.data() };
*p = 3;
std::cout << arr[0] << std::endl;
std::cout << arr[1] << std::endl;
```

<details>
<summary>Answer</summary>

`arr.data()` returns a pointer to the first element, like `&arr[0]`.
Writing through that pointer changes the element.
It prints `3` and `2`.
</details>

### 2. The number of elements

```cpp
std::array<int, 3> arr{ 4, 7, 9 };
std::cout << arr.size() << std::endl;
```

<details>
<summary>Answer</summary>

It prints `3`.
`arr.size()` returns the number of elements, not the number of bytes.
Here that is the size argument in `std::array<int, 3>`.
</details>

### 3. Initializing C++ arrays (1)
```cpp
std::array<int, 2> arr{ 1, 2 };
std::array<int, 2> other{ 3, 4 };
arr = other;
```

<details>
<summary>Answer</summary>

Here, each element is copied from `other` into `arr`.
</details>

### 4. Initializing C++ arrays (2)
```cpp
std::array<int, 2> arr{ 1, 2 };
std::array<int, 2> other{ arr };
```

<details>
<summary>Answer</summary>

The same copying occurs here, when `other` is created.
</details>

### 5. Address of an array
```cpp
std::array<int, 2> arr{ 1, 2 };
std::array<int, 2>* p{ &arr };
*p = { 3, 4 };
std::cout << arr[0] << std::endl;
std::cout << arr[1] << std::endl;
```

<details>
<summary>Answer</summary>

`p` will contain the address of the beginning of the entire array object.
The array object covers all of its elements.

Here, the original elements are overwritten with `3, 4`.
</details>

### 6. Dereferencing an array address
```cpp
std::array<int, 2> arr{ 1, 2 };
std::array<int, 2>* p{ &arr };
std::array<int, 2> arr1{ *p };
arr1[0] = 3;
arr1[1] = 4;
std::cout << arr[0] << std::endl;
std::cout << arr[1] << std::endl;
```

<details>
<summary>Answer</summary>

`p` points to an object of type `std::array<int, 2>`, and the expression `*p` gives a value
of type `std::array<int, 2>`, so `arr1` receives a copy of the entire array.

Since `arr1` is a copy, its changes will not affect `arr`.
</details>

### 7. Indexing elements through an address
```cpp
std::array<int, 2> arr{ 1, 2 };
std::array<int, 2>* p{ &arr };
(*p)[0] = 3;
(*p)[1] = 4;
std::cout << arr[0] << std::endl;
std::cout << arr[1] << std::endl;
```

<details>
<summary>Answer</summary>

`*p` accesses the original array object.
`(*p)[0]` and `(*p)[1]` access its elements, so the assignments change `arr`.
It prints `3` and `4`.
</details>

### 8. The array object and its first element

```cpp
std::array<int, 2> arr{ 1, 2 };
std::cout << arr.data() << std::endl;
std::cout << &arr << std::endl;
```

<details>
<summary>Answer</summary>

`arr.data()` has type `int*`; `&arr` has type `std::array<int, 2>*`.
Both lines print addresses.
Even if the printed addresses match on your implementation, the pointer types are different.
Use `arr.data()` or `&arr[0]` when an element pointer is required.
</details>

### 9. Matrices (two-dimensional arrays)
```cpp
std::array<std::array<int, 2>, 3> arr{
    std::array{ 1, 2 },
    { 3, 4 },
    { 5, 6 },
};
std::array<int, 2> firstRow { arr[0] };
std::array<int, 2> lastRow { arr[2] };
arr[0][0] = 7;
arr[2][1] = 8;
arr[1] = { 9, 10 };
```

<details>
<summary>Answer</summary>

This illustrates an array whose element type is another array rather than `int`.
Each array element therefore effectively stores two ints.

> In the initialization of `arr`, you need to specify `std::array`
> because otherwise the compiler cannot determine the element type from the initialization.
> It needs a little help.
>
> You do not need to understand this mechanism yet.
</details>

<details>
<summary>Can a user-defined type be used as an array element?</summary>

Yes. Try defining a type, for example:
```cpp
struct Item
{
    int f1;
    int f2;
};
```

And use it as the element type, like this:
```cpp
std::array<Item, 3> arr{
    Item{ 1, 2 },
    { 3, 4 },
    { 5, 6 },
};
```
</details>


## Structures and arrays

### 1. An array field of addresses
```cpp
#include <iostream>
#include <array>

struct A
{
    std::array<int*, 2> f;
};

int main()
{
    int var1;
    int var2;
    A a { .f = { &var1, &var2 } };
    *a.f[0] = 1;
    *a.f[1] = 2;
    int** b = a.f.data();
    int c = **b;

    std::cout << var1 << std::endl;
    std::cout << var2 << std::endl;

    std::cout << a.f[0] << std::endl;
    std::cout << a.f[1] << std::endl;

    std::cout << b << std::endl;
    std::cout << c << std::endl;
}
```

<details>
<summary>Answer:</summary>

The line `A a { .f = { &var1, &var2 } };` initializes `a`,
putting the address of `var1` into field `a.f[0]` and the address of `var2` into `a.f[1]`.

In the line `*a.f[0] = ...`, execution follows the address stored in `a.f[0]`:
`*a.f[0]` -> `*(a.f[0])` -> `*(&var1)` -> `var1`.

In `int** b = a.f.data();`, `.data()` returns `&(a.f[0])`, with type `int**`.
This gives the address of the first element in array `f` in `a`.

It prints:
- `1`, `2` as the values of `var1` and `var2`;
- the addresses of `var1` and `var2` as the values of `a.f[0]` and `a.f[1]`;
- `c` is equal to `1`.

</details>

### 2. Structure size (2)
```cpp
#include <iostream>
#include <array>

struct A
{
    std::array<int, 4> f1;
    int* f2;
};

int main()
{
    std::cout << sizeof(A) << std::endl;
}
```

<details>
<summary>Answer:</summary>

- `std::array<int, 4> f1` is 4 `int`s, 4 bytes each — 16 bytes;
- `int* f2` is 8 bytes on a 64-bit processor.

The total is 24 bytes.
</details>

### 3. Initializing an array field
```cpp
#include <iostream>
#include <array>

struct A
{
    std::array<int, 2> arr;
};

int main()
{
    A a { { 1, 2 } };
    A b { { 3, 4 } };
    b = a;

    std::cout << b.arr[0] << std::endl;
    std::cout << b.arr[1] << std::endl;
}
```

<details>
<summary>Answer:</summary>

It prints `1`, `2`.
</details>

### 4. Copying a structure with an array field
```cpp
#include <iostream>
#include <array>

struct A
{
    std::array<int, 2> arr;
};

int main()
{
    A a { { 1, 2 } };
    A b { a };

    a.arr[0] = 3;

    std::cout << b.arr[0] << std::endl;
    std::cout << b.arr[1] << std::endl;
    std::cout << a.arr[0] << std::endl;
    std::cout << a.arr[1] << std::endl;
}
```

<details>
<summary>Answer:</summary>

`A b{ a }` copies the values of *all fields*, including the whole array, element by element.

At the moment of copying, `a` holds `arr[0] = 1`, `arr[1] = 2`,
so `b` receives the same values: `b.arr[0] = 1`, `b.arr[1] = 2`.
But it is a separate copy in `b`'s own memory: the array `arr` itself
is stored inside `A` by value, not by address.

So `a.arr[0] = 3` affects only `a`, while `b` stays untouched.

It prints `1`, `2`, `3`, `2`.
</details>

### 5. An array of structures
```cpp
#include <iostream>
#include <array>

struct A
{
    int f1;
    int f2;
};

int main()
{
    std::array<A, 3> arr{};

    arr[0].f2 = 1;

    arr[1] = A{ 2, 3 };

    A copy { arr[2] };
    copy.f1 = 4;
    copy.f2 = 5;

    std::cout << arr[0].f1 << std::endl;
    std::cout << arr[0].f2 << std::endl;
    std::cout << arr[1].f1 << std::endl;
    std::cout << arr[1].f2 << std::endl;
    std::cout << arr[2].f1 << std::endl;
    std::cout << arr[2].f2 << std::endl;
}
```

<details>
<summary>Answer:</summary>

The line `std::array<A, 3> arr{};`:
- Defines an array of three variables of type `A`.
 In total, memory is allocated for 6 `int`s.
- The braces mean “initialize with zeros”.
 Each array element is filled with the default `A`, namely `A{}`,
 which means all 6 `int`s become zero.

In `arr[0].f2 = 1;`, `arr[0]` accesses the memory of
the first variable in the array.
This variable has type `A` (not `int`! It is very important to understand this).
Its second field (`.f2`) is assigned `1` (`= 1`).

`arr[1] = A{ 2, 3 };` overwrites the entire second element
with the result of expression `A{ 2, 3 }`.
This overwrites both fields.

`A copy { arr[2] };` reads the third element of the array,
copying what is there into temporary variable `copy`.
`copy` holds a copy of the value from `arr[2]` of type `A` (that is, it has a copy of all fields).
Therefore, subsequent changes to `copy` do not affect `arr[2]`.

```
0
1
2
3
0
0
```
</details>
