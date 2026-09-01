# Basic syntax: statements

- [Video about statements](https://www.youtube.com/watch?v=Z8AFpeE7hOo&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=5)

## Concepts

- Source file
- Compiling and running a program
- Program statements
- Order of statement execution
- Console output statement
- Functions without parameters
- The special `main` function
- Function body
- Empty function
- Comments
- Order of definitions in a program

## Analysis tasks

What will happen when these code snippets are compiled and run?

### 1. Empty `main`

```cpp
int main()
{
}
```

<!-- Nothing, main, int, 1, compilation error, runtime error -->

<details>
<summary>Answer</summary>

This program will compile successfully.

The `main` function will run automatically when this program is started.

The function itself contains no statements in its body (the curly braces are empty).
For this reason, running `main` will print nothing.
</details>

### 2. Printing a string
```cpp
int main()
{
    std::cout << "Hello world";
    std::cout << std::endl;
}
```

<details>
<summary>Intuition for <code>std::cout &lt;&lt;</code></summary>

`std` is short for *standard*.
You can think of `std::` as indicating a name from the standard library.

The name `cout` combines:
- `c` stands for the word "console";
- `out` is short for "output", as in output to the console.

`<<` sort of **pushes** the following string into `std::cout`.
</details>

<details>
<summary>Answer</summary>

This program will not compile.
A compilation error will occur because 
there is no `#include <iostream>` line before `int main()` 
(the `<iostream>` header is not included).
Without this line, the compiler does not know what `std::cout` is.
</details>

### 3. Corrected code for printing a string
```cpp
#include <iostream>

int main()
{
    std::cout << "Hello world";
    std::cout << std::endl;
}
```

<details>
<summary>Answer</summary>

This program will compile.
When it runs, the statements in the `main` function will execute,
printing "Hello world".
</details>

### 4. Printing on the same line
```cpp
#include <iostream>

int main()
{
    std::cout << "Hello world" << std::endl;
}
```

<details>
<summary>Answer</summary>

This code is equivalent to the following:
```cpp
std::cout << "Hello world";
std::cout << std::endl;
```
</details>

### 5. Empty function `A`
```cpp
void A()
{
}
```

<!-- Nothing, A, void, 0, compilation error, runtime error -->

<details>
<summary>Answer</summary>

The source code will compile, but the program will not link successfully because there is no `main` function
(the linking stage will be covered in more detail in a later lesson).

```
(.text+0x1b): undefined reference to `main'
collect2: error: ld returned 1 exit status
```

`ld` is the name of the linker program.
</details>

### 6. Function `A`
```cpp
void A()
{
    std::cout << "Hello World." << std::endl;
}
```

<!-- Nothing, A, void, 0, Hello World, compilation error, runtime error -->

<details>
<summary>Answer</summary>

A compilation error will occur because the `<iostream>` header is not included
(there is no `#include <iostream>` line).
The compiler does not know what `std::cout` is.

```
test.cpp: In function ‘void A()’:
test.cpp:3:10: error: ‘cout’ is not a member of ‘std’
    3 |     std::cout << "Hello World";
      |          ^~~~
test.cpp:1:1: note: ‘std::cout’ is defined in header ‘<iostream>’; did you forget to ‘#include <iostream>’?
  +++ |+#include <iostream>
    1 | void A()
```

To fix this, add `#include <iostream>` as the first line.
</details>

### 7. Corrected function `A`
```cpp
#include <iostream>

void A()
{
    std::cout << "Hello World." << std::endl;
}
```

<!-- Nothing, A, void, 0, Hello World, compilation error, runtime error -->

<details>
<summary>Answer</summary>

The source code will compile, but the program will not link because there is no `main` function. [See question 1](#1-empty-main)
</details>

### 8. Function `main`
```cpp
#include <iostream>

int main()
{
    std::cout << "Hello World." << std::endl;
}
```

<!-- Nothing, A, void, 0, Hello World, compilation error, runtime error -->

<details>
<summary>Answer</summary>

The program will compile successfully:
- the `main` function is defined;
- the `<iostream>` header is included before `std::cout` is used.

When run, it will print "Hello World."
</details>

### 9. Function `Main`
```cpp
#include <iostream>

int Main()
{
    std::cout << "Hello World." << std::endl;
}
```

<!-- Nothing, A, void, 0, Hello World, compilation error, runtime error -->

<details>
<summary>Answer</summary>

C++ is case-sensitive for function names and the names of other entities.
There is no `main` function, so the program will not link, just as in [the earlier example](#5-пустая-функция-A).
</details>

### 10. Comment
```cpp
#include <iostream>

int main()
{
    // std::cout << "Hello" << std::endl;
    std::cout << "World" << std::endl;
}
```

<details>
<summary>Answer</summary>

Only World will be printed.
The line that prints Hello is commented out (`//` at the beginning), so it will not execute.
</details>

### 11. Everything commented out
```cpp
int main()
{
    // std::cout << "Hello" << std::endl;
    // std::cout << "World" << std::endl;
}
```

<details>
<summary>Answer</summary>

It will compile without any issues.
Comments are ignored during compilation, so
the compiler does not need to know about `std::cout`.

When run, it will print nothing.
</details>

### 12. A function calls a function
```cpp
#include <iostream>

void A()
{
    std::cout << "Hello World" << std::endl;
}
void B()
{
    A();
}
```

<details>
<summary>Answer</summary>

The source code will compile, but the program will not link because there is no `main` function.
</details>

### 13. `main` calls a function that calls a function
```cpp
#include <iostream>

void A()
{
    std::cout << "A" << std::endl;
}
void B()
{
    std::cout << "B-before" << std::endl;
    A();
    std::cout << "B-after" << std::endl;
}
int main()
{
    B();
}
```

<details>
<summary>Answer</summary>

The program will compile successfully.

The statements execute in this order:
```
B(); // функцию вызвали
std::cout << "B-before" << std::endl;
A(); // функцию вызвали
std::cout << "A" << std::endl;
// A завершилась
std::cout << "B-after" << std::endl;
// B завершилась
```
</details>

### 14. Almost the same situation
Identify the difference between this example and the previous one.
What changed, and will it change the outcome?

```cpp
#include <iostream>

void B()
{
    std::cout << "B-before" << std::endl;
    A();
    std::cout << "B-after" << std::endl;
}
void A()
{
    std::cout << "A" << std::endl;
}
int main()
{
    B();
}
```

<details>
<summary>Answer</summary>

This program will not compile.
The call to `A();` in function `B` appears **before the definition of function `A` in the source file**.

Calling `B();` in the `main` function does not cause the same problem because
**function `B` is defined before it is called**.

In this example, `A` must be defined before `B` calls it.
</details>

## Practice

- Write a program that prints `"Jello"` to the console.

- *Define* a function `A` that prints `A`. Call it in the `main` function.
  <details>
  <summary>Hint</summary>

  A function definition uses the following syntax.

  ```cpp
  void A()
  {
  }
  ```

  A function call looks like this:
  ```cpp
  A();
  ```

  The function definition must come before the function call.
  The following code will not work:

  ```cpp
  int main()
  {
      A()
  }
  void A()
  {
  }
  ```

  Correct code:

  ```cpp
  void A()
  {
      std::cout << "A";
      std::cout << std::endl;
  }
  int main()
  {
      A()
  }
  ```
  </details>

- Define 3 functions: `A`, `B`, `C`.
  Function `A` must call functions `B` and `C`.
  Each of `A`, `B`, and `C` must print a message
  indicating that it has been called (for `A`, use `"called A"`).
