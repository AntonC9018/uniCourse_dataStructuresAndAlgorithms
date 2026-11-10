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
- Sentinel values (`-1` for no index, `std::string::npos`)
- Pointers already hold null (`nullptr`)

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

### 8. A sentinel value instead of an optional
```cpp
#include <array>
#include <iostream>

const int NO_INDEX = -1;

int findIndex(std::array<int, 4> arr, int target)
{
    for (int i = 0; i < 4; i++)
    {
        if (arr[i] == target)
        {
            return i;
        }
    }
    return NO_INDEX;
}

int main()
{
    std::array<int, 4> arr{ 5, 8, 2, 8 };
    int a{ findIndex(arr, 8) };
    int b{ findIndex(arr, 7) };

    std::cout << a << std::endl;

    if (b == NO_INDEX)
    {
        std::cout << "not found" << std::endl;
    }
}
```

<details>
<summary>Answer</summary>

An index can never be negative, so one impossible value, `-1`,
can be reserved to mean “no index”.
Such a reserved value is called a *sentinel value*.
It needs no extra flag: the empty state is stored in the `int` itself.

- `8` is first found at index `1`, so `a` is `1`;
- `7` is not in the array, so `b` is `NO_INDEX`.

It prints `1` and `"not found"`.

The downside is that nothing forces the caller to check:
`arr[b]` would compile and read outside the array (UB).
</details>

### 9. `std::string::npos`
```cpp
#include <iostream>
#include <string>

int main()
{
    std::string s{ "hello" };
    size_t a{ s.find('l') };
    size_t b{ s.find('z') };

    std::cout << a << std::endl;

    if (b == std::string::npos)
    {
        std::cout << "not found" << std::endl;
    }
}
```

<details>
<summary>Answer</summary>

The standard library uses sentinel values too.
`find` returns the index of the first matching character,
or `std::string::npos` if there is none.

The index type `size_t` is unsigned, so `-1` cannot be used.
`npos` is the largest `size_t` value instead
(it is in fact defined as `-1` converted to `size_t`).
No string can be that long, so this index is impossible too.

It prints `2` and `"not found"`.

`std::optional` has no way to choose a sentinel value:
`std::optional<size_t>` always stores a separate flag next to the value.
</details>

### 10. When there is no free value for a sentinel
```cpp
#include <iostream>

const int NO_VALUE = -1;

int divide(int a, int b)
{
    if (b == 0)
    {
        return NO_VALUE;
    }
    return a / b;
}

int main()
{
    std::cout << divide(7, 0) << std::endl;
    std::cout << divide(-7, 7) << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `-1` twice.
The caller cannot tell the error apart from a real result:
any `int` can be the result of a division, so no value is left free for the sentinel.
Here an optional is needed, as in the `divide` examples above.

A sentinel only works when some value of the type is impossible as a real result,
like a negative index.
</details>

### 11. A pointer can already hold null
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
