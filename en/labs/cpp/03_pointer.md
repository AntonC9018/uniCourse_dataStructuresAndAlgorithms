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
>     // сюда
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
int a = 5; // скажем, адрес = 32
int b = 6; // скажем, адрес = 36
int* p = &a; // адрес p = 40, адрес в p = 32
int** pp = &p; // адрес в pp = 40
**pp = 7; // *(*pp) --> *(40) --> *(p) --> *32 --> a
         // то есть a = 7
*pp = &b; // адрес в p = 36
**pp = 8; // *(*pp) --> *(40) --> *(p) --> *36 --> b
         // то есть b = 8

std::cout << a;
std::cout << std::endl;

std::cout << b;
std::cout << std::endl;
```
</details>

### 14. Pointer sizes
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

### 15. Pointer and variable sizes

```cpp
int a = 7;
int ap = &a;

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
