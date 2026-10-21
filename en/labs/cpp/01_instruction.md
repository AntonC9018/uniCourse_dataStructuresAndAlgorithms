---
slug: en/cpp/labs/instruction
---
<!-- course-site-backlink:start -->
[This lesson on the website](https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms/en/cpp/labs/instruction/)
<!-- course-site-backlink:end -->
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
<summary>Where the program starts</summary>

The program starts by running `main`. The code inside its curly braces is its body. Here the body is empty, so there is nothing to print.
</details>

<details>
<summary>Answer</summary>

Compiles and prints nothing.
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
<summary>Printing text</summary>

`std::cout <<` sends text to the console. Before using it, add `#include <iostream>` at the top of the file. This example is missing that line.
</details>

<details>
<summary>Answer</summary>

Does not compile.
</details>

<details>
<summary>Where the name cout comes from</summary>

`std` is short for “standard”; `std::` points to a name from the standard library. In `cout`, `c` stands for “console” and `out` for “output”. You can think of `<<` as pushing the following value into `std::cout`.
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
<summary>Ending a line</summary>

`std::cout` prints the text, and `std::endl` ends the line, like pressing Enter. Here these two steps run in order inside `main`.
</details>

<details>
<summary>Answer</summary>

Compiles and prints `Hello world`, followed by a newline.
</details>

<details>
<summary>One more thing about endl</summary>

`endl` is short for “end line”. It also sends any waiting output to the screen right away.
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
<summary>Printing several things in one statement</summary>

You can put several `<<` operations in one statement. They print in order. Here this is the same as:
```cpp
std::cout << "Hello world";
std::cout << std::endl;
```
</details>

<details>
<summary>Answer</summary>

Compiles and prints `Hello world`, followed by a newline.
</details>

### 5. Empty function `A`
```cpp
void A()
{
}
```

<!-- Nothing, A, void, 0, compilation error, runtime error -->

<details>
<summary>A program needs main</summary>

Defining `A` does not tell the program where to start. A complete program needs a function named `main`. This code defines only `A`.
</details>

<details>
<summary>Answer</summary>

Cannot build a complete program: `main` is missing.
</details>

<details>
<summary>If the error mentions ld</summary>

Building a program includes a step called linking. This is where the missing `main` is reported. `ld` is the name of the tool doing that step. Linking is covered later.
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
<summary>Including iostream</summary>

The compiler needs `#include <iostream>` before it can recognize `std::cout` and `std::endl`. This line is missing here. After adding it, you will also need `main` to make a complete program.
</details>

<details>
<summary>Answer</summary>

Does not compile.
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
<summary>A function does not run by itself</summary>

Including `<iostream>` makes the printing code recognizable, but it does not start `A`. The program still needs `main`, which can call `A`.
</details>

<details>
<summary>Answer</summary>

Cannot build a complete program: `main` is missing.
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
<summary>Running the code in main</summary>

This time `<iostream>` is included and `main` is defined. When the program starts, the statement inside `main` prints the text and ends the line.
</details>

<details>
<summary>Answer</summary>

Compiles and prints `Hello World.`, followed by a newline.
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
<summary>Uppercase and lowercase letters matter</summary>

C++ treats `Main` and `main` as different names. The program needs `main`, with a lowercase `m`; defining `Main` does not replace it.
</details>

<details>
<summary>Answer</summary>

Cannot build a complete program: `main` is missing.
</details>

### 10. `COUT` instead of `cout`
```cpp
#include <iostream>

int main()
{
    std::COUT << "Hello World." << std::endl;
}
```

<!-- Nothing, A, void, 0, Hello World, compilation error, runtime error -->

<details>
<summary>Use the exact name</summary>

The printing name is `std::cout`, all lowercase. `std::COUT` is a different name that the compiler does not recognize.
</details>

<details>
<summary>Answer</summary>

Does not compile.
</details>

### 11. Comment
```cpp
#include <iostream>

int main()
{
    // std::cout << "Hello" << std::endl;
    std::cout << "World" << std::endl;
}
```

<details>
<summary>Comments are ignored</summary>

`//` starts a comment that continues to the end of the line. The compiler ignores that text. Here the line printing `Hello` is a comment, so only the line printing `World` runs.
</details>

<details>
<summary>Answer</summary>

Prints only `World`, followed by a newline.
</details>

### 12. Everything commented out
```cpp
int main()
{
    // std::cout << "Hello" << std::endl;
    // std::cout << "World" << std::endl;
}
```

<details>
<summary>Commented code does not need to compile</summary>

Both printing lines are comments. The compiler sees an empty `main`, so it does not need `<iostream>` for this code.
</details>

<details>
<summary>Answer</summary>

Compiles and prints nothing.
</details>

### 13. A function calls a function
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
<summary>Calling a function still needs a starting point</summary>

`B` can call `A`, but neither function starts automatically. Without `main`, there is nowhere for the program to start.
</details>

<details>
<summary>Answer</summary>

Cannot build a complete program: `main` is missing.
</details>

### 14. `main` calls a function that calls a function
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
<summary>What happens during a function call</summary>

Statements run in order. When one function calls another, it waits for that function to finish, then continues after the call. Here `main` calls `B`; `B` prints `B-before`, calls `A`, then prints `B-after`.
</details>

<details>
<summary>Answer</summary>

Compiles and prints:
```text
B-before
A
B-after
```
</details>

### 15. Almost the same situation
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
<summary>Put the function before its call</summary>

The compiler reads the file from top to bottom. It needs to know about a function before reaching a call to it. Here `B` calls `A` before `A` is defined. Moving `A` above `B` fixes this.
</details>

<details>
<summary>Answer</summary>

Does not compile.
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
