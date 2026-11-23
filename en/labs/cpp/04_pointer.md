---
slug: en/cpp/labs/pointer
---
<!-- course-site-backlink:start -->
[This lesson on the website](https://cpp.curmanschii.top/en/cpp/labs/pointer/)
<!-- course-site-backlink:end -->
# Pointers

- [Video about pointers](https://www.youtube.com/watch?v=859Y0Q8pyLg&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=8)
- [Video covering the basics, with more in-depth information](https://www.youtube.com/watch?v=9AhNOjjyAwU&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=14)

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
<summary>Execution trace</summary>

<!-- <visualization> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#1-variable-address)

<!-- </visualization> -->

</details>

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

> `&` can give the address of *any object*, but that will be covered in lab 13.
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
<summary>Execution trace</summary>

<!-- <visualization> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#2-address-of-an-uninitialized-variable)

<!-- </visualization> -->

</details>

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
<summary>Execution trace</summary>

<!-- <visualization> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#3-dereference-operator-writing)

<!-- </visualization> -->

</details>

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

### 6. Whitespace in pointer declarations

```cpp
int value{ 5 };
int* a{ &value };
int *b{ &value };
int * c{ &value };
int     *     d{ &value };
     *     a = 6;
std::cout << *b << std::endl;
std::cout << *c << std::endl;
std::cout <<     *     d << std::endl;
```

<details>
<summary>Answer</summary>

It prints `6` three times.
`int* a`, `int *b`, `int * c`, and `int     *     d` all declare an `int*`.
Whitespace between these tokens does not change the declaration.
All four pointers store the address of the same variable.
Whitespace around the dereference operator also has no effect: `*a` and `     *     a` access the same variable.
</details>

### 7. Printing a complex expression
```cpp
int a{ 5 };
int* b{ &a };
std::cout << (*b) + 7;
std::cout << std::endl;
```

<details>
<summary>Execution trace</summary>

<!-- <visualization> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#7-printing-a-complex-expression)

<!-- </visualization> -->

</details>

<details>
<summary>Correct answer:</summary>

`(*b) + 7` is an expression. It is evaluated in parts:
- `(*b)` means following the address in `b` and treating the result as the variable `a`.
- `(*b) + 7` -> `a + 7`; `a` is replaced with the value in `a` because it is used as an expression.
- `5 + 7` -> `12`.
</details>

### 8. Pointer to a larger data type
```cpp
uint8_t a{ 5 };
int* b{ &a };
```

<details>
<summary>Execution trace</summary>

<!-- <visualization types> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#8-pointer-to-a-larger-data-type)

<!-- </visualization> -->

</details>

<details>
<summary>Correct answer:</summary>

Compilation error (see the video about pointers)
</details>

### 9. Pointer to a smaller data type
```cpp
int a = 5;
uint8_t* b = &a;
```

<details>
<summary>Execution trace</summary>

<!-- <visualization types> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#9-pointer-to-a-smaller-data-type)

<!-- </visualization> -->

</details>

<details>
<summary>Correct answer:</summary>

Compilation error (see the video about pointers)
</details>

### 10. Dependence of the address on the value

Will `b` and `c` contain the same address?
```cpp
int a = 5;
int* b = &a;
a = 6;
int* c = &a;
```

<details>
<summary>Execution trace</summary>

<!-- <visualization> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#10-dependence-of-the-address-on-the-value)

<!-- </visualization> -->

</details>

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


### 11. It is the same memory!
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
<summary>Execution trace</summary>

<!-- <visualization> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#11-it-is-the-same-memory)

<!-- </visualization> -->

</details>

<details>
<summary>Answer:</summary>

Both reads and writes occur at the same address.
`ap` contains the address of variable `a`.
Writing to or reading from `*ap` is equivalent to working with `a` directly.
</details>

### 12. Assigning a value through a pointer

Is something like this allowed?
```cpp
int a;
int* b = &a;
*b = 5;
std::cout << a;
std::cout << std::endl;
```

<details>
<summary>Execution trace</summary>

<!-- <visualization> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#12-assigning-a-value-through-a-pointer)

<!-- </visualization> -->

</details>

<details>
<summary>Answer:</summary>

A value can be assigned to an uninitialized variable through a pointer.
This is allowed.
</details>

### 13. Reassigning a pointer
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
<summary>Execution trace</summary>

<!-- <visualization> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#13-reassigning-a-pointer)

<!-- </visualization> -->

</details>

<details>
<summary>Answer:</summary>

On the line `p = &b`, the *address* in `p` itself is overwritten with the address of another variable (`b`).

`*p = 8` now writes 8 into `b`.

</details>

### 14. Double pointer
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
<summary>Execution trace</summary>

<!-- <visualization> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#14-double-pointer)

<!-- </visualization> -->

</details>

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

### 15. auto from an address

```cpp
int value{ 5 };
auto p{ &value };
*p = 8;
std::cout << value << std::endl;
```

<details>
<summary>Execution trace</summary>

<!-- <visualization> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#15-auto-from-an-address)

<!-- </visualization> -->

</details>

<details>
<summary>Answer</summary>

`&value` has type `int*`, so `p` has type `int*`.
It prints `8`: writing through the inferred pointer changes `value`.
</details>

### 16. auto from a pointer and its value

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
<summary>Execution trace</summary>

<!-- <visualization> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#16-auto-from-a-pointer-and-its-value)

<!-- </visualization> -->

</details>

<details>
<summary>Answer</summary>

`p` has type `int*`; `*p` has type `int`.
Thus `copiedPointer` points to the same variable, while `copiedValue` is an independent integer copy.
It prints `8` and `5`.
</details>

### 17. auto from the address of a pointer

```cpp
int value{ 5 };
int* p{ &value };
auto pp{ &p };
**pp = 9;
std::cout << value << std::endl;
```

<details>
<summary>Execution trace</summary>

<!-- <visualization> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#17-auto-from-the-address-of-a-pointer)

<!-- </visualization> -->

</details>

<details>
<summary>Answer</summary>

`&p` has type `int**`, so `pp` has type `int**`.
`*pp` accesses `p`; `**pp` accesses `value`.
It prints `9`.
</details>

### 18. Pointer sizes
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

### 19. Pointer and variable sizes

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

### 20. Pointer to itself
```cpp
void* p = nullptr;
p = static_cast<void*>(&p);

std::cout << p;
std::cout << std::endl;

std::cout << &p;
std::cout << std::endl;
```

<details>
<summary>Execution trace</summary>

<!-- <visualization types> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#20-pointer-to-itself)

<!-- </visualization> -->

</details>

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

### 21. Empty pointer initialization
```cpp
int* p{};
std::cout << p << std::endl;
```

<details>
<summary>Execution trace</summary>

<!-- <visualization> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#21-empty-pointer-initialization)

<!-- </visualization> -->

</details>

<details>
<summary>Answer</summary>

Empty braces value-initialize the pointer, which for pointers means it becomes `nullptr`.
This is equivalent to writing `int* p{ nullptr };`.

So `0` is printed (the null address).

This is different from `int* p;`, which leaves `p` uninitialized with garbage data.
Unlike an uninitialized pointer, reading `p` itself here (for example, printing it) is allowed.
Dereferencing `p` itself would still not be allowed, since it does not point to any variable.
</details>

### 22. Copying a variable and a pointer with similar names

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
<summary>Execution trace</summary>

<!-- <visualization> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#22-copying-a-variable-and-a-pointer-with-similar-names)

<!-- </visualization> -->

</details>

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

### 23. Writing through a pointer to a larger type (1)

```cpp
uint8_t a{ 5 };
int c{ 10 };
int* b{ reinterpret_cast<int*>(&a) };
*b = 300;
```

<details>
<summary>Execution trace</summary>

<!-- <visualization punning> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#23-writing-through-a-pointer-to-a-larger-type-1)

<!-- </visualization> -->

</details>

<details>
<summary>What does <code>reinterpret_cast</code> do here?</summary>

In examples 8 and 9, `int* b{ &a };` failed to compile because `&a` has type `uint8_t*`.
`reinterpret_cast<int*>(&a)` tells the compiler to treat that same address as an `int*` anyway,
without converting the value or moving the variable.
That makes it possible to see why the compiler rejected the assignment in the first place.
</details>

<details>
<summary>Answer</summary>

`a` is a 1-byte `uint8_t`, while `b` is a pointer to a 4-byte `int`.
Because `c` is a 4-byte `int`, the compiler places 3 unused alignment padding bytes between `a`
and `c` so that `c` starts at a 4-byte boundary.

Dereferencing `b` treats the 4 bytes starting at `a`'s address as one `int`.
In hexadecimal, `300` (`256 + 44`) is `0x0000012C`.
On a little-endian machine, `*b = 300` writes the least significant byte (`0x2C`, which is `44`)
into `a` and spills the remaining 3 bytes (`01 00 00`) past `a` into the alignment padding
before `c`.
On a big-endian machine, the most significant byte (`00`) lands in `a` and `00 01 2C` spills into
the padding.
Writing past the bounds of `a` is undefined behavior.
</details>

### 24. Writing through a pointer to a larger type (2)

```cpp
uint8_t a{ 5 };
uint8_t c{ 10 };
int* b{ reinterpret_cast<int*>(&a) };
*b = 300;
```

<details>
<summary>Execution trace</summary>

<!-- <visualization punning> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#24-writing-through-a-pointer-to-a-larger-type-2)

<!-- </visualization> -->

</details>

<details>
<summary>Answer</summary>

Here `c` is a 1-byte `uint8_t`, so it can sit in the very next byte right after `a` with no
padding between them.

Writing the 4-byte `int` `300` (`0x0000012C`) through `*b` writes 4 bytes starting at `a`'s
address.
On a little-endian machine, the first byte (`0x2C`, or `44`) overwrites `a`, the second byte
(`0x01`, or `1`) overwrites `c`, and the remaining two bytes (`00 00`) spill into the bytes
after `c`.
Although the assignment never names `c`, `*b = 300` corrupts `c`.
Overwriting neighboring memory past `a` is undefined behavior.
</details>

### 25. Reading through a pointer to a larger type (1)

```cpp
uint8_t a{ 42 };
int c{ 10 };
int* b{ reinterpret_cast<int*>(&a) };
int x{ *b };
```

<details>
<summary>Execution trace</summary>

<!-- <visualization punning> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#25-reading-through-a-pointer-to-a-larger-type-1)

<!-- </visualization> -->

</details>

<details>
<summary>Answer</summary>

Reading `*b` reads 4 bytes starting at `a`'s address to form an `int`.
Only the first byte belongs to `a` (`42`, which is `0x2A` in hexadecimal).
The next 3 bytes are uninitialized alignment padding before `c` and hold indeterminate values
(`??`).

Reading past `a` is undefined behavior.
`x` is assembled from `a`'s byte and 3 indeterminate padding bytes (`0x??????2A` on
little-endian, or `0x2A??????` on big-endian).
</details>

### 26. Reading through a pointer to a larger type (2)

```cpp
uint16_t a{ 5 };
uint16_t c{ 2 };
int* b{ reinterpret_cast<int*>(&a) };
int x{ *b };
```

<details>
<summary>Execution trace</summary>

<!-- <visualization punning> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#26-reading-through-a-pointer-to-a-larger-type-2)

<!-- </visualization> -->

</details>

<details>
<summary>Answer</summary>

`a` and `c` are 2-byte `uint16_t` variables placed in adjacent 2-byte slots (`05 00` and `02 00`
on little-endian).
All 4 bytes starting at `a` hold known values with no padding gap, yet reading a 4-byte `int`
through `*b` still reaches past the end of `a` into `c`, which is undefined behavior.

On a little-endian machine, the 4 bytes `05 00 02 00` assemble into `0x00020005`, which is
`131077`.
On a big-endian machine, `00 05 00 02` assembles into `0x00050002`, which is `327682`.
</details>

### 27. Writing through a pointer to a smaller type (1)

```cpp
int a{ 5 };
uint8_t* b{ reinterpret_cast<uint8_t*>(&a) };
*b = 2;
```

<details>
<summary>Execution trace</summary>

<!-- <visualization punning> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#27-writing-through-a-pointer-to-a-smaller-type-1)

<!-- </visualization> -->

</details>

<details>
<summary>Answer</summary>

`a` occupies 4 bytes, while `b` is a `uint8_t*` that accesses only 1 byte at `a`'s starting
address.
`*b = 2` overwrites only that first byte of `a` with `02` and leaves the other 3 bytes untouched.

On a little-endian machine, the first byte of `a` is its least significant byte (`05 00 00 00`
becomes `02 00 00 00`), so `a` becomes `2`.
On a big-endian machine, the first byte of `a` is its most significant byte (`00 00 00 05`
becomes `02 00 00 05`, or `0x02000005`), so `a` becomes `33554437`.
</details>

### 28. Writing through a pointer to a smaller type (2)

```cpp
int a{ 261 };
uint8_t* b{ reinterpret_cast<uint8_t*>(&a) };
*b = 0;
```

<details>
<summary>Execution trace</summary>

<!-- <visualization punning> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#28-writing-through-a-pointer-to-a-smaller-type-2)

<!-- </visualization> -->

</details>

<details>
<summary>Answer</summary>

`261` is `256 + 5`, or `0x00000105`.
On a little-endian machine, the 4 bytes of `a` are `05 01 00 00`.
Because `b` is a `uint8_t*`, `*b = 0` zeroes only the first byte (`05` becomes `00`) and does
not touch the remaining 3 bytes.
The second byte still holds `01` (`256`), so `a` becomes `256` (`00 01 00 00`) rather than `0`.

On a big-endian machine, the bytes of `a` are `00 00 01 05`, so writing `0` into the first byte
leaves `a` unchanged at `261`.
</details>

### 29. Reading through a pointer to a smaller type

```cpp
int a{ 261 };
uint8_t* b{ reinterpret_cast<uint8_t*>(&a) };
uint8_t x{ *b };
```

<details>
<summary>Execution trace</summary>

<!-- <visualization punning> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#29-reading-through-a-pointer-to-a-smaller-type)

<!-- </visualization> -->

</details>

<details>
<summary>Answer</summary>

Dereferencing `uint8_t* b` reads only 1 byte from `a`'s starting address and ignores the other 3
bytes of `a`.
On a little-endian machine, the first byte of `261` (`05 01 00 00`) is `05`, so `x` becomes `5`.
On a big-endian machine, the first byte of `261` (`00 00 01 05`) is `00`, so `x` becomes `0`.
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
<summary>Execution trace</summary>

<!-- <visualization types> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#1-an-integer-assigned-to-a-pointer)

<!-- </visualization> -->

</details>

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
<summary>Execution trace</summary>

<!-- <visualization types> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#2-a-pointer-assigned-to-a-double-pointer)

<!-- </visualization> -->

</details>

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
<summary>Execution trace</summary>

<!-- <visualization types> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#3-a-pointer-assigned-to-an-integer)

<!-- </visualization> -->

</details>

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
<summary>Execution trace</summary>

<!-- <visualization types> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#4-a-pointer-address-assigned-to-a-pointer)

<!-- </visualization> -->

</details>

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
<summary>Execution trace</summary>

<!-- <visualization types> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#5-an-integer-address-assigned-to-a-double-pointer)

<!-- </visualization> -->

</details>

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
<summary>Execution trace</summary>

<!-- <visualization types> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#6-copying-a-pointer-through-a-double-pointer)

<!-- </visualization> -->

</details>

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
<summary>Execution trace</summary>

<!-- <visualization types> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#7-one-dereference-instead-of-two)

<!-- </visualization> -->

</details>

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
<summary>Execution trace</summary>

<!-- <visualization types> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#8-writing-through-two-dereferences)

<!-- </visualization> -->

</details>

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
size_t count{ 3 };
int8_t* p{};
p = &count;
```

<details>
<summary>Execution trace</summary>

<!-- <visualization types> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#9-a-size_t-address-assigned-to-an-int8_t-pointer)

<!-- </visualization> -->

</details>

<details>
<summary>Answer</summary>

It does not compile.
`&count` has type `size_t*`, not `int8_t*`.
Pointers preserve the pointed-to type; this assignment performs no numeric conversion.
</details>

### 10. An int8_t address assigned to a size_t pointer

```cpp
#include <cstddef>
#include <cstdint>
int8_t value{ 3 };
size_t* p{};
p = &value;
```

<details>
<summary>Execution trace</summary>

<!-- <visualization types> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#10-an-int8_t-address-assigned-to-a-size_t-pointer)

<!-- </visualization> -->

</details>

<details>
<summary>Answer</summary>

It does not compile.
`&value` has type `int8_t*`; `p` requires `size_t*`.
Having a numeric value that fits both types does not make their pointers compatible.
</details>

### 11. An int8_t value assigned to a size_t

```cpp
#include <cstddef>
#include <cstdint>
int8_t value{ 3 };
size_t count{};
count = value;
```

<details>
<summary>Execution trace</summary>

<!-- <visualization types> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#11-an-int8_t-value-assigned-to-a-size_t)

<!-- </visualization> -->

</details>

<details>
<summary>Answer</summary>

It compiles.
This is a numeric assignment, so the value is converted to `size_t`.
`count` becomes `3`.
It does not assign or reinterpret an address.
</details>

### 12. A size_t value assigned to a pointer

```cpp
#include <cstddef>
size_t count{ 3 };
size_t* p{};
p = count;
```

<details>
<summary>Execution trace</summary>

<!-- <visualization types> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#12-a-size_t-value-assigned-to-a-pointer)

<!-- </visualization> -->

</details>

<details>
<summary>Answer</summary>

It does not compile.
`count` has type `size_t`; `p` requires `size_t*`.
A type being large enough to hold numbers does not make those numbers pointers.
</details>

### 13. A double pointer with a different pointed-to type

```cpp
#include <cstddef>
#include <cstdint>
size_t count{ 3 };
size_t* p{ &count };
int8_t** pp{};
pp = &p;
```

<details>
<summary>Execution trace</summary>

<!-- <visualization types> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#13-a-double-pointer-with-a-different-pointed-to-type)

<!-- </visualization> -->

</details>

<details>
<summary>Answer</summary>

It does not compile.
`&p` has type `size_t**`, while `pp` requires `int8_t**`.
Matching the number of stars is not enough: the pointed-to types must also match.
</details>

### 14. A size_t address with the wrong pointer depth

```cpp
#include <cstddef>
size_t count{ 3 };
size_t** pp{};
pp = &count;
```

<details>
<summary>Execution trace</summary>

<!-- <visualization types> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#14-a-size_t-address-with-the-wrong-pointer-depth)

<!-- </visualization> -->

</details>

<details>
<summary>Answer</summary>

It does not compile.
`&count` has type `size_t*`, not `size_t**`.
First create a pointer to `count`, then take the address of that pointer.
</details>

### 15. Assigning an int8_t read through a pointer to a size_t

```cpp
#include <cstddef>
#include <cstdint>
int8_t small{ 3 };
int8_t* p{ &small };
size_t count{};
count = *p;
```

<details>
<summary>Execution trace</summary>

<!-- <visualization types> -->

[▶ Step through this example on the course site](https://cpp.curmanschii.top/en/cpp/labs/pointer/#15-assigning-an-int8_t-read-through-a-pointer-to-a-size_t)

<!-- </visualization> -->

</details>

<details>
<summary>Answer</summary>

It compiles.
`*p` has type `int8_t`, so this converts a numeric value to `size_t`.
`count` becomes `3`; the pointer itself is not assigned.
</details>
