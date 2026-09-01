# Lab 5

Topic: **Functions, function calls, and the stack**.

[Accompanying video 1](https://www.youtube.com/watch?v=jTRJM_gmhU4&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=5)

[Accompanying video 2](https://www.youtube.com/watch?v=jTRJM_gmhU4&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=7)

## Concepts

- Executable file (executable)
- Function
- Instruction address, Instruction Pointer
- Stack, Stack Pointer
- Return address
- Exiting a function
- Returning a value from a function
- Local variable

## Analysis 1

**Is it (technically) possible to overwrite a local variable from another function?**

Explain the code below (execution starts with the `main` function). 
This code will not compile as written; analyze it at a conceptual level.
`sp` means stack pointer.
Assume that local variables are stored on the stack and that the return address occupies 4 bytes.
What will the value of `x` be, and why?

```c
void f()
{
    *(sp - 8) = 0;
    return;
}

int main()
{
    int x;
    x = 1;
    f();
    return 0; // x = ?
}
```

<details>
<summary>Answer</summary>
The stack will look as follows.

1. Before the line that calls `f();`

| sp - 4 | sp |
| -----  | -- |
| x (1)  | ?? |

2. At the first line in `f`:

| sp - 8 | sp - 4                            | sp |
| -----  | ------                            | -- |
| x (1)  | return address to `return 0;` in `main` | ?? |

3. At the `return;` statement in `f`

| sp - 8 | sp - 4                            | sp |
| -----  | ------                            | -- |
| x (0)  | return address to `return 0;` in `main` | ?? |

4. At `return 0;` in `main`

| sp - 4 | sp |
| -----  | ------                            |
| x (0)  | return address from `main` |

</details>

While executing `f`, `sp - 8` points to the address of the local variable `x` in `main`.

Assuming that trying to return to instruction address 0 causes the program to crash (terminate with an error),
how can you make the program above crash by changing 1 character in the code?

<details>
<summary>Answer</summary>

Change `sp - 8` to `sp - 4`, which points to the return address.
This way, you can overwrite the return address with 0.
When attempting to return to this address, the program will crash.
</details>


> This is a common error in C, especially when working with arrays.
> It is also known as *stack corruption*.
> The compiler sometimes adds stack protection in debugging mode, 
> which helps find such errors (Google it if you are interested).


## Analysis 2

**Infinite recursion**

> Execution begins in the `main` function.

Explain what the program below will do:

```
void f()
{
    f();
    return;
}
int main()
{
    f();
    return 0;
}
```

> When `sp` moves beyond the limits of the stack (beyond the maximum address allocated to the stack),
> a stack overflow occurs. The program usually crashes.
