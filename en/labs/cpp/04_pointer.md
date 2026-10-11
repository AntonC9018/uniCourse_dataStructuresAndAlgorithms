---
slug: en/cpp/labs/pointer
---
<!-- course-site-backlink:start -->
[This lesson on the website](https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms/en/cpp/labs/pointer/)
<!-- course-site-backlink:end -->
# Pointers

- [Video about pointers](https://www.youtube.com/watch?v=859Y0Q8pyLg&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=8)
- [Video covering the basics, with more in-depth
information](https://www.youtube.com/watch?v=9AhNOjjyAwU&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=14)

## Concepts

- Memory address
- Pointer
- Pointer type notation
- Getting the address of a variable
- Writing to and reading from an address using dereference (dereferencing)
- Pointer size vs. the size of what it points to
- Why pointers with different element sizes are incompatible

## Exercises for understanding

Explain what will happen in the following code snippets.
Also run the snippets to verify that your reasoning is correct.

> When `main` is not shown, place the code in a typical `main` file:
> ```cpp
> #include <iostream>
> #include <cstdint>
>
> int main()
> {
>     // your code here
> }
> ```


### 1. Variable address
```cpp
int a{ 5 };
int* b{ &a }; // int* b = &a;
std::cout << b;
std::cout << std::endl;
```

<details>
<summary>Answer:</summary>

`int* b{ &a }` stores the address of the variable `a` in `b`.
Next, the *address* stored in `b` is printed.
It is not the value at the address stored in `b` (that would be written as `*b`), but the address itself.
</details>

<details>
<summary>What is the type of variable <code>b</code>?</summary>

Variable-definition syntax consists of:
1. a type;
2. a variable name;
3. optionally, an initialization.

`int* b{ &a };` — here:
1. `int*` is the type;
2. `b` is the variable name;
3. `{ &a }` is the initialization.

**The type of `b` is not `int`, but `int*`!**
</details>

<details>
<summary>What is the type of expression <code>&a</code>?</summary>

`&` is an operator that obtains the *address of a variable*.
`&` applies **not to the value of `a`, but to the variable `a` itself**.

The type of `&a` is `int*`.
At compile time, this type indicates
that **the resulting address is specifically the address of a variable of type `int`,
and not of some other type**.

> `&` can give the address of *any object*, but that will be covered in lab 3.
</details>

### 2. Address of an uninitialized variable

Is something like this allowed?

```cpp
int a;
int* b{ &a };
std::cout << b;
std::cout << std::endl;
```

<details>
<summary>Answer:</summary>

You can take the address of an uninitialized variable.
It will be printed as an ordinary address.

*Reading the value at* that address would not be allowed.
</details>

### 3. Dereference operator (writing)
```cpp
int a { 1 };
int* b{ &a };
*b = 2;
std::cout << a;
std::cout << std::endl;
```

<details>
<summary>Answer:</summary>

The address of the variable `a` was stored in `b`.

In the line `*b = 2`, `*b` lets us refer to the variable
located at the address in `b`, that is, to `a`.

`*b = 2` -> `a = 2` writes `2` into `a`.
</details>

### 4. A number as an address

Is something like this allowed?

```cpp
int* b{ 32 };
std::cout << *b;
std::cout << std::endl;
```

<details>
<summary>Answer:</summary>

No. An address cannot be set directly like this; it must be obtained using
the `&` operator on an object (for example, a variable).
</details>

### 5. Dereference operator (reading)
```cpp
int a{ 5 };
int b{ *(&a) };
std::cout << b;
std::cout << std::endl;
```

<details>
<summary>Correct answer:</summary>

Evaluating the expression `*(&a)`:
- `&a` becomes the address of variable `a` (say, 32).
- `*32` follows the address, allowing access to variable `a`.
- When `a` is used as an expression, it yields the value 5.

`*(&a)` -> `*32` -> `a` -> `5`
</details>

### 6. Printing a complex expression
```cpp
int a{ 5 };
int* b{ &a };
std::cout << (*b) + 7;
std::cout << std::endl;
```

<details>
<summary>Correct answer:</summary>

`(*b) + 7` is an expression. It is evaluated in parts:
- `(*b)` means following the address in `b` and treating the result as the variable `a`.
- `(*b) + 7` -> `a + 7`; `a` is replaced with the value in `a` because it is used as an expression.
- `5 + 7` -> `12`.
</details>

### 7. Pointer to a larger data type
```cpp
uint8_t a{ 5 };
int* b{ &a };
```

<details>
<summary>Correct answer:</summary>

Compilation error (see the video about pointers)
</details>

### 8. Pointer to a smaller data type
```cpp
int a = 5;
uint8_t* b = &a;
```

<details>
<summary>Correct answer:</summary>

Compilation error (see the video about pointers)
</details>

### 9. Dependence of the address on the value

Will `b` and `c` contain the same address?
```cpp
int a = 5;
int* b = &a;
a = 6;
int* c = &a;
```

<details>
<summary>Correct answer:</summary>

They will contain the same address.

Variables *never change their address*.
`a = 6` writes 6 into the existing memory cell.
It does not redirect `a` to another cell.

`&a` takes the address of cell `a`, not the value in it.
It will always give the same address, regardless of
which value is stored in `a`.
</details>


### 10. It is the same memory!
```cpp
int a = 5;
int* ap = &a;

*ap = 6;
std::cout << a;
std::cout << std::endl;

a = 7;
std::cout << *ap;
std::cout << std::endl;
```

<details>
<summary>Answer:</summary>

Both reads and writes occur at the same address.
`ap` contains the address of variable `a`.
Writing to or reading from `*ap` is equivalent to working with `a` directly.
</details>

### 11. Assigning a value through a pointer

Is something like this allowed?
```cpp
int a;
int* b = &a;
*b = 5;
std::cout << a;
std::cout << std::endl;
```

<details>
<summary>Answer:</summary>

A value can be assigned to an uninitialized variable through a pointer.
This is allowed.
</details>

### 12. Reassigning a pointer
```cpp
int a = 5;

int* p = &a;
*p = 6;

int b = 7;

p = &b;
*p = 8;

std::cout << a;
std::cout << std::endl;

std::cout << b;
std::cout << std::endl;
```

<details>
<summary>Answer:</summary>

On the line `p = &b`, the *address* in `p` itself is overwritten with the address of another variable (`b`).

`*p = 8` now writes 8 into `b`.

</details>

### 13. Double pointer
```cpp
int a = 5;
int b = 6;
int* p = &a;
int** pp = &p;
**pp = 7;
        
*pp = &b;
**pp = 8;

std::cout << a;
std::cout << std::endl;

std::cout << b;
std::cout << std::endl;
```

<details>
<summary>Answer</summary>
 
```cpp
int a = 5; // say, address = 32
int b = 6; // say, address = 36
int* p = &a; // address of p = 40, address stored in p = 32
int** pp = &p; // address stored in pp = 40
**pp = 7; // *(*pp) --> *(40) --> *(p) --> *32 --> a
         // so a = 7
*pp = &b; // address stored in p = 36
**pp = 8; // *(*pp) --> *(40) --> *(p) --> *36 --> b
         // so b = 8

std::cout << a;
std::cout << std::endl;

std::cout << b;
std::cout << std::endl;
```
</details>

### 14. auto from an address

```cpp
int value{ 5 };
auto p{ &value };
*p = 8;
std::cout << value << std::endl;
```

<details>
<summary>Answer</summary>

`&value` has type `int*`, so `p` has type `int*`.
It prints `8`: writing through the inferred pointer changes `value`.
</details>

### 15. auto from a pointer and its value

```cpp
int value{ 5 };
int* p{ &value };
auto copiedPointer{ p };
auto copiedValue{ *p };
*copiedPointer = 8;
std::cout << value << std::endl;
std::cout << copiedValue << std::endl;
```

<details>
<summary>Answer</summary>

`p` has type `int*`; `*p` has type `int`.
Thus `copiedPointer` points to the same variable, while `copiedValue` is an independent integer copy.
It prints `8` and `5`.
</details>

### 16. auto from the address of a pointer

```cpp
int value{ 5 };
int* p{ &value };
auto pp{ &p };
**pp = 9;
std::cout << value << std::endl;
```

<details>
<summary>Answer</summary>

`&p` has type `int**`, so `pp` has type `int**`.
`*pp` accesses `p`; `**pp` accesses `value`.
It prints `9`.
</details>

### 17. Pointer sizes
```cpp
int a = 7;
int* pa = &a;
void* voidp = pa;

uint8_t c = 9;
uint8_t* pc = &c;

std::cout << sizeof(pa);
std::cout << std::endl;

std::cout << sizeof(voidp);
std::cout << std::endl;

std::cout << sizeof(pc);
std::cout << std::endl;
```

<details>
<summary>Answer</summary>

Pointers of any type have the same size because they only store memory addresses.

On 64-bit systems, any pointer is 64 bits in size (you are most likely on a 64-bit system).
</details>

### 18. Pointer and variable sizes

```cpp
int a = 7;
int* ap = &a;

std::cout << sizeof(a);
std::cout << std::endl;

std::cout << sizeof(ap);
std::cout << std::endl;

std::cout << sizeof(*ap);
std::cout << std::endl;
```


<details>
<summary>Answer</summary>

`sizeof(a)` is the same as `sizeof(int)`, 4.

`sizeof(ap)` is the same as `sizeof(int*)`, 8.

`sizeof(*ap)` does not evaluate the expression `*ap`; it only determines the type of its result.
The expression `*ap` has type `int`, so `sizeof(int)`, which is 4, is calculated.
</details>

### 19. Pointer to itself
```cpp
void* p = nullptr;
p = static_cast<void*>(&p);

std::cout << p;
std::cout << std::endl;

std::cout << &p;
std::cout << std::endl;
```

<details>
<summary>Answer</summary>

`&p` takes the address of the variable `p` itself.
The type of the expression `&p` is `void**` (the address of a variable of type `void*`).

The `static_cast<void*>(...)` explicitly converts this `void**` to `void*`,
that is, to the type of the variable `p` itself.
So the assignment `p = static_cast<void*>(&p)` stores
the address of `p` itself in `p` — now `p` points to itself.

Two identical addresses are printed: the value stored in `p` matches the address `&p`.

If the `static_cast<void*>` is omitted, the conversion from `void**` to `void*` still happens implicitly.
</details>

### 20. Empty pointer initialization
```cpp
int* p{};
std::cout << p << std::endl;
```

<details>
<summary>Answer</summary>

Empty braces value-initialize the pointer, which for pointers means it becomes `nullptr`.
This is equivalent to writing `int* p{ nullptr };`.

So `0` is printed (the null address).

This is different from `int* p;`, which leaves `p` uninitialized with garbage data.
Unlike an uninitialized pointer, reading `p` itself here (for example, printing it) is allowed.
Dereferencing `p` itself would still not be allowed, since it does not point to any variable.
</details>

### 21. Copying a variable and a pointer with similar names

```cpp
int x{ 0 };
int* px{ &x };
int y{ x };
int* py{ px };

*px = 1;

std::cout << x << std::endl;
std::cout << y << std::endl;
std::cout << *px << std::endl;
std::cout << *py << std::endl;
```

<details>
<summary>Answer:</summary>

`int y{ x }` copies the *value* from `x` — `y` is independent of `x` afterwards,
so writing through the pointer does not affect it.

`int* py{ px }` copies the *address* from `px` — both pointers point to the same variable `x`.

`*px = 1` writes `1` into `x`, so the output is:
- `x` — `1`,
- `y` — `0` (copied before the assignment),
- `*px` — `1`,
- `*py` — `1` (same address as `px`).
</details>


## Type-checking puzzles

Each snippet is independent. Does it compile? Give the types of both sides of the last assignment.
Most snippets are deliberately incorrect; explain a correction instead of trying to run them.

### 1. An integer assigned to a pointer

```cpp
int value{ 5 };
int* p{};
p = value;
```

<details>
<summary>Answer</summary>

It does not compile.
The right side has type `int`; the left side requires `int*`.
Use `p = &value;` to store an address.
</details>

### 2. A pointer assigned to a double pointer

```cpp
int value{ 5 };
int* p{ &value };
int** pp{};
pp = p;
```

<details>
<summary>Answer</summary>

It does not compile.
`p` has type `int*`, while `pp` requires `int**`.
Use `pp = &p;` to point to the pointer variable.
</details>

### 3. A pointer assigned to an integer

```cpp
int value{ 5 };
int* p{ &value };
int result{};
result = p;
```

<details>
<summary>Answer</summary>

It does not compile.
`p` is an address of type `int*`, not an integer value.
Use `result = *p;` to copy the pointed-to value.
</details>

### 4. A pointer address assigned to a pointer

```cpp
int value{ 5 };
int* p{ &value };
int* other{};
other = &p;
```

<details>
<summary>Answer</summary>

It does not compile.
`&p` has type `int**`; `other` has type `int*`.
Use `other = p;` to copy the stored address, or declare `other` as `int**` to store `&p`.
</details>

### 5. An integer address assigned to a double pointer

```cpp
int value{ 5 };
int** pp{};
pp = &value;
```

<details>
<summary>Answer</summary>

It does not compile.
`&value` has type `int*`, not `int**`.
An extra `*` in a declaration does not make it accept every kind of address.
</details>

### 6. Copying a pointer through a double pointer

```cpp
int value{ 5 };
int* p{ &value };
int** pp{ &p };
int* other{};
other = *pp;
```

<details>
<summary>Answer</summary>

It compiles.
`*pp` has type `int*`, so the assignment is valid.
`other` and `p` now point to the same integer.
</details>

### 7. One dereference instead of two

```cpp
int value{ 5 };
int* p{ &value };
int** pp{ &p };
int result{};
result = *pp;
```

<details>
<summary>Answer</summary>

It does not compile.
`*pp` has type `int*`; `result` needs `int`.
Use `result = **pp;` to read the integer.
</details>

### 8. Writing through two dereferences

```cpp
int value{ 5 };
int* p{ &value };
int** pp{ &p };
**pp = 8;
```

<details>
<summary>Answer</summary>

It compiles.
`**pp` accesses the `int` variable `value`.
The assignment is valid and stores `8` in it.
</details>

### 9. A size_t address assigned to an int8_t pointer

```cpp
#include <cstddef>
#include <cstdint>
std::size_t count{ 3 };
std::int8_t* p{};
p = &count;
```

<details>
<summary>Answer</summary>

It does not compile.
`&count` has type `std::size_t*`, not `std::int8_t*`.
Pointers preserve the pointed-to type; this assignment performs no numeric conversion.
</details>

### 10. An int8_t address assigned to a size_t pointer

```cpp
#include <cstddef>
#include <cstdint>
std::int8_t value{ 3 };
std::size_t* p{};
p = &value;
```

<details>
<summary>Answer</summary>

It does not compile.
`&value` has type `std::int8_t*`; `p` requires `std::size_t*`.
Having a numeric value that fits both types does not make their pointers compatible.
</details>

### 11. An int8_t value assigned to a size_t

```cpp
#include <cstddef>
#include <cstdint>
std::int8_t value{ 3 };
std::size_t count{};
count = value;
```

<details>
<summary>Answer</summary>

It compiles.
This is a numeric assignment, so the value is converted to `std::size_t`.
`count` becomes `3`.
It does not assign or reinterpret an address.
</details>

### 12. A size_t value assigned to a pointer

```cpp
#include <cstddef>
std::size_t count{ 3 };
std::size_t* p{};
p = count;
```

<details>
<summary>Answer</summary>

It does not compile.
`count` has type `std::size_t`; `p` requires `std::size_t*`.
A type being large enough to hold numbers does not make those numbers pointers.
</details>

### 13. A double pointer with a different pointed-to type

```cpp
#include <cstddef>
#include <cstdint>
std::size_t count{ 3 };
std::size_t* p{ &count };
std::int8_t** pp{};
pp = &p;
```

<details>
<summary>Answer</summary>

It does not compile.
`&p` has type `std::size_t**`, while `pp` requires `std::int8_t**`.
Matching the number of stars is not enough: the pointed-to types must also match.
</details>

### 14. A size_t address with the wrong pointer depth

```cpp
#include <cstddef>
std::size_t count{ 3 };
std::size_t** pp{};
pp = &count;
```

<details>
<summary>Answer</summary>

It does not compile.
`&count` has type `std::size_t*`, not `std::size_t**`.
First create a pointer to `count`, then take the address of that pointer.
</details>

### 15. Assigning an int8_t read through a pointer to a size_t

```cpp
#include <cstddef>
#include <cstdint>
std::int8_t small{ 3 };
std::int8_t* p{ &small };
std::size_t count{};
count = *p;
```

<details>
<summary>Answer</summary>

It compiles.
`*p` has type `std::int8_t`, so this converts a numeric value to `std::size_t`.
`count` becomes `3`; the pointer itself is not assigned.
</details>
