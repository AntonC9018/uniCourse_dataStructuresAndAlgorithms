# Functions

- [Video](https://www.youtube.com/watch?v=6JtlzvwhHr0&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=29)

## Concepts

- Function
- Function call
- Function definition
- Parameter, argument
- Return value, `return`
- How a function's interface is specified

## Comprehension questions

For each of the following examples, explain:
- How many variables will exist at different stages of program execution;
- Whether the program will compile at all, and if not, why;
- What values each variable will have at the end of the program.

### 1. Two different variables
```cpp
void func()
{
    int b = 6;
}
int main()
{
    int a = 5;
    func();
}
```

<details>
<summary>Answer:</summary>

One variable, `a`, is created in `main`; it has the value 5.

Then, when `func` is called, it creates another variable, `b`, with the value `6`.
It occupies the next free slot after `a` in temporary memory (the stack), if we ignore other data needed for function calls.

When `func` finishes, the second variable, `b`, ceases to exist —
that is, its memory can no longer be referenced from `main`; however, the value 6
continues to remain in that memory location.
</details>

### 2. Two variables with the same name
```cpp
void func()
{
    int a = 6;
}
int main()
{
    int a = 5;
    func();
}
```

<details>
<summary>Answer:</summary>

The situation is equivalent to the previous example.
The difference is that the local variable that was named `b` in the previous example is now named `a`.
The variables still occupy different memory locations.
</details>

### 3. Assigning to a variable in another function
```cpp
void func()
{
    int b = 6;
}
int main()
{
    int a = 5;
    func();
    b = 7;
}
```

<details>
<summary>Answer:</summary>

This code illustrates that the variable `b` ceases to exist after `func` returns.
The code will not compile.
</details>

### 4. Assigning to a passed variable
```cpp
void func(int b)
{
    b = 6;
}
int main()
{
    int a = 5;
    func(a);
}
```

<details>
<summary>Answer:</summary>

When the function is called, a local variable is allocated for each of its parameters.
The values of the arguments are *copied* into these variables—
specifically, the values of the expressions in the corresponding call positions (here, `a`).

`b = 6` changes the local variable that exists during the call to `func`.
`b = 6` does not affect `a`.

`a` will be 5.
</details>

### 5. Assigning to a passed variable with the same name
```cpp
void func(int a)
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
<summary>Answer:</summary>

The situation is equivalent to the previous one.
The parameter `a` in `func` is a local variable created when `func` is called.
This `a` is not connected to the `a` in `main`.

`a` will be `5`.
</details>

### 6. Passing a structure
```cpp
struct A
{
    int f1;
    int f2;
};
void func(A a)
{
    a.f1 = 1;
    a.f2 = 2;
}
int main()
{
    A a;
    a.f1 = 3;
    a.f2 = 4;
    func(a);
}
```

<details>
<summary>Answer:</summary>

Here, `A` is the parameter type.
When a value of type `A` is passed, each of its fields is copied separately.

Again, the variable and parameter names do not matter; they are not connected to each other.

The code in `func` will not affect the `a` in `main`.
</details>

### 7. Passing an address
```cpp
void func(int* a)
{
    *a = 1;
}
int main()
{
    int a{2};
    func(&a);
}
```

<details>
<summary>Answer:</summary>

Here, the address of a local variable is passed to the function.

`a` in `func` holds **an address rather than a copy of the original integer**.
Using it, you can reference and modify the memory of the local variable in `main`.

`a` will be overwritten with `1` by the function.
</details>

### 8. Passing the address of a structure
```cpp
#include <iostream>

struct A
{
    int f1;
    int f2;
};
void func(A* a)
{
    a->f1 = 1;
    a->f2 = 2;
}
int main()
{
    A a;
    a.f1 = 3;
    a.f2 = 4;
    func(&a);

    std::cout << a.f1 << std::endl;
    std::cout << a.f2 << std::endl;
}
```

<details>
<summary>Answer:</summary>

The situation is similar to the one above.

`a` in `func` holds **an address rather than copies of the fields**.

Here, the values of both fields of the variable `a` in `main` will be overwritten.
</details>

### 9. Two parameters (1)
```cpp
int func(int a, int b)
{
    return a + b;
}
int main()
{
    int b = 6;
    func(1, b);
}
```

<details>
<summary>Answer:</summary>

Although `func` returns a result, it is not saved anywhere.
`b` will retain its old value.
</details>

### 10. Two parameters (2)
```cpp
int func(int a, int b)
{
    return a + b;
}
int main()
{
    int b = 6;
    int s = func(1, b);
    b = s;
}
```

<details>
<summary>Answer:</summary>

Both `b` and `s` will be 7.
</details>

### 11. Passing a function call as a parameter
```cpp
int func(int a, int b)
{
    return a + b;
}
int main()
{
    int b = 6;
    int s = func(func(1, func(2, b)), b);
}
```

<details>
<summary>Answer:</summary>

`func(func(1, func(2, b)), b)` is a complex expression; it is evaluated from the inside out:
- `func(2, b)` -> `func(2, 6)` -> `8`;
- `func(1, 8)` -> `9`;
- `func(9, b)` -> `func(9, 6)` -> `15`.
</details>

### 12. A function that calls itself
```cpp
void func(int a)
{
    func(a);
}
int main()
{
    func(1);
}
```
<details>
<summary>Answer:</summary>

Here, each call to `func` from within itself causes more memory to be allocated,
at least for variable `a`, because each subsequent call to
`func` creates its own local `a`, initialized with the value of `a` in the
preceding call (that is, 1).

At some point, the stack will run out of memory and the program will crash (stack overflow).
</details>

### 13. Copying arguments
```cpp
#include <iostream>

void func(int sum, int* a)
{
    std::cout << sum << std::endl;
    *a = 3;
    std::cout << sum << std::endl;
}
int main()
{
    int a { 1 };
    func(a + 2, &a);
}
```

<details>
<summary>Answer:</summary>

`3` will be printed twice because the expression `a + 2` is evaluated first,
then its *result* is passed to the function.
A function **receives the result of evaluating an expression, not the expression itself**.

Changing `a` does not affect the sum in any way, because they are stored in two unrelated memory locations.
</details>

### 14. Passing a parameter, then changing it after the call
```cpp
#include <iostream>

int func(int x)
{
    return x;
}

int main()
{
    int a { 1 };
    int b { func(a) };
    a = 2;

    std::cout << a << std::endl;
    std::cout << b << std::endl;
}
```

<details>
<summary>Answer:</summary>

`a` will be `2`, and `b` will be `1`.

Three things happen on the line `int b { func(a) };`:
- memory is allocated for variable `b`;
- the result of the expression `func(a)` is calculated;
- the result of the expression is assigned to `b`.

The **result of the expression** is assigned to `b`!
</details>

<details>
<summary>What is the type of the result of the expression <code>func(a)</code>?</summary>

The result of the expression comes from executing the function,
so the expression has the function's return type.
The function's return type is specified in the function definition — `int`.

Since `b` also has type `int`, the result can be stored there.
If the type were incompatible, a compilation error would occur.
</details>

<details>
<summary>What happens when <code>func(a)</code> is evaluated?</summary>

- Local variables are created for the parameters.
 In this case, one variable is created for parameter `x`.
- The argument value is stored in `x` —
 the result of evaluating the expression `a` — `1`.
- Execution moves to the first statement of the function `func`.
- `return x` is executed, which **makes the result of the expression
 following `return` the result of the `func` call**.
 The result of the expression `x` (reading the local variable `x`),
 which is the value `1`, becomes the **result of the function call**.
- All local variables created during the call to `func` disappear.
 In this case, variable `x` disappears.

Since the result of the function call is used to initialize `b` on the line `int b { func(a) }`,
`b` receives the value that `a` had when `func(a)` was evaluated.
</details>

### 15. A real example: vector
```cpp
#include <iostream>

struct Vector
{
    int x;
    int y;
};

Vector multiply(Vector pos, int scalar)
{
    Vector result;
    result.x = pos.x * scalar;
    result.y = pos.y * scalar;
    return result;
}

int main()
{
    Vector v { 2, 3 };
    Vector v2 { multiply(v, 2) };

    std::cout << v2.x << std::endl;
    std::cout << v2.y << std::endl;
}
```

<details>
<summary>Will it work if the type of <code>v2</code> is changed from <code>Vector</code> to <code>int</code>?</summary>


The intended `main` function is:
```cpp
int main()
{
    Vector v { 2, 3 };
    int v2 { multiply(v, 2) };

    std::cout << v2 << std::endl;
}
```

<details>
<summary>Answer</summary>

It will not compile because the expression `multiply(v, 2)` has type `Vector`,
and an `int` cannot be created from a `Vector`.
</details>

</details>

### 16. Advanced level: addresses of local variables
```cpp
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

### 17. Advanced level: data in uninitialized variables
```cpp
void f()
{
    int a;
    std::cout << a << std::endl;
    a = 2;
}

void g()
{
    int b{ 1 };
    std::cout << b << std::endl;
}

int main()
{
    g();
    f();
    f();
}
```

<details>
<summary>Answer</summary>

If you do not pass the `-Wall` and `-Werror` flags when compiling, this will compile.
But remember that reading uninitialized variables is UB!

When the uninitialized variable `a` is read in `f`,
you may get the value that was previously in that memory location.
Before that, `g` was called and that memory location was allocated for variable `b`.
Therefore, uninitialized `a` may contain the last value of `b`
left in the memory allocated to it.

The situation is similar when `f` is called for the second time:
`a` may contain what was in that memory location before.
Before that, it contained `2`, written during the previous execution of `f`.

```
1
1
2
```
</details>
