---
slug: en/cpp/labs/variables
---
<!-- course-site-backlink:start -->
[This lesson on the website](https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms/en/cpp/labs/variables/)
<!-- course-site-backlink:end -->
# Variables and Types

- [Video about variables and types](https://www.youtube.com/watch?v=6ML34OuwZrc&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=6)
- [Video on the basics and more in-depth material (up to pointers)](https://www.youtube.com/watch?v=9AhNOjjyAwU&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=14)
- [Video about type conversions (up to pointers)](https://www.youtube.com/watch?v=imkDyDE7Tkw&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=28)

## Concepts

- A variable as an abstraction of a memory cell
- Relative locations of variables in RAM
- Variable definitions and declarations
- Operations on variables (reading and writing)
- Uninitialized variables, garbage data
- UB (undefined behavior)
- Initialization syntax
- Value
- Expressions and their evaluation
- Data types: signedness (negative values) and size

<!-- ## Practice --> 

## Understanding the examples

Explain what happens in the following code snippets.
Also, run the code to verify your reasoning.

> When `main` is not shown, place the code in a typical source file with a `main` function:
> ```cpp
> #include <iostream>
> #include <cstdint>
>
> int main()
> {
>     // your code here
> }
> ```

### 1. Variable definition
```cpp
int a = 5;
std::cout << a << std::endl;
```

<details>
<summary>Creating a variable</summary>

In `int a = 5;`, `int` is the type, `a` is the name, and `5` is the starting value. `int` stores whole numbers. The next line reads and prints the value in `a`.
</details>

<details>
<summary>Answer</summary>

Prints `5`; `a` has type `int`.
</details>

### 2. Variable declaration
```cpp
int a;
std::cout << a << std::endl;
```

<details>
<summary>Give a variable a value before reading it</summary>

`int a;` creates a local variable without giving it a starting value. Do not read it before writing a value into it. Here the printing line tries to do exactly that. Use `int a = 0;`, for example, to give it a known starting value.
</details>

<details>
<summary>Answer</summary>

No reliable output.
</details>

<details>
<summary>Why a test run does not prove this is safe</summary>

This is called undefined behavior in C++ versions through C++23: the language does not promise any particular result. Even seeing `0` once does not mean you can rely on it. Compiler warnings such as `-Wall` can help catch the mistake; `-Werror` turns warnings into errors.
</details>

### 3. Defining a variable with the same name
```cpp
int a = 5;
int a = 6;
std::cout << a << std::endl;
```

<details>
<summary>Creating a variable or changing its value</summary>

Writing `int a` creates a variable. You cannot create another variable with the same name in the same block, even with a different type. To change the existing value, write `a = 6;` without `int`.
</details>

<details>
<summary>Answer</summary>

Does not compile.
</details>

### 4. Assigning one variable to another
```cpp
int a = 5;
int b = 6;
a = b;
b = 7;
std::cout << a << std::endl;
```

<details>
<summary>Assignment copies the current value</summary>

`a = b` copies the value currently stored in `b` into `a`. It does not keep the variables connected. Here it copies `6`; changing `b` to `7` later does not change `a`.
</details>

<details>
<summary>Answer</summary>

Prints `6`.
</details>

### 5. Literals, variables and operators are expressions
```cpp
int a = 5;
int b = a;
int c = a + 6;
std::cout << b << std::endl;
std::cout << c << std::endl;
```

<details>
<summary>An expression gives a value</summary>

An expression is code that gives a value. A number such as `5` gives itself; reading `a` gives its stored value; `a + 6` adds two values. Here `a` is `5`, so `b` gets `5` and `c` gets `11`.
</details>

<details>
<summary>Answer</summary>

Prints `5` and `11` on separate lines.
</details>

### 6. Assigning an expression to a variable

What are the expressions in this code fragment?

```cpp
int a = 5;
int b = a + 6;
a = 7;
std::cout << b << std::endl;
```

<details>
<summary>Store the result, not the formula</summary>

In `int b = a + 6;`, the computer first calculates `a + 6` and then stores the result in `b`. Here that is `5 + 6`, or `11`. Changing `a` afterwards does not calculate `b` again.
</details>

<details>
<summary>Answer</summary>

Prints `11`. The number literals, variable reads, `a + 6`, `a = 7`, and the printing expression are expressions.
</details>

<details>
<summary>An assignment is also an expression</summary>

`a = 7` changes `a` and also gives back the assigned value. That lets you write:
```cpp
int c = (a = 7);
```
Both `a` and `c` then contain `7`.
</details>

### 7. String value
```cpp
int a = "abc";
```

<details>
<summary>The value must fit the type</summary>

`int` stores whole numbers. The text `"abc"` is not a whole number and cannot be used as the starting value of an `int`.
</details>

<details>
<summary>Answer</summary>

Does not compile.
</details>

### 8. Reversing the output expression

```cpp
"ggg" >> std::cout;
```

<details>
<summary>The order in a printing statement matters</summary>

Put `std::cout` on the left and use `<<`: `std::cout << "ggg";`. Reversing the order and changing `<<` to `>>` does not do the same thing.
</details>

<details>
<summary>Answer</summary>

Does not compile.
</details>

### 9. Uniform initialization
```cpp
int a{5};
```

<details>
<summary>Setting a starting value with braces</summary>

`int a{5};` gives `a` the starting value `5`, much like `int a = 5;`. Braces also help catch mistakes: `int a{5.6};` is rejected because an `int` cannot keep the fractional part.
</details>

<details>
<summary>Answer</summary>

Compiles; `a` has type `int` and value `5`.
</details>

<details>
<summary>What happens without braces</summary>

`int a = 5.6;` can compile, but stores only `5`: the fractional part is lost. The braces in `int a{5.6};` make the compiler reject that possible loss.
</details>

### 10. Empty initialization
```cpp
int a{};
std::cout << a << std::endl;
```

<details>
<summary>Empty braces give an int zero</summary>

`int a{};` gives `a` the starting value `0`. This is different from `int a;`, which gives no starting value. Reading `a` is safe here.
</details>

<details>
<summary>Answer</summary>

Prints `0`.
</details>

### 11. Assigning empty braces

```cpp
int a{ 7 };
a = {};
std::cout << a << std::endl;
```

<details>
<summary>Assigning empty braces</summary>

For an `int`, `a = {};` writes `0` into `a`. It replaces the old value `7`; it does not leave the variable without a value.
</details>

<details>
<summary>Answer</summary>

Prints `0`.
</details>

### 12. An int{} expression

```cpp
int a{ 7 };
a = int{};
int b = int{};
std::cout << a << std::endl;
std::cout << b << std::endl;
```

<details>
<summary>Using int{} as a value</summary>

`int{}` is an expression with type `int` and value `0`. You can use it to change a variable or give a new variable its starting value. Here both `a` and `b` get `0`.
</details>

<details>
<summary>Answer</summary>

Prints `0` twice.
</details>

### 13. The `sizeof` operator
```cpp
std::cout << sizeof(int) << std::endl;
std::cout << sizeof(uint8_t) << std::endl;
int a;
std::cout << sizeof(a) << std::endl;
```

<details>
<summary>Finding a size in bytes</summary>

`sizeof` gives the size of a type or variable in bytes. Because `a` is an `int`, `sizeof(a)` equals `sizeof(int)`. It does not read the value of `a`, so the missing starting value is not a problem here. `uint8_t` takes one byte; the size of `int` can depend on the system.
</details>

<details>
<summary>Answer</summary>

On a system with a 4-byte `int`, prints `4`, `1`, and `4`. The first and last values depend on the size of `int`.
</details>

### 14. `auto`

What type will `a` have in this example?
```cpp
auto a = 5;
```

<details>
<summary>Letting the compiler choose the type</summary>

`auto` asks the compiler to choose the type from the starting expression. The number `5` has type `int`, so `a` gets type `int`. The type is chosen once and cannot change later.
</details>

<details>
<summary>Answer</summary>

`a` has type `int` and value `5`.
</details>

<details>
<summary>The type stays the same</summary>

Choosing the type automatically does not let it change later:
```cpp
auto a = 5;
a = "abc"; // error: a is still int
```
</details>

### 15. `auto` without initialization
```cpp
auto a;
a = 5;
```

<details>
<summary>auto needs a starting expression</summary>

The compiler must choose the type at `auto a;`, but there is no starting expression to choose it from. Assigning `5` on the next line is too late. Write `auto a = 5;` instead.
</details>

<details>
<summary>Answer</summary>

Does not compile.
</details>

### 16. `auto` with uniform initialization

```cpp
auto a{ 5 };
```

<details>
<summary>auto with braces</summary>

With one expression in these braces, `auto` chooses its type. Here `5` has type `int`, just as in `auto a = 5;`.
</details>

<details>
<summary>Answer</summary>

`a` has type `int` and value `5`.
</details>

### 17. `auto` from another variable
```cpp
int a{ 5 };
auto b{ a + 5 };
```

<details>
<summary>auto uses the whole expression</summary>

The starting expression does not have to be a number written directly in the code. Here `a + 5` adds two `int` values and gives `10`, also an `int`, so that is the type chosen for `b`.
</details>

<details>
<summary>Answer</summary>

`b` has type `int` and value `10`.
</details>

### 18. Swapping variables
```cpp
int a { 1 };
int b { 2 };
a = b;
b = a;
std::cout << a << std::endl;
std::cout << b << std::endl;
```

<details>
<summary>Overwriting loses the old value</summary>

`a = b` replaces the `1` in `a` with `2`. Then `b = a` copies that `2` into `b`. The original `1` has already been lost, so these assignments cannot swap the values.
</details>

<details>
<summary>Answer</summary>

Prints `2` twice; the values are not swapped.
</details>

<details>
<summary>How to actually swap the values</summary>

Save the old value of `a` before overwriting it:
```cpp
int temp{ a };
a = b;
b = temp;
```
</details>

[Numeric conversions](03_numeric_conversions.md) are covered in the next lab.
