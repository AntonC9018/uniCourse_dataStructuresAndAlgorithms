---
slug: en/cpp/labs/optional
---
<!-- course-site-backlink:start -->
[This lesson on the website](https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms/en/cpp/labs/optional/)
<!-- course-site-backlink:end -->
# `std::optional`

## Concepts

- A value that may be missing
- Custom optional struct (`has_value` + `value`)
- `std::optional<int>`
- Empty state vs holding a value
- `std::nullopt`, `has_value()`
- A constant for the empty value
- Returning an optional from a function
- Arrays of optionals
- Pointers already hold null (`nullptr`)
- References cannot be null

## Examples to aid understanding

### 1. Custom optional struct
```cpp
#include <iostream>

struct OptionalInt
{
    bool has_value;
    int value;
};

int main()
{
    OptionalInt a{ true, 5 };
    OptionalInt b{ false, 0 };

    if (a.has_value)
    {
        std::cout << a.value << std::endl;
    }

    if (b.has_value)
    {
        std::cout << b.value << std::endl;
    }
    else
    {
        std::cout << "empty" << std::endl;
    }
}
```

<details>
<summary>Answer</summary>

Sometimes a value may be missing, and this needs to be represented explicitly.
Here, `has_value` says whether `value` is meaningful.

- `a` holds a value: `has_value` is `true`, so `a.value` (`5`) is printed.
- `b` is empty: `has_value` is `false`, so `b.value` (`0`) is ignored
  and `"empty"` is printed instead.

This pair of a flag plus a value is the whole idea behind an optional.
</details>

### 2. A constant for the empty value
```cpp
#include <iostream>

struct OptionalInt
{
    bool has_value;
    int value;
};

const OptionalInt NO_VALUE{ false, 0 };

int main()
{
    OptionalInt a{ true, 5 };
    OptionalInt b{ NO_VALUE };

    if (a.has_value)
    {
        std::cout << a.value << std::endl;
    }

    if (b.has_value)
    {
        std::cout << b.value << std::endl;
    }
    else
    {
        std::cout << "empty" << std::endl;
    }
}
```

<details>
<summary>Answer</summary>

Give the empty state a name, so that every empty optional is written the same way.
`NO_VALUE` holds `has_value = false`, and the `0` in it is never read —
it is there only because `value` must contain something.

`b` is initialized from the constant, so it is empty just like in the previous example.

It prints `5` and `"empty"`.
</details>

### 3. A function returning an optional
```cpp
#include <iostream>

struct OptionalInt
{
    bool has_value;
    int value;
};

const OptionalInt NO_VALUE{ false, 0 };

OptionalInt divide(int a, int b)
{
    if (b == 0)
    {
        return NO_VALUE;
    }
    return OptionalInt{ true, a / b };
}

int main()
{
    OptionalInt a{ divide(7, 2) };
    OptionalInt b{ divide(7, 0) };

    if (a.has_value)
    {
        std::cout << a.value << std::endl;
    }

    if (b.has_value)
    {
        std::cout << b.value << std::endl;
    }
    else
    {
        std::cout << "empty" << std::endl;
    }
}
```

<details>
<summary>Answer</summary>

A function can return an optional to signify a missing result.
Division by zero has no result, so `divide` returns `NO_VALUE` in that case.

- `divide(7, 2)` returns an optional holding `3`;
- `divide(7, 0)` returns the empty constant, so `"empty"` is printed instead.

It prints `3` and `"empty"`.
</details>

### 4. An array of optionals
```cpp
#include <array>
#include <iostream>

struct OptionalInt
{
    bool has_value;
    int value;
};

const OptionalInt NO_VALUE{ false, 0 };

int main()
{
    std::array<OptionalInt, 3> arr{
        { true, 1 },
        NO_VALUE,
        { true, 3 },
    };

    for (OptionalInt el : arr)
    {
        if (el.has_value)
        {
            std::cout << el.value << std::endl;
        }
        else
        {
            std::cout << "empty" << std::endl;
        }
    }
}
```

<details>
<summary>Answer</summary>

Each element is checked in turn: if it holds a value, the value is printed,
otherwise `"empty"` is printed.

It prints `1`, `"empty"`, `3`.
</details>

### 5. `std::optional<int>`
```cpp
#include <iostream>
#include <optional>

int main()
{
    std::optional<int> a{ 5 };
    std::optional<int> b{ std::nullopt };

    if (a.has_value())
    {
        std::cout << a.value() << std::endl;
    }

    if (b.has_value())
    {
        std::cout << b.value() << std::endl;
    }
    else
    {
        std::cout << "empty" << std::endl;
    }
}
```

<details>
<summary>Answer</summary>

`std::optional<int>` is the standard version of the custom struct from the earlier examples.
It either holds an `int` or holds nothing.

- `a` holds a value: `std::optional<int>{ 5 }` stores `5`,
  so `has_value()` is `true` and `value()` gives `5`.
- `b` is empty: `std::nullopt` means “no value”,
  so `has_value()` is `false`, `value()` must not be used,
  and `"empty"` is printed instead.

It prints `5` and `"empty"`.
</details>


### 6. A function returning an optional (`std::optional`)
```cpp
#include <iostream>
#include <optional>

std::optional<int> divide(int a, int b)
{
    if (b == 0)
    {
        return std::nullopt;
    }
    return a / b;
}

int main()
{
    std::optional<int> a{ divide(7, 2) };
    std::optional<int> b{ divide(7, 0) };

    if (a.has_value())
    {
        std::cout << a.value() << std::endl;
    }

    if (b.has_value())
    {
        std::cout << b.value() << std::endl;
    }
    else
    {
        std::cout << "empty" << std::endl;
    }
}
```

<details>
<summary>Answer</summary>

This is the same `divide` as in the custom example, but with the standard type.
Division by zero returns `std::nullopt`.

Note that `return a / b;` needs no braces: a plain `int` becomes
an `std::optional<int>` holding that value automatically.

It prints `3` and `"empty"`.
</details>

### 7. An array of optionals (`std::optional`)
```cpp
#include <array>
#include <iostream>
#include <optional>

int main()
{
    std::array<std::optional<int>, 3> arr{
        1,
        std::nullopt,
        3,
    };

    for (std::optional<int> x : arr)
    {
        if (x.has_value())
        {
            std::cout << x.value() << std::endl;
        }
        else
        {
            std::cout << "empty" << std::endl;
        }
    }
}
```

<details>
<summary>Answer</summary>

This is the same loop as in the custom example, but with the standard type.
A plain `1` becomes an `std::optional<int>` holding `1` automatically.

It prints `1`, `"empty"`, `3`.
</details>

### 8. A pointer can already hold null
```cpp
#include <iostream>

int main()
{
    int a{ 5 };
    int* p{ &a };
    int* q{ nullptr };

    if (p != nullptr)
    {
        std::cout << *p << std::endl;
    }

    if (q != nullptr)
    {
        std::cout << *q << std::endl;
    }
    else
    {
        std::cout << "empty" << std::endl;
    }
}
```

<details>
<summary>Answer</summary>

Pointers already have a built-in empty state — `nullptr`.
They need no extra flag like `has_value`.

- `p` points at `a`, so the check passes and `5` is printed;
- `q` holds `nullptr`, so the check fails and `"empty"` is printed instead.

It prints `5` and `"empty"`.
</details>

### 9. A reference cannot hold null
```cpp
int main()
{
    int& x{ nullptr };
}
```

<details>
<summary>Answer</summary>

This will not compile: a reference must be bound to a real variable of type `int`,
and `nullptr` is not one. References have no empty state.
</details>

### 10. Taking the address of `nullptr`
```cpp
int main()
{
    int& x{ &nullptr };
}
```

<details>
<summary>Answer</summary>

This will not compile either: `&` can only be applied to a variable,
and `nullptr` is not a variable, so its address cannot be taken.
</details>

### 11. A reference bound to null is UB
```cpp
#include <iostream>

int main()
{
    int* a = nullptr;
    int& x{ *a };
    std::cout << x << std::endl;
}
```

<details>
<summary>Answer</summary>

This compiles, but it is UB: `*a` follows a null address.
Creating the reference already dereferences null,
so anything can happen (usually a crash).
Unlike an optional, there is nothing to check — the error is not represented in any way.

Note that writing `&a` here would not compile at all:
`&a` is an `int**`, not an `int`.
</details>

### 12. `std::optional` for pointers is pointless

`std::optional` for pointers is pointless: pointers are allowed to hold null already,
and there is no way to express the opposite — a pointer guaranteed not to be null.
A reference should be used when wanting to pass a pointer guaranteed not to be null.

```cpp
#include <iostream>

void print(int* p)
{
    if (p != nullptr)
    {
        std::cout << *p << std::endl;
    }
}

void printRef(int& r)
{
    std::cout << r << std::endl;
}

int main()
{
    int a{ 5 };
    print(&a);
    print(nullptr);
    printRef(a);
}
```

<details>
<summary>Answer</summary>

Wrapping a pointer as `std::optional<int*>` adds nothing:
the pointer already expresses “maybe null” through `nullptr`.

And an optional cannot express “guaranteed not null” either.
That guarantee is what a reference gives: `printRef` needs no check,
because the caller is forced to pass a real variable.

It prints `5` twice: once from `print(&a)`, once from `printRef(a)`.
`print(nullptr)` prints nothing.
</details>
