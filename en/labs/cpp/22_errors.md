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

struct Printer
{
    bool jammed;
};

bool printPage(Printer& printer)
{
    if (printer.jammed)
    {
        return false;
    }
    std::cout << "page printed" << std::endl;
    return true;
}

int main()
{
    Printer printer{ true };
    bool printed = printPage(printer);
    std::cout << printed << std::endl;

    printer.jammed = false;
    printed = printPage(printer);
    std::cout << printed << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `0`, `page printed`, and `1`.
`Printer` models a printer, and `jammed` says whether paper is stuck in it.
The first request fails because the printer is jammed. After the jam is cleared, the second request prints a page and succeeds.

A bool tells the caller whether the operation succeeded, but not the failure kind.
This interface uses `true` for success and `false` for failure.
</details>

### 2. Printing an error

```cpp
#include <iostream>

struct Printer
{
    bool jammed;
};

bool printPage(Printer& printer)
{
    if (printer.jammed)
    {
        std::cerr << "printer is jammed" << std::endl;
        return false;
    }
    std::cout << "page printed" << std::endl;
    return true;
}

int main()
{
    Printer printer{ true };
    bool printed = printPage(printer);
    std::cout << printed << std::endl;
}
```

<details>
<summary>Answer</summary>

It writes `printer is jammed` to standard error and `0` to standard output.
In `std::cerr`, `err` stands for *error*. It is an output stream for diagnostics, used here in the same way as `std::cout`.

The message tells a person what went wrong, but the caller receives only `false`: the specific failure kind is lost in the return value.
Here that does not really matter, because the function checks only one thing: whether the printer is jammed.
If more checks were added, the bool alone would not identify which one failed.
</details>

### 3. Returning the failure kind

```cpp
#include <iostream>

enum class GradeError
{
    None,
    TooLow,
    TooHigh,
};

GradeError validateGrade(int grade)
{
    if (grade <= 0)
    {
        return GradeError::TooLow;
    }
    if (grade >= 10)
    {
        return GradeError::TooHigh;
    }
    return GradeError::None;
}

int main()
{
    std::cout << (validateGrade(0) == GradeError::TooLow) << std::endl;
    std::cout << (validateGrade(10) == GradeError::TooHigh) << std::endl;
    std::cout << (validateGrade(5) == GradeError::None) << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `1`, `1`, and `1`.
This interface accepts a grade strictly greater than `0` and strictly less than `10`.
A single parameter is checked in two ways: `0` is too low, `10` is too high, and `5` is valid.
The enum communicates the specific failure kind, so the caller can distinguish the two failed checks without analyzing a message.
</details>

### 4. A printer with two failure kinds

```cpp
#include <iostream>

struct Printer
{
    bool jammed;
    int pagesLoaded;
};

enum class PrintError
{
    None,
    Jammed,
    NoPaper,
};

PrintError printPage(Printer& printer)
{
    if (printer.jammed)
    {
        return PrintError::Jammed;
    }
    if (printer.pagesLoaded == 0)
    {
        return PrintError::NoPaper;
    }
    printer.pagesLoaded -= 1;
    return PrintError::None;
}

int main()
{
    Printer printer{ true, 0 };
    PrintError error = printPage(printer);
    std::cout << (error == PrintError::Jammed) << std::endl;

    printer.jammed = false;
    error = printPage(printer);
    std::cout << (error == PrintError::NoPaper) << std::endl;

    printer.pagesLoaded = 1;
    error = printPage(printer);
    std::cout << (error == PrintError::None) << std::endl;
    std::cout << printer.pagesLoaded << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `1`, `1`, `1`, and `0`.
The printer now also tracks its loaded sheets. A successful print consumes one sheet; a failed request leaves the printer unchanged.

At first, both problems are present, but the jam check returns immediately, so `Jammed` is reported.
Clearing the jam reveals `NoPaper`. Loading a sheet makes the last request succeed and reduces `pagesLoaded` from `1` to `0`.
Passing the printer by reference lets the function update that same printer object.
</details>

### 5. A bool and an output pointer

```cpp
#include <iostream>

bool divideExactly(int dividend, int divisor, int* quotient)
{
    if (dividend < 0 || divisor <= 0)
    {
        return false;
    }
    if (dividend % divisor != 0)
    {
        return false;
    }
    *quotient = dividend / divisor;
    return true;
}

int main()
{
    int quotient = 99;
    bool success = divideExactly(8, 2, &quotient);
    std::cout << success << std::endl;
    std::cout << quotient << std::endl;

    success = divideExactly(9, 2, &quotient);
    std::cout << success << std::endl;
    std::cout << quotient << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `1`, `4`, `0`, and `4`.
This function accepts a non-negative dividend and a positive divisor, and succeeds only when division is exact.
`8 / 2` is exactly `4`. For `9 / 2`, integer division would discard the fractional part, so the remainder check rejects it.

The bool reports success, while the quotient is written through the pointer parameter.
On failure, no assignment occurs: the last `4` is the previous result, not a result for `9 / 2`.
`quotient` must point to a valid integer object.
</details>

### 6. The same output through a reference

```cpp
#include <iostream>

bool divideExactly(int dividend, int divisor, int& quotient)
{
    if (dividend < 0 || divisor <= 0)
    {
        return false;
    }
    if (dividend % divisor != 0)
    {
        return false;
    }
    quotient = dividend / divisor;
    return true;
}

int main()
{
    int quotient = 99;
    bool success = divideExactly(8, 2, quotient);
    std::cout << success << std::endl;
    std::cout << quotient << std::endl;

    success = divideExactly(9, 2, quotient);
    std::cout << success << std::endl;
    std::cout << quotient << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints the same `1`, `4`, `0`, and `4`.
The reference parameter names the caller's integer, so assigning to `quotient` changes the caller's object.
Pass the variable itself instead of its address.
The exact-division rule and the promise to leave the output unchanged on failure are the same as before.
</details>

### 7. Ignoring the status

```cpp
#include <iostream>

struct TemperatureSensor
{
    bool connected;
    int temperature;
};

bool readTemperature(const TemperatureSensor& sensor, int& temperature)
{
    if (!sensor.connected)
    {
        return false;
    }
    temperature = sensor.temperature;
    return true;
}

int main()
{
    TemperatureSensor sensor{ false, 17 };
    int temperature = 21;
    readTemperature(sensor, temperature);
    std::cout << temperature << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `21`.
The disconnected sensor cannot supply a new reading, so the function returns `false` without changing the output.
The caller ignores that status and prints the old temperature.
`21` is an initialized value, but treating it as a new measurement would be a logic error.
Use the output as a new reading only after checking that the call succeeded.
</details>

### 8. An enum and an output value

```cpp
#include <iostream>

struct Printer
{
    bool jammed;
    int pagesLoaded;
};

enum class PrintError
{
    None,
    Jammed,
    NoPaper,
};

PrintError printPage(Printer& printer, int& pagesRemaining)
{
    if (printer.jammed)
    {
        return PrintError::Jammed;
    }
    if (printer.pagesLoaded == 0)
    {
        return PrintError::NoPaper;
    }
    printer.pagesLoaded -= 1;
    pagesRemaining = printer.pagesLoaded;
    return PrintError::None;
}

int main()
{
    Printer printer{ false, 2 };
    int pagesRemaining = 99;
    PrintError error = printPage(printer, pagesRemaining);
    if (error == PrintError::None)
    {
        std::cout << pagesRemaining << std::endl;
    }

    printer.jammed = true;
    error = printPage(printer, pagesRemaining);
    if (error == PrintError::Jammed)
    {
        std::cout << "printer is jammed" << std::endl;
    }
}
```

<details>
<summary>Answer</summary>

It prints `1` and `printer is jammed`.
The successful request consumes one of the two loaded sheets and writes the remaining count through the reference parameter.
The enum reports either success or a specific failure kind.

The failed request changes neither the printer nor `pagesRemaining`.
The old count is not used as a new result: the caller handles `Jammed` instead.
This combines a detailed status with a separate output value.
</details>

### 9. A null pointer means failure

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

### 10. Returning a custom result structure

```cpp
#include <iostream>

struct TicketMachine
{
    bool online;
    int nextTicket;
};

struct TicketResult
{
    bool success;
    int number;
};

TicketResult issueTicket(TicketMachine& machine)
{
    if (!machine.online)
    {
        return { false, 0 };
    }
    int number = machine.nextTicket;
    machine.nextTicket += 1;
    return { true, number };
}

int main()
{
    TicketMachine machine{ true, 42 };
    TicketResult result = issueTicket(machine);
    if (result.success)
    {
        std::cout << result.number << std::endl;
    }

    machine.online = false;
    result = issueTicket(machine);
    if (result.success)
    {
        std::cout << result.number << std::endl;
    }
    else
    {
        std::cout << "machine is offline" << std::endl;
    }
}
```

<details>
<summary>Answer</summary>

It prints `42` and `machine is offline`.
An online ticket machine issues the next ticket number and advances its counter.
When offline, it cannot issue a ticket and leaves the counter unchanged.

The structure returns the status and ticket number together, without an output parameter.
On failure, `number` is initialized to `0`, but it does not represent an issued ticket.
This is the custom optional structure from the [optional lab](17_optional.md), applied to an operation that can fail.
An enum status field could provide a specific failure kind if the interface needed one.
</details>

### 11. Returning std::optional

```cpp
#include <iostream>
#include <optional>

struct TicketMachine
{
    bool online;
    int nextTicket;
};

std::optional<int> issueTicket(TicketMachine& machine)
{
    if (!machine.online)
    {
        return std::nullopt;
    }
    int number = machine.nextTicket;
    machine.nextTicket += 1;
    return number;
}

int main()
{
    TicketMachine machine{ true, 42 };
    std::optional<int> result = issueTicket(machine);
    if (result.has_value())
    {
        std::cout << *result << std::endl;
    }

    machine.online = false;
    result = issueTicket(machine);
    if (result.has_value())
    {
        std::cout << *result << std::endl;
    }
    else
    {
        std::cout << "machine is offline" << std::endl;
    }
}
```

<details>
<summary>Answer</summary>

It prints the same `42` and `machine is offline`.
`std::optional<int>` expresses either an issued ticket number or its absence.
`std::nullopt` supplies the empty state, and the caller checks `has_value()` before dereferencing.
Like a bool status, the empty state alone does not explain the failure kind.
</details>

### 12. Collecting multiple errors

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

### 13. Reusing the error list

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

### 14. An assertion that passes

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

### 15. An assertion that fails

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

### 16. An assertion for an output-parameter contract

```cpp
#include <iostream>
#include <cassert>

struct TemperatureSensor
{
    bool connected;
    int temperature;
};

bool readTemperature(const TemperatureSensor& sensor, int* temperature)
{
    assert(temperature != nullptr);
    if (!sensor.connected)
    {
        return false;
    }
    *temperature = sensor.temperature;
    return true;
}

int main()
{
    TemperatureSensor sensor{ false, 17 };
    int temperature = 21;
    bool success = readTemperature(sensor, &temperature);
    std::cout << success << std::endl;
    std::cout << temperature << std::endl;

    sensor.connected = true;
    success = readTemperature(sensor, &temperature);
    std::cout << success << std::endl;
    std::cout << temperature << std::endl;
}
```

<details>
<summary>Answer</summary>

With assertions enabled, it prints `0`, `21`, `1`, and `17`.
This interface requires a valid output object. The assertion checks that its pointer is not null; both calls satisfy that check.
Passing `nullptr` would violate the function's contract.

A disconnected sensor is an expected failure, reported with `false`, so the program can continue and reconnect it.
Once connected, the sensor supplies the new reading `17`.
Even with assertions disabled, the caller still must provide a valid output object.
Assertions and ordinary error reporting serve different purposes.
</details>

### 17. Checking success and failure with assertions

```cpp
#include <iostream>
#include <cassert>

struct Printer
{
    bool jammed;
    int pagesLoaded;
};

bool printPage(Printer& printer)
{
    if (printer.jammed || printer.pagesLoaded == 0)
    {
        return false;
    }
    printer.pagesLoaded -= 1;
    return true;
}

int main()
{
    Printer printer{ true, 2 };
    bool printed = printPage(printer);
    assert(!printed);
    assert(printer.pagesLoaded == 2);

    printer.jammed = false;
    printed = printPage(printer);
    assert(printed);
    assert(printer.pagesLoaded == 1);
    std::cout << "tests passed" << std::endl;
}
```

<details>
<summary>Answer</summary>

With assertions enabled, it prints `tests passed`.
The first request is rejected because the printer is jammed; both loaded sheets remain.
After clearing the jam, the second request succeeds and consumes one sheet.
The assertions check the status and the resulting state of the same printer.

The calls to `printPage` are separate from the assertions, so they still execute if assertions are disabled.
Do not place required work only inside `assert`, because its expression may not be evaluated.
With checks disabled, the printed message alone does not establish that the results were verified.
</details>

[Tagged unions and flags](32_tagged_unions_and_flags.md) and [exceptions](33_exceptions.md) have separate later labs.
