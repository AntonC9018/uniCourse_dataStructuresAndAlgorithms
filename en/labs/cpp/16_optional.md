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
#include <iostream>

struct OptionalInt
{
    bool has_value;
    int value;
};

const OptionalInt NO_VALUE{ false, 0 };

int main()
{
    OptionalInt arr[3]{ { true, 1 }, NO_VALUE, { true, 3 } };

    int i{ 0 };
    while (i < 3)
    {
        if (arr[i].has_value)
        {
            std::cout << arr[i].value << std::endl;
        }
        else
        {
            std::cout << "empty" << std::endl;
        }
        i = i + 1;
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

`std::optional<int>` is the standard version of the custom struct from the previous example.
It either holds an `int` or holds nothing.

- `a` holds a value: `std::optional<int>{ 5 }` stores `5`,
  so `has_value()` is `true` and `value()` gives `5`.
- `b` is empty: `std::nullopt` means “no value”,
  so `has_value()` is `false`, `value()` must not be used,
  and `"empty"` is printed instead.

It prints `5` and `"empty"`.
</details>

### 6. A constant for the empty value (`std::optional`)
```cpp
#include <iostream>
#include <optional>

const std::optional<int> NO_VALUE{ std::nullopt };

int main()
{
    std::optional<int> a{ 5 };
    std::optional<int> b{ NO_VALUE };

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

This is the standard-type version of the custom constant from the earlier example:
`NO_VALUE` is an empty `std::optional<int>`.

It prints `5` and `"empty"`.
</details>

### 7. A function returning an optional (`std::optional`)
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

### 8. An array of optionals (`std::optional`)
```cpp
#include <iostream>
#include <optional>

const std::optional<int> NO_VALUE{ std::nullopt };

int main()
{
    std::optional<int> arr[3]{ 1, NO_VALUE, 3 };

    int i{ 0 };
    while (i < 3)
    {
        if (arr[i].has_value())
        {
            std::cout << arr[i].value() << std::endl;
        }
        else
        {
            std::cout << "empty" << std::endl;
        }
        i = i + 1;
    }
}
```

<details>
<summary>Answer</summary>

This is the same loop as in the custom example, but with the standard type.
A plain `1` becomes an `std::optional<int>` holding `1` automatically.

It prints `1`, `"empty"`, `3`.
</details>
