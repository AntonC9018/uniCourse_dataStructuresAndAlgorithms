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

### 2. `std::optional<int>`
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
