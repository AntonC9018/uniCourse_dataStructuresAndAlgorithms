---
slug: en/cpp/labs/const
---
<!-- course-site-backlink:start -->
[This lesson on the website](https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms/en/cpp/labs/const/)
<!-- course-site-backlink:end -->
# `const`

## Concepts

- Const variables and structure objects
- Copying a const value into a non-const object
- Const references: reading, observing changes, and copying values
- Const function parameters: passing by value and by reference
- Reading through a pointer to const, reassigning the pointer, and observing changes
- Why copying an address does not remove the pointed-to `const`
- Const C-array elements
- Compile-time array sizes: `const int` and `constexpr` structures

## Comprehension questions

For each example, predict whether it compiles. If it does, what does it print?
Which objects can be changed, and through which expressions?

Unless `main` is shown, place the snippet inside `main`. For all examples, include `<iostream>` before the code:

```cpp
#include <iostream>

int main()
{
    // snippet here
}
```

### 1. Reassigning a const variable

```cpp
const int a = 5;
a = 6;
std::cout << a << std::endl;
```

<details>
<summary>Answer</summary>

The program will not compile: `a = 6` tries to change a const object.
Initialization gives `a` its value, but subsequent assignments are forbidden.
Without the assignment, it prints `5`.
</details>

### 2. Copying a const integer

```cpp
const int a = 5;
int b = a;
b = 6;
std::cout << a << std::endl;
std::cout << b << std::endl;
```

<details>
<summary>Answer</summary>

It prints `5` and `6`.
`b` is a separate, non-const object initialized with a copy of the value of `a`.
Reading a const object is allowed; changing the copy does not change the original.
</details>

### 3. A const structure object

```cpp
struct Position
{
    int x;
    int y;
};

int main()
{
    const Position a{ 1, 2 };
    a.x = 3;
    std::cout << a.x << std::endl;
}
```

<details>
<summary>Answer</summary>

The program will not compile: `a.x = 3` tries to change a field of the const object `a`.
The fields are ordinary `int` fields; it is this particular `Position` object that is const.
Without the assignment, it prints `1`.
</details>

### 4. Copying a const structure

```cpp
struct Position
{
    int x;
    int y;
};

int main()
{
    const Position a{ 1, 2 };
    Position b = a;
    b.x = 3;
    std::cout << a.x << std::endl;
    std::cout << b.x << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `1` and `3`.
As with `int`, copying a const object into a non-const object is allowed.
The field values are copied into `b`; `b.x` is a different object from `a.x`.
</details>

### 5. Writing through a const reference

```cpp
const int a = 5;
const int& r = a;
r = 6;
std::cout << r << std::endl;
```

<details>
<summary>Answer</summary>

The program will not compile: `r = 6` tries to change `a` through a const reference.
`r` refers to the existing object `a`; it does not hold a copy of its value.
A `const int&` can refer to a const integer, but only reading through it is allowed.
Without the assignment, it prints `5`.
</details>

### 6. Observing a change through a const reference

```cpp
int a = 5;
const int& r = a;
std::cout << r << std::endl;
a = 6;
std::cout << r << std::endl;
```

<details>
<summary>Answer</summary>

It prints `5` and `6`.
A const reference can also refer to a non-const object.
`a` can still be changed directly, and `r` reads the current value of that same object.
The restriction applies to writes through `r`; it does not freeze `a`.
</details>

### 7. Copying a value read through a const reference

```cpp
int a = 5;
const int& r = a;
int b = r;
b = 6;
a = 7;
std::cout << r << std::endl;
std::cout << b << std::endl;
```

<details>
<summary>Answer</summary>

It prints `7` and `6`.
`int b = r` copies the value read through `r` into a separate, non-const object.
Changing `b` does not change `a`, and changing `a` does not change `b`.
The reference `r` continues to refer to `a`.
</details>

### 8. A non-const reference from a const reference

```cpp
int a = 5;
const int& r = a;
int& other = r;
other = 6;
```

<details>
<summary>Answer</summary>

The program will not compile at `int& other = r`.
A non-const reference cannot bind to the object through a const reference by discarding `const`.
Unlike `int b = r`, this would not create a separate integer:
`other` would refer to the same object and allow writes to it.
The rule applies even though this particular `a` is non-const.
Use `const int& other = r` to keep the restriction; then `other = 6` is also forbidden.
</details>

### 9. Structure fields through a const reference

```cpp
struct Position
{
    int x;
    int y;
};

int main()
{
    Position a{ 1, 2 };
    const Position& r = a;
    r.x = 3;
    std::cout << r.x << std::endl;
}
```

<details>
<summary>Answer</summary>

The program will not compile: `r.x = 3` tries to change an integer field through a const reference.
The same read-only access rule applies to a whole structure.
`a.x = 3` would be allowed because `a` itself is non-const.
Without the assignment, it prints `1`.
</details>

### 10. A const value parameter

```cpp
void func(const int a)
{
    a = 6;
}

int main()
{
    int a = 5;
    func(a);
}
```

<details>
<summary>Answer</summary>

The program will not compile: the parameter `a` inside `func` is const.
The argument would be copied into this separate parameter object.
`const` on the parameter restricts changes to that copy; it does not make the caller's variable const.
The same rule applies to a structure passed by value as `const Position a`.
</details>

### 11. A const argument and a non-const parameter

```cpp
void func(int a)
{
    a = 6;
    std::cout << a << std::endl;
}

int main()
{
    const int a = 5;
    func(a);
    std::cout << a << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `6` and `5`.
The const argument is copied into the ordinary `int` parameter.
Only that local copy changes, just as in the earlier integer-copy example.
</details>

### 12. Passing a const structure by value

```cpp
struct Position
{
    int x;
    int y;
};

void func(Position a)
{
    a.x = 3;
    std::cout << a.x << std::endl;
}

int main()
{
    const Position a{ 1, 2 };
    func(a);
    std::cout << a.x << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `3` and `1`.
This combines structure copying with passing by value.
The parameter is a non-const copy, so changing its field is allowed and leaves the original unchanged.
</details>

### 13. A const reference parameter

```cpp
struct Position
{
    int x;
    int y;
};

int readX(const Position& a)
{
    return a.x;
}

int main()
{
    Position a{ 1, 2 };
    const Position b{ 3, 4 };
    std::cout << readX(a) << std::endl;
    a.x = 5;
    std::cout << readX(a) << std::endl;
    std::cout << readX(b) << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `1`, `5`, and `3`.
The [references lab](12_reference.md) used `increasePower(Arm&)` to change the caller's object.
Adding `const` keeps the reference to the original object but restricts access through the parameter to reading.
No `Position` object is copied when passing either argument.

Both const and non-const objects can be passed to `const Position&`.
The second call reads the updated `a.x`, while adding `a.x = 6` inside `readX` would cause a compilation error.
A by-value parameter `Position a` would instead make a separate, mutable copy, as in the previous example.
</details>

### 14. A pointer to const

```cpp
int a = 5;
const int* p = &a;
*p = 6;
std::cout << *p << std::endl;
```

<details>
<summary>Answer</summary>

The program will not compile: `*p = 6` tries to write through a pointer to const.
`const int*` allows reading the pointed-to integer, but not changing it through `p`.
Without the assignment, it prints `5`.
</details>

### 15. Reassigning a pointer to const

```cpp
int a = 5;
int b = 6;
const int* p = &a;
p = &b;
std::cout << *p << std::endl;
```

<details>
<summary>Answer</summary>

It prints `6`.
The object accessed through `p` is read-only through that pointer, but `p` itself can change.
Assigning `&b` changes the stored address; it does not overwrite either integer.
</details>

<details>
<summary>Where does <code>const</code> go?</summary>

`const int* p` and `int const* p` mean the same thing: a pointer to const `int`.
Here, `const` applies to the pointed-to object.

In `int* const p = &a`, `const` applies to the pointer variable instead:
`p = &b` is forbidden, but `*p = 6` is allowed if `a` is non-const.
`const int* const p = &a` restricts both.

In this lab, the main focus is `const T*`: reading an object through a pointer.
</details>

### 16. Accessing structure fields through a pointer to const

```cpp
struct Position
{
    int x;
    int y;
};

int main()
{
    Position a{ 1, 2 };
    const Position* p = &a;
    p->x = 3;
    std::cout << p->x << std::endl;
}
```

<details>
<summary>Answer</summary>

The program will not compile: `p->x = 3` attempts to change the object through `const Position*`.
Both integer fields can be read through `p`, but neither can be changed through it.
Without the assignment, it prints `1`.
</details>

### 17. Observing a change through a pointer to const

```cpp
struct Position
{
    int x;
    int y;
};

int main()
{
    Position a{ 1, 2 };
    const Position* p = &a;
    std::cout << p->x << std::endl;
    a.x = 3;
    std::cout << p->x << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `1` and `3`.
`a` is still a non-const object and can be changed directly.
The pointer does not store a frozen copy of `a`; each read accesses the same object's current field value.
`const Position*` restricts this access path, not every possible way of accessing `a`.
</details>

### 18. Copying an address does not copy the object

```cpp
struct Position
{
    int x;
    int y;
};

int main()
{
    Position a{ 1, 2 };
    const Position* p = &a;
    Position* q = p;
    q->x = 3;
}
```

<details>
<summary>Answer</summary>

The program will not compile at `Position* q = p`.
An ordinary pointer cannot be initialized from a pointer to const by discarding the pointed-to `const`.

Unlike `Position b = a`, copying a pointer copies an address, not the `Position` object.
Allowing this conversion would allow writes to the same object through `q`.
Use `const Position* q = p` to keep the restriction; then `q->x = 3` is also forbidden.
This conversion is forbidden even though this particular `a` is non-const.
</details>

### 19. Copying the value read through a pointer to const

```cpp
struct Position
{
    int x;
    int y;
};

int main()
{
    const Position a{ 1, 2 };
    const Position* p = &a;
    Position b = *p;
    b.x = 3;
    std::cout << p->x << std::endl;
    std::cout << b.x << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `1` and `3`.
`Position b = *p` reads and copies the whole object, rather than copying its address.
The new object `b` is non-const, so its fields can be changed.
This combines reading through a pointer with the earlier structure-copy rule.
</details>

### 20. A pointer-to-const parameter

```cpp
struct Position
{
    int x;
    int y;
};

int readX(const Position* p)
{
    return p->x;
}

int main()
{
    Position a{ 1, 2 };
    const Position b{ 3, 4 };
    std::cout << readX(&a) << std::endl;
    std::cout << readX(&b) << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `1` and `3`.
The function receives a copy of an address, not a copy of the structure.
It can read the original object but cannot change its integer fields through `p`.
Adding `p->x = 5` inside `readX` would cause a compilation error.
Both non-const and const objects can be passed to a parameter of type `const Position*`.
The local pointer parameter itself can still be reassigned, as in the earlier pointer example.
</details>

### 21. A const C array

```cpp
const int arr[2]{ 1, 2 };
arr[0] = 3;
std::cout << arr[0] << std::endl;
```

<details>
<summary>Answer</summary>

The program will not compile: the elements of `arr` are const integers.
They can be read, but `arr[0] = 3` attempts to change one of them.
Without the assignment, it prints `1`.
</details>

### 22. Reading an array through a pointer to const

```cpp
int arr[2]{ 1, 2 };
const int* p = &arr[0];
arr[0] = 3;
std::cout << p[0] << std::endl;
p += 1;
std::cout << *p << std::endl;
```

<details>
<summary>Answer</summary>

It prints `3` and `2`.
The C array supplies the address of its first element.
`p[0]` reads the current value of `arr[0]`, which was changed directly.
The pointer can advance to the next element, but neither `p[0] = 4` nor `*p = 4` is allowed.
This combines array access and pointer arithmetic with read-only access through a pointer.
</details>

### 23. Const integers as array sizes

```cpp
const int globalSize = 2;

int main()
{
    const int localSize = 3;
    int a[globalSize]{ 1, 2 };
    int b[localSize]{ 3, 4, 5 };
    std::cout << a[1] << std::endl;
    std::cout << b[2] << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `2` and `5`.
Both sizes are const integers initialized with constant expressions, so their values can be used at compile time.
Being global is not required: the local `localSize` works too.
Here, “size known at compile time” describes the array bound, not the `static` storage keyword.
</details>

### 24. Const does not always mean known at compile time

```cpp
int input = 0;
std::cin >> input;
const int size = input;
int arr[size]{};
```

<details>
<summary>Answer</summary>

In standard C++, the program will not compile at `int arr[size]{}`.
`size` cannot be reassigned, but its value comes from user input and is not a constant expression.
The compiler needs a compile-time bound for this C array.
Some compilers accept variable-length arrays as an extension; that is not standard C++.
</details>

### 25. A constexpr structure and an array size

```cpp
struct Sizes
{
    int count;
};

int main()
{
    constexpr Sizes sizes{ 3 };
    int arr[sizes.count]{ 1, 2, 3 };
    std::cout << arr[2] << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `3`.
A `constexpr` variable must be initialized with a constant expression and is also const.
Here, the whole `Sizes` object is initialized at compile time, so reading `sizes.count` is valid as an array bound.

For the earlier `const int localSize = 3`, `constexpr` was not needed to use the value as a bound.
For this structure, writing only `const Sizes sizes{ 3 }` would
not make `sizes.count` a constant expression usable as a bound.
`constexpr` explicitly provides that guarantee for this object.

The [C++ array lab](14_cpp_array.md) uses the same idea for the size argument in `std::array<int, sizes.count>`.
</details>
