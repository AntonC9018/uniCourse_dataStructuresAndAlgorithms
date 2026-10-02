---
slug: en/cpp/labs/errors
---
<!-- course-site-backlink:start -->
[This lesson on the website](https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms/en/cpp/labs/errors/)
<!-- course-site-backlink:end -->
# Errors

- [Validation and ways to report errors](../../07_serialization/doc.md#validation)

## Concepts

- Expected failures and programming mistakes
- Bool success status and printed diagnostics
- Enum failure kinds
- Output values through pointer and reference parameters
- Null pointers, custom result structures, and `std::optional`
- Collecting multiple errors in a vector passed by reference
- Assertions: assumptions, termination, tests, and disabled checks

## Comprehension questions

For each example, predict its output and whether execution reaches the end.
What tells the caller that the operation succeeded? When is the returned or output value meaningful?

Each code block is a separate program. Unless an example explicitly says otherwise, assertions are enabled.

### 1. Returning a bool

```cpp
#include <iostream>

bool isValidAmount(int amount)
{
    return amount >= 0;
}

int main()
{
    std::cout << isValidAmount(3) << std::endl;
    std::cout << isValidAmount(-1) << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `1` and `0`: without `std::boolalpha`, these are the printed forms of `true` and `false`.
The function uses `true` to mean success and `false` to mean failure.
That convention belongs to this interface; the type `bool` itself does not prescribe what either value means.
A bool communicates whether validation succeeded, but not the kind of failure.
</details>

### 2. Printing an error

```cpp
#include <iostream>

bool isValidAmount(int amount)
{
    if (amount < 0)
    {
        std::cerr << "amount must not be negative" << std::endl;
        return false;
    }
    return true;
}

int main()
{
    bool valid = isValidAmount(-1);
    std::cout << valid << std::endl;
}
```

<details>
<summary>Answer</summary>

It writes `amount must not be negative` to standard error and `0` to standard output.
`std::cerr` is an output stream for diagnostics, used here in the same way as `std::cout`.
A terminal commonly shows both streams; their exact combined display depends on how they are captured.

The message tells a person what went wrong. The caller still receives only `false`, so printing does not provide a structured failure kind to other code.
</details>

### 3. Returning the failure kind

```cpp
#include <iostream>

enum class ValidationError
{
    None,
    NegativeAmount,
    NegativePrice,
};

ValidationError validateOrder(int amount, int price)
{
    if (amount < 0)
    {
        return ValidationError::NegativeAmount;
    }
    if (price < 0)
    {
        return ValidationError::NegativePrice;
    }
    return ValidationError::None;
}

int main()
{
    ValidationError result = validateOrder(-1, -2);
    std::cout << (result == ValidationError::NegativeAmount) << std::endl;
    std::cout << (result == ValidationError::NegativePrice) << std::endl;
    std::cout << (validateOrder(3, 4) == ValidationError::None) << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `1`, `0`, and `1`.
An enum lets the caller distinguish success from specific failure kinds without analyzing a message.
Although both arguments in the first call are invalid, the first `return` ends the function immediately.
Only `NegativeAmount` is reported; the price check is not reached.
</details>

### 4. A bool and an output pointer

```cpp
#include <iostream>

bool tryHalf(int input, int* output)
{
    if (input < 0)
    {
        return false;
    }
    *output = input / 2;
    return true;
}

int main()
{
    int value = 99;
    bool success = tryHalf(8, &value);
    std::cout << success << std::endl;
    std::cout << value << std::endl;

    success = tryHalf(-1, &value);
    std::cout << success << std::endl;
    std::cout << value << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `1`, `4`, `0`, and `4`.
The function returns its status and writes the computed value through the pointer parameter.
It accepts non-negative inputs and uses integer division.

On failure, it returns before assigning to `*output`, so this interface leaves the output value unchanged.
The second `4` is the result of the previous successful call, not a new result for `-1`.
Here, `output` must point to a valid integer object; it is not an optional parameter.
</details>

### 5. The same output through a reference

```cpp
#include <iostream>

bool tryHalf(int input, int& output)
{
    if (input < 0)
    {
        return false;
    }
    output = input / 2;
    return true;
}

int main()
{
    int value = 99;
    bool success = tryHalf(8, value);
    std::cout << success << std::endl;
    std::cout << value << std::endl;

    success = tryHalf(-1, value);
    std::cout << success << std::endl;
    std::cout << value << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints the same `1`, `4`, `0`, and `4`.
The reference parameter names the caller's integer, so assigning to `output` changes `value`.
At the call site, pass `value` instead of its address.
The success/failure contract is unchanged; a reference also cannot represent a missing output object with `nullptr`.
</details>

### 6. Ignoring the status

```cpp
#include <iostream>

bool tryHalf(int input, int& output)
{
    if (input < 0)
    {
        return false;
    }
    output = input / 2;
    return true;
}

int main()
{
    int value = 99;
    tryHalf(-1, value);
    std::cout << value << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `99`.
The call returns `false`, but that status is ignored.
`value` keeps its old value; treating it as a successfully computed result would be a logic error.
Use the output as a new result only after the status indicates success.
Here, `99` is an ordinary initialized value, so reading it is defined; it is simply not the requested result.
</details>

### 7. An enum and an output value

```cpp
#include <iostream>

enum class HalfError
{
    None,
    NegativeInput,
};

HalfError tryHalf(int input, int& output)
{
    if (input < 0)
    {
        return HalfError::NegativeInput;
    }
    output = input / 2;
    return HalfError::None;
}

int main()
{
    int value = 99;
    HalfError error = tryHalf(-1, value);
    if (error == HalfError::None)
    {
        std::cout << value << std::endl;
    }
    else if (error == HalfError::NegativeInput)
    {
        std::cout << "negative input" << std::endl;
    }
}
```

<details>
<summary>Answer</summary>

It prints `negative input`.
This combines the output-parameter pattern with an enum status.
`None` means success; other members explain failure.
The caller checks the status before treating the output as a result.
An enum becomes especially useful when more than one failure kind is possible.
</details>

### 8. A null pointer means failure

```cpp
#include <iostream>
#include <span>

int* findValue(std::span<int> values, int wanted)
{
    for (int& value : values)
    {
        if (value == wanted)
        {
            return &value;
        }
    }
    return nullptr;
}

int main()
{
    int values[]{ 3, 5, 7 };
    int* found = findValue(values, 5);
    if (found != nullptr)
    {
        *found = 6;
    }
    std::cout << values[1] << std::endl;

    int* missing = findValue(values, 9);
    std::cout << (missing == nullptr) << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `6` and `1`.
Success returns the address of an existing array element; failure returns `nullptr`.
The pointer must be checked before dereferencing it.
This reports whether a value was found, but not an additional failure kind.

The returned pointer refers to the caller's array, not a local copy inside `findValue`.
The array remains alive while `found` is used; the loop's reference variable refers to its actual element.
</details>

### 9. Returning a custom result structure

```cpp
#include <iostream>

struct HalfResult
{
    bool success;
    int value;
};

HalfResult tryHalf(int input)
{
    if (input < 0)
    {
        return { false, 0 };
    }
    return { true, input / 2 };
}

int main()
{
    HalfResult result = tryHalf(8);
    if (result.success)
    {
        std::cout << result.value << std::endl;
    }

    result = tryHalf(-1);
    if (result.success)
    {
        std::cout << result.value << std::endl;
    }
    else
    {
        std::cout << "failure" << std::endl;
    }
}
```

<details>
<summary>Answer</summary>

It prints `4` and `failure`.
The structure returns the status and the value together, without an output parameter.
The failure case initializes `value` to `0`, but that field is not a successful result when `success` is false.
This is the custom optional structure from the [optional lab](17_optional.md), applied to a fallible computation.
The status field could instead be an enum if the caller needed a failure kind.
</details>

### 10. Returning std::optional

```cpp
#include <iostream>
#include <optional>

std::optional<int> tryHalf(int input)
{
    if (input < 0)
    {
        return std::nullopt;
    }
    return input / 2;
}

int main()
{
    std::optional<int> result = tryHalf(8);
    if (result.has_value())
    {
        std::cout << *result << std::endl;
    }

    result = tryHalf(-1);
    if (result.has_value())
    {
        std::cout << *result << std::endl;
    }
    else
    {
        std::cout << "failure" << std::endl;
    }
}
```

<details>
<summary>Answer</summary>

It prints the same `4` and `failure`.
`std::optional<int>` expresses either an integer result or its absence.
`std::nullopt` supplies the empty state, and the caller checks `has_value()` before dereferencing.
Like a bool status, the empty state alone does not explain the failure kind.
</details>

### 11. Collecting multiple errors

```cpp
#include <iostream>
#include <vector>

enum class ValidationError
{
    None,
    NegativeAmount,
    NegativePrice,
};

bool validateOrder(int amount, int price, std::vector<ValidationError>& errors)
{
    bool valid = true;
    if (amount < 0)
    {
        errors.push_back(ValidationError::NegativeAmount);
        valid = false;
    }
    if (price < 0)
    {
        errors.push_back(ValidationError::NegativePrice);
        valid = false;
    }
    return valid;
}

int main()
{
    std::vector<ValidationError> errors;
    bool valid = validateOrder(-1, -2, errors);
    std::cout << valid << std::endl;
    std::cout << errors.size() << std::endl;
    for (ValidationError error : errors)
    {
        std::cout << static_cast<int>(error) << std::endl;
    }
}
```

<details>
<summary>Answer</summary>

It prints `0`, `2`, `1`, and `2`.
A `std::vector<ValidationError>` stores a list of error values; `push_back` appends one value and `size()` gives the current number of values.
The vector is passed by reference, so the function adds to the caller's list.

Unlike the earlier enum example, neither failure returns immediately.
Both checks run, recording `NegativeAmount` and `NegativePrice` in that order.
The returned bool describes whether this call found any errors.
</details>

### 12. Reusing the error list

```cpp
#include <iostream>
#include <vector>

enum class ValidationError
{
    None,
    NegativeAmount,
    NegativePrice,
};

bool validateOrder(int amount, int price, std::vector<ValidationError>& errors)
{
    bool valid = true;
    if (amount < 0)
    {
        errors.push_back(ValidationError::NegativeAmount);
        valid = false;
    }
    if (price < 0)
    {
        errors.push_back(ValidationError::NegativePrice);
        valid = false;
    }
    return valid;
}

int main()
{
    std::vector<ValidationError> errors;
    validateOrder(-1, -2, errors);
    bool valid = validateOrder(3, 4, errors);
    std::cout << valid << std::endl;
    std::cout << errors.size() << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `1` and `2`.
The second call succeeds, but it does not clear the errors recorded by the first call.
The function appends new errors; its returned bool concerns only the current validation.
An accumulating list can hold results from several validations.
If the caller wants a fresh list for each call, it should create a new vector or call `errors.clear()` beforehand.
</details>

### 13. An assertion that passes

```cpp
#include <iostream>
#include <cassert>

int main()
{
    int amount = 3;
    assert(amount >= 0);
    std::cout << amount << std::endl;
}
```

<details>
<summary>Answer</summary>

With assertions enabled, it prints `3`.
`assert` from `<cassert>` checks a condition expected to be true.
When the condition is true, execution continues.
Unlike a bool return value, an assertion does not report a recoverable failure to the caller.
</details>

### 14. An assertion that fails

```cpp
#include <iostream>
#include <cassert>

int main()
{
    int amount = -1;
    assert(amount >= 0);
    std::cout << "after assert" << std::endl;
}
```

<details>
<summary>Answer</summary>

With assertions enabled, the assertion fails, emits a diagnostic, and terminates the program by calling `std::abort`.
`after assert` is not printed. The exact diagnostic is implementation-dependent.
An assertion detects a violated assumption; it does not return `false` or give the caller a chance to choose an ordinary failure branch.

If `NDEBUG` is defined when compiling, `assert` performs no check and does not evaluate its expression.
Then this program prints `after assert`.
Do not use assertions as the only validation of expected bad input.
</details>

### 15. An assertion for an output-parameter contract

```cpp
#include <iostream>
#include <cassert>

bool tryHalf(int input, int* output)
{
    assert(output != nullptr);
    if (input < 0)
    {
        return false;
    }
    *output = input / 2;
    return true;
}

int main()
{
    int value = 99;
    bool success = tryHalf(-1, &value);
    std::cout << success << std::endl;
    std::cout << value << std::endl;

    success = tryHalf(8, &value);
    std::cout << success << std::endl;
    std::cout << value << std::endl;
}
```

<details>
<summary>Answer</summary>

With assertions enabled, it prints `0`, `99`, `1`, and `4`.
Passing a valid output object is a requirement of this interface.
The assertion checks that the caller did not pass `nullptr`; both calls satisfy that requirement.
A null pointer would be a programming mistake under this contract, not another supported failure result.

A negative input is an expected failure and is reported with `false`, so the program can continue.
If assertions are disabled, the caller still must satisfy the output-pointer requirement.
This illustrates why assertions and ordinary error reporting serve different purposes.
</details>

### 16. Checking success and failure with assertions

```cpp
#include <iostream>
#include <cassert>

bool tryHalf(int input, int& output)
{
    if (input < 0)
    {
        return false;
    }
    output = input / 2;
    return true;
}

int main()
{
    int value = 99;
    bool success = tryHalf(8, value);
    assert(success);
    assert(value == 4);

    success = tryHalf(-1, value);
    assert(!success);
    assert(value == 4);
    std::cout << "tests passed" << std::endl;
}
```

<details>
<summary>Answer</summary>

With assertions enabled, it prints `tests passed`.
The assertions check both the successful result and the promised unchanged output on failure.
A mismatch would stop the program at the failed check.

The calls to `tryHalf` are separate from the assertions, so those calls still execute if assertions are disabled.
Do not place required work only inside `assert`, because its expression may not be evaluated.
With checks disabled, the printed message alone does not establish that the results were verified.
</details>

[Tagged unions and flags](32_tagged_unions_and_flags.md) and [exceptions](33_exceptions.md) have separate later labs.
