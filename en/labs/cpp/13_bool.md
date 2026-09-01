# `bool`

Topic: `bool`, flow control.

Video:
- [`bool`, flow control](https://www.youtube.com/watch?v=21m4VfonFnA&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=10)

## Concepts

- Boolean values (`true`, `false`)
- Boolean expressions
- Numeric comparison operators `>`, `<`, `>=`, `<=`, `==`, `!=`
- Boolean operators `&&`, `||`, `==`, `!`, `!=`
- Lazy evaluation of the operands of the `&&` and `||` operators
- Implicit conversion to `bool` from `int` and pointers
- The `NULL` macro
- The special `nullptr` value

## Examples to aid understanding

### 1. `true`
```cpp
bool a { true };
std::cout << a << std::endl;
```

<details>
<summary>Answer</summary>

The `bool` type has only two possible values: `true` and `false`.  
When printed to the console, `true` is displayed as `1` and `false` as `0`.
</details>

### 2. `0` and `1` as `bool`
```cpp
bool a { 0 };
bool b { 1 };
```

<details>
<summary>Answer</summary>

You can also store `0` instead of `false`, and `1` instead of `true`.
This compiles successfully.
</details>

### 3. Converting `int` to `bool`
```cpp
bool c { static_cast<bool>(123) };
```

<details>
<summary>Answer</summary>

`static_cast<bool>` applied to an `int` produces `true` if the number is not `0`, otherwise `false`.
`c` will contain `true`.
</details>

### 4. Size of `bool`
```cpp
std::cout << sizeof(bool) << std::endl;
```

<details>
<summary>Answer</summary>

`bool` takes 1 byte, even though just one bit is enough to represent two values, 
0 or 1.
If you want to store several `bool` values in separate bits
of the same byte, you need to use bit masks.
</details>

### 5. `bool` expression (1)
```cpp
bool a = 1 == 2;
std::cout << a << std::endl;
```

<details>
<summary>Answer</summary>

The `==` operator takes 2 expressions as operands and returns the result of the equality check as a Boolean value.
The result is `false`.
</details>

### 6. `bool` expression (2)
```cpp
int x = 3;
int y = 4;
bool b = x == y;
std::cout << b << std::endl;
```

<details>
<summary>Answer</summary>

Here, the operator works with the values of the variables rather than with the variables themselves.
When the code runs, the variables are evaluated to their values before the comparison.
</details>

### 7. `bool` expression (3)
```cpp
int x = 3;
int y = 4;
bool b = x == y;
x = 4;
std::cout << b << std::endl;
```

<details>
<summary>Answer</summary>

`b` stores not the expression `x == y`, but the result of evaluating it (`false`).
Subsequent changes to `x` do not affect `b` in any way.
</details>

### 8. `bool` expression (4)
```cpp
int x = 3;
int y = 4;
bool b = x * 2 == y + 4;
std::cout << b << std::endl;
```

<details>
<summary>Answer</summary>

This is an example of using more complex expressions as operands.

`bool b = x * 2 == y + 4` is interpreted as `bool b = ((x * 2) == (y + 4))`.
The calculations then proceed according to the rules for expressions.
</details>

### 9. Reassigning a `bool` variable
```cpp
bool a = 1 > 2;
a = 3 == 3;
std::cout << a << std::endl;
```

<details>
<summary>Answer</summary>

Here, `a` is reassigned from `false` to another value (`true`).
</details>

### 10. Passing a `bool` variable to a function
```cpp
#include <iostream>

void f(bool a)
{
    std::cout << a << std::endl;
}

int main()
{
    bool a = true;
    f(a);
}
```

### 11. Passing a Boolean expression to a function
```cpp
#include <iostream>

void f(bool flag)
{
    std::cout << flag << std::endl;
}

int main()
{
    f(5 > 3);
}
```

<details>
<summary>Answer</summary>

The argument `5 > 3` is evaluated before the function is called.  
`flag` receives the result `true`.
</details>

### 12. Function that reassigns a `bool` parameter
```cpp
#include <iostream>

void f(bool b)
{
    b = true;
}

int main()
{
    int x { 1 };
    f(x == 2);
    std::cout << x << std::endl;
}
```

<details>
<summary>Answer</summary>

When `f` is called, it receives the result of evaluating the expression `x == 2`.
Changing the parameter `b` does not affect `x` in any way.

It prints `1`.
</details>

### 13. Returning a `bool` value
```cpp
#include <iostream>

bool f()
{
    return true;
}

int main()
{
    bool result = f();
    std::cout << result << std::endl;
}
```

### 14. Example of a Boolean function
```cpp

#include <iostream>

bool IsGreater(int a, int b)
{
    return a > b;
}

int main()
{
    bool result = IsGreater(5, 6);
    std::cout << result << std::endl;
}
```

### 15. Comparing Boolean variables
```cpp
bool a = true;
bool b = false;
bool c = a == b;
std::cout << c << std::endl;
```

<details>
<summary>Answer</summary>

The equality operator `==` can be applied to expressions of type `bool`.
The comparison `true == false` produces `false`.
</details>

### 16. The `!` operator
```cpp
bool a = false;
bool b = !a;
std::cout << b << std::endl;
```

<details>
<summary>Answer</summary>

The `!` operator turns `false` into `true` (and vice versa).
</details>

### 17. The `&&` operator
```cpp
bool a = true;
bool b = false;
bool c = a && b;
std::cout << c << std::endl;
```

<details>
<summary>Answer</summary>

`a && b` -> `true && false` -> `false`, because both operands must be `true`.
</details>

### 18. Nuances of the `&&` operator (1)
```cpp
#include <iostream>

bool A()
{
    std::cout << "A" << std::endl;
    return true;
}

bool B()
{
    std::cout << "B" << std::endl;
    return true;
}

int main()
{
    bool result = A() && B();
}
```

<details>
<summary>Answer</summary>

To determine whether both `A()` and `B()` return `true`, the program has to call both of them.

```
A
B
```
</details>

### 19. Nuances of the `&&` operator (2)
```cpp
#include <iostream>

bool A()
{
    std::cout << "A" << std::endl;
    return true;
}

bool B()
{
    std::cout << "B" << std::endl;
    return false;
}

int main()
{
    bool result = A() && B();
}
```

<details>
<summary>Answer</summary>

The first function returns `true`, so the second one is also executed.  
The second returns `false`, and the result of the expression is `A() && B()` -> `true && false` -> `false`.

```
A
B
```
</details>

### 20. Nuances of the `&&` operator (3)
```cpp
#include <iostream>

bool A()
{
    std::cout << "A" << std::endl;
    return false;
}

bool B()
{
    std::cout << "B" << std::endl;
    return true;
}

int main()
{
    bool result = A() && B();
}
```

<details>
<summary>Answer</summary>

With `&&`, if the first operand is `false`, the second is not evaluated.  
This is called lazy evaluation.

```
A
```
</details>

### 21. Nuances of the `||` operator (4)
```cpp
#include <iostream>

bool A()
{
    std::cout << "A" << std::endl;
    return true;
}

bool B()
{
    std::cout << "B" << std::endl;
    return true;
}

int main()
{
    bool result = A() || B();
}
```

<details>
<summary>Answer</summary>

With `||`, if the first operand is `true`, the second is not evaluated.  
This is also lazy evaluation.

```
A
```
</details>

### 22. A function changes a variable used in a parameter expression
```cpp
#include <iostream>

void func(bool b, int* a)
{
    std::cout << b << std::endl;
    *a = 2;
    std::cout << b << std::endl;
}

int main()
{
    int a { 1 };
    func(a == 1, &a);
}
```

<details>
<summary>Answer</summary>

`func` receives **the result of evaluating the expression** `a == 1`,
as well as the address of `a`.

Changing `a` inside `func` does not change `b`, because `b` stores only the
result, not the expression that produced it.
</details>
