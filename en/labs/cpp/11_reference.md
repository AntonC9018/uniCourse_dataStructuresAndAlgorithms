# References

## Concepts

- rvalue, lvalue
- Reference

## Comprehension questions

What will happen when this code is run? Why?

> Unless `main` is shown explicitly, assume the code appears in a typical main file:
> ```cpp
> #include <iostream>
> #include <array> // required for std::array
>
> int main()
> {
>     // here
> }
> ```

### 1. Assigning to a numeric literal
```cpp
5 = 6;
```

<details>
<summary>Answer</summary>

`5` is an rvalue, so it cannot appear on the left-hand side of an assignment.
</details>

### 2. Taking the address of a number
```cpp
int* a = &5;
```

<details>
<summary>Answer</summary>

You cannot take the address of an rvalue. 
You can take the address only of an lvalue (an expression that designates an object),
because a numeric literal does not designate an object in memory.
</details>

### 3. Taking the address of an expression
```cpp
int* a = &(5 + 6);
```

<details>
<summary>Answer</summary>

The situation is similar: `(5 + 6)` is an rvalue.
It is impossible to take the address of an rvalue.
</details>

### 4. Reference from a number
```cpp
int& a = 5;
```

<details>
<summary>Answer</summary>

An `int&` can bind only to an lvalue—an expression that designates an object—
because `a` must ultimately refer to an object in memory, not merely a value.
</details>

### 5. Reference from a variable
```cpp
int a = 5;
int& b = a;
std::cout << a << std::endl;
std::cout << b << std::endl;
```

<details>
<summary>Answer</summary>

Here, `b` is a *reference* to `a`.
The compiler may treat `b` as another name for `a`
or implement it internally using a pointer to `a`.

When reading a value, using the name `b` is equivalent to using the name `a`
—both names refer to the same object.
Unlike `b`, `a` is an object. When its declaration is executed,
storage is allocated for it, typically on the stack.

`5` will be printed 2 times.
</details>

### 6. Assigning a number to a reference
```cpp
int a = 5;
int& b = a;
b = 6;
std::cout << a << std::endl;
```

<details>
<summary>Answer</summary>

Here, `a` will be overwritten with `6` through the name `b`.
</details>

### 7. Overwriting a variable that has a reference
```cpp
int a = 5;
int& b = a;
a = 6;
std::cout << b << std::endl;
```

<details>
<summary>Answer</summary>

`a` is overwritten directly.

Since `b` is a *reference* to `a`, reading from `b` reads from `a`.
</details>


### 8. Reference from an expression
```cpp
int a = 5;
int& b = a + 7;
std::cout << a << std::endl;
std::cout << b << std::endl;
```

<details>
<summary>Answer</summary>

`a + 7` is an rvalue, not an lvalue.
Since a non-const lvalue reference cannot bind to an rvalue, this code will not compile.
</details>

### 9. Assignment operator applied to a reference
```cpp
int a = 5;
int& b = a;
b += 7;
std::cout << a << std::endl;
std::cout << b << std::endl;
```

<details>
<summary>Answer</summary>

`b += 7` updates `a` because `b` refers to `a`.

The same value will be printed for both variables (`12`).
</details>

### 10. Assigning a variable to a reference
```cpp
int a = 1;
int b = 2;
int& c = a;
c = b;
std::cout << a << std::endl;
std::cout << b << std::endl;
std::cout << c << std::endl;
```

<details>
<summary>Answer</summary>

`c = b` does not rebind the reference; a reference cannot be rebound.

In `c = b`, you can effectively replace `c` with the object it refers to (`a`),
giving `a = b`, which overwrites `a` with the value from `b`, `2`.

The output will be:
```
2
2
2
```

</details>

### 11. Overwriting the referenced variable after assigning through the reference
```cpp
int a = 1;
int b = 2;
int& c = a;
c = b;
c = 3;
std::cout << a << std::endl;
std::cout << b << std::endl;
std::cout << c << std::endl;
```

<details>
<summary>Answer</summary>

Unlike pointers, references cannot be "redirected".

This illustrates that `c` continues to refer to `a`,
even after the line `c = b`.

The output will be:
```
3
2
3
```
</details>

### 12. Reference from a dereference
```cpp
int a = 1;
int* pa = &a;
int& b = *pa;
*pa = 2;
b = 3;
std::cout << a << std::endl;
std::cout << b << std::endl;
std::cout << *pa << std::endl;
```

<details>
<summary>Answer</summary>

`int& b = *pa;` creates a reference to the object pointed to by `pa`.
All 3 expressions now refer to the same object, `a`.

`3` will be printed 3 times.
</details>

### 13. Reassigning a pointer after creating a reference from it
```cpp
int a = 1;
int b = 2;
int* p = &a;
int& r = *p;
p = &b;
r = 3;
std::cout << a << std::endl;
std::cout << b << std::endl;
```

<details>
<summary>Answer</summary>

Reassigning `p` does not change what `r` refers to, so `r = 3` changes `a`.
The output will be:
```
3
2
```
</details>

### 14. Overwriting a variable through an address and a reference
```cpp
int a = 1;
int& b = a;
int* c = &b;
*c = 2;
std::cout << a << std::endl;
```

<details>
<summary>Answer</summary>

You can also obtain an address from a reference.
Here, `*c = 2;` will overwrite `a`.
</details>


### 15. References to fields
```cpp
#include <iostream>

struct Position
{
    int x;
    int y;
};

int main()
{
    Position a{ .x = 1, .y = 2 };

    Position& ra = a;

    int& rx = ra.x;
    ra.x = 3;

    ra.y = 4;
    int& ry = ra.y;

    std::cout << rx << std::endl;
    std::cout << ry << std::endl;

    std::cout << ra.x << std::endl;
    std::cout << ra.y << std::endl;

    std::cout << a.x << std::endl;
    std::cout << a.y << std::endl;
}
```

<details>
<summary>Answer</summary>

References can be created to members of larger objects.

Here, `3` and `4` will be printed everywhere.
</details>

### 16. Reference to a pointer (1)
```cpp
int a = 1;
int b = 2;
int* pa = &a;
int*& rpa = pa;
pa = &b;
*rpa = 3;
std::cout << a << std::endl;
std::cout << b << std::endl;
```

<details>
<summary>Answer</summary>

You can create references to pointers because pointers are also objects that store addresses.

Here, we replace the address stored in `pa`.
The reference `rpa` reflects that change, so dereferencing it accesses `b`.

`*rpa` -> `*pa` -> `*(&b)` -> `b`

`a` will be `1`, and `b` will be `3`.
</details>

### 17. Reference to a pointer (2)
```cpp
int a = 1;
int b = 2;
int* pa = &a;
int*& rpa = pa;
pa = &b;
int& rb = *rpa;
rb = 3;

std::cout << a << std::endl;
std::cout << b << std::endl;
```

<details>
<summary>Answer</summary>

This illustrates that references can be bound to
any expression that ultimately yields an lvalue.

`rb = 3` will write `3` into `b`.
</details>

### 18. Size of a reference

Is it possible to obtain the size of a reference? What is the size of a reference?

```cpp
#include <iostream>

int main()
{
    int a = 6;
    int& b = a;
    std::cout << sizeof(b) << std::endl;
}
```

<details>
<summary>Answer</summary>

`sizeof(b)` works, but it gives the size of an `int`, not a reference.

The size of a reference itself cannot be obtained; its representation is an implementation detail.

Many compilers implement a reference parameter by passing an address, but this is also an implementation detail.
Such an address is commonly 8 bytes on modern platforms.

> A function needs information from outside its local scope to access a particular variable.
> Passing its address is a straightforward way to provide that information.
</details>

### 19. Example of using references (1)
```cpp
#include <iostream>

void resetAmount(int& amount)
{
    amount = 0;
}
int main()
{
    int appleAmount = 6;
    resetAmount(appleAmount);
    std::cout << appleAmount << std::endl;
}
```

<details>
<summary>Answer</summary>

`appleAmount` will be overwritten with `0` because a reference to it is passed to the function.

Many compilers implement this by passing the *address* of the `appleAmount` variable,
but that detail is hidden from you.
</details>

### 20. Example of using references (2)
```cpp
#include <iostream>

struct Arm
{
    int power;
};

void increasePower(Arm& arm)
{
    arm.power += 1;
}

int main()
{
    Arm arm { 1 };
    increasePower(arm);
    std::cout << arm.power << std::endl;
}
```

<details>
<summary>Answer</summary>

You can pass references to struct objects to a function.
Here, the function increases the power.
</details>
