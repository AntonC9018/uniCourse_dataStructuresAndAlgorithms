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
    {
        Printer printer{ true };
        bool printed = printPage(printer);
        std::cout << printed << std::endl;
    }
    {
        Printer printer{ false };
        bool printed = printPage(printer);
        std::cout << printed << std::endl;
    }
}
```

<details>
<summary>Answer</summary>

It prints `0`, `page printed`, and `1`.
`Printer` models a printer, and `jammed` says whether paper is stuck in it.
The first block's request fails because that printer is jammed. The second block creates an unjammed printer, so its request prints a page and succeeds.

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
    if (grade > 10)
    {
        return GradeError::TooHigh;
    }
    return GradeError::None;
}

int main()
{
    std::cout << static_cast<int>(validateGrade(0)) << std::endl;
    std::cout << static_cast<int>(validateGrade(11)) << std::endl;
    std::cout << static_cast<int>(validateGrade(10)) << std::endl;
    std::cout << static_cast<int>(validateGrade(5)) << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `1`, `2`, `0`, and `0`: the numeric values of `TooLow`, `TooHigh`, `None`, and `None`.
This interface accepts integer grades from `1` through `10`, including `10`.
A single parameter is checked in two ways: `0` is too low, `11` is too high, and both `10` and `5` are valid.
The enum communicates the specific failure kind; `static_cast<int>` makes its value printable.
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
    {
        Printer printer{ true, 0 };
        PrintError error = printPage(printer);
        std::cout << (error == PrintError::Jammed) << std::endl;
    }
    {
        Printer printer{ false, 0 };
        PrintError error = printPage(printer);
        std::cout << (error == PrintError::NoPaper) << std::endl;
    }
    {
        Printer printer{ false, 1 };
        PrintError error = printPage(printer);
        std::cout << (error == PrintError::None) << std::endl;
        std::cout << printer.pagesLoaded << std::endl;
    }
}
```

<details>
<summary>Answer</summary>

It prints `1`, `1`, `1`, and `0`.
Each block creates a printer for a separate case. A successful print consumes one sheet; a failed request leaves that printer unchanged.

In the first case, both problems are present, but the jam check returns immediately, so `Jammed` is reported.
The second printer is not jammed but has no paper, so it reports `NoPaper`.
The third printer has one sheet and succeeds, reducing `pagesLoaded` from `1` to `0`.
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
    {
        int quotient = 99;
        bool success = divideExactly(8, 2, &quotient);
        std::cout << success << std::endl;
        std::cout << quotient << std::endl;
    }
    {
        int quotient = 99;
        bool success = divideExactly(9, 2, &quotient);
        std::cout << success << std::endl;
        std::cout << quotient << std::endl;
    }
}
```

<details>
<summary>Answer</summary>

It prints `1`, `4`, `0`, and `99`.
This function accepts a non-negative dividend and a positive divisor, and succeeds only when division is exact.
`8 / 2` is exactly `4`. For `9 / 2`, integer division would discard the fractional part, so the remainder check rejects it.

Each block has its own quotient and status variables.
The bool reports success, while the quotient is written through the pointer parameter.
On failure, no assignment occurs: the second block's quotient remains `99`, not a result for `9 / 2`.
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
    {
        int quotient = 99;
        bool success = divideExactly(8, 2, quotient);
        std::cout << success << std::endl;
        std::cout << quotient << std::endl;
    }
    {
        int quotient = 99;
        bool success = divideExactly(9, 2, quotient);
        std::cout << success << std::endl;
        std::cout << quotient << std::endl;
    }
}
```

<details>
<summary>Answer</summary>

It prints the same `1`, `4`, `0`, and `99`.
The reference parameter names the caller's integer, so assigning to `quotient` changes the caller's object.
Pass the variable itself instead of its address.
The exact-division rule and the promise to leave the output unchanged on failure are the same as before.
Each block starts with a new quotient initialized to `99`.
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
    [[maybe_unused]] bool success = readTemperature(sensor, temperature);
    std::cout << temperature << std::endl;
}
```

<details>
<summary>Answer</summary>

It prints `21`.
The disconnected sensor cannot supply a new reading, so the function returns `false` without changing the output.
The caller saves the status in a `[[maybe_unused]]` variable and intentionally leaves it unchecked.
The attribute marks the unused result explicitly; it does not handle the failure.

`21` is an initialized value, but treating it as a new measurement would be a logic error.
Use the output as a new reading only after checking that the call succeeded.
</details>

### 8. An enum and an output value

```cpp
#include <iostream>

struct VendingMachine
{
    int bottles;
    int price;
};

enum class PurchaseError
{
    None,
    SoldOut,
    NotEnoughMoney,
};

PurchaseError buyWater(VendingMachine& machine, int money, int& change)
{
    if (machine.bottles == 0)
    {
        return PurchaseError::SoldOut;
    }
    if (money < machine.price)
    {
        return PurchaseError::NotEnoughMoney;
    }
    machine.bottles -= 1;
    change = money - machine.price;
    return PurchaseError::None;
}

int main()
{
    VendingMachine machine{ 1, 3 };
    {
        int change = 99;
        PurchaseError error = buyWater(machine, 2, change);
        if (error == PurchaseError::NotEnoughMoney)
        {
            std::cout << "not enough money" << std::endl;
        }
    }
    {
        int change = 99;
        PurchaseError error = buyWater(machine, 5, change);
        if (error == PurchaseError::None)
        {
            std::cout << change << std::endl;
        }
    }
    {
        int change = 99;
        PurchaseError error = buyWater(machine, 5, change);
        if (error == PurchaseError::SoldOut)
        {
            std::cout << "sold out" << std::endl;
        }
    }
}
```

<details>
<summary>Answer</summary>

It prints `not enough money`, `2`, and `sold out`.
The machine has one bottle priced at `3`. The first payment of `2` is rejected without selling it.
The second payment of `5` succeeds: the bottle is sold, and the reference output receives the customer's change, `5 - 3`.
The last purchase fails because the machine is now empty.

The enum reports a specific failure kind, while the reference supplies a useful result on success.
Each call has fresh status and change variables. Failed calls leave their change variable unchanged, and the caller does not use it as a result.
The same machine is deliberately kept across the blocks to show its stock being consumed.
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
    {
        TicketMachine machine{ true, 42 };
        TicketResult result = issueTicket(machine);
        if (result.success)
        {
            std::cout << result.number << std::endl;
        }
    }
    {
        TicketMachine machine{ false, 42 };
        TicketResult result = issueTicket(machine);
        if (result.success)
        {
            std::cout << result.number << std::endl;
        }
        else
        {
            std::cout << "machine is offline" << std::endl;
        }
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
    {
        TicketMachine machine{ true, 42 };
        std::optional<int> result = issueTicket(machine);
        if (result.has_value())
        {
            std::cout << *result << std::endl;
        }
    }
    {
        TicketMachine machine{ false, 42 };
        std::optional<int> result = issueTicket(machine);
        if (result.has_value())
        {
            std::cout << *result << std::endl;
        }
        else
        {
            std::cout << "machine is offline" << std::endl;
        }
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
    {
        [[maybe_unused]] bool valid = validateOrder(-1, -2, errors);
    }
    {
        bool valid = validateOrder(3, 4, errors);
        std::cout << valid << std::endl;
        std::cout << errors.size() << std::endl;
    }
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
    {
        TemperatureSensor sensor{ false, 17 };
        int temperature = 21;
        bool success = readTemperature(sensor, &temperature);
        std::cout << success << std::endl;
        std::cout << temperature << std::endl;
    }
    {
        TemperatureSensor sensor{ true, 17 };
        int temperature = 21;
        bool success = readTemperature(sensor, &temperature);
        std::cout << success << std::endl;
        std::cout << temperature << std::endl;
    }
}
```

<details>
<summary>Answer</summary>

With assertions enabled, it prints `0`, `21`, `1`, and `17`.
Each block creates a sensor, an output variable, and a status variable for a separate case.
This interface requires a valid output object. The assertion checks that its pointer is not null; both calls satisfy that check.
Passing `nullptr` would violate the function's contract.

A disconnected sensor is an expected failure, reported with `false`, so the program can continue.
The connected sensor in the second block supplies the reading `17`.
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
    {
        Printer printer{ true, 2 };
        bool printed = printPage(printer);
        assert(!printed);
        assert(printer.pagesLoaded == 2);
    }
    {
        Printer printer{ false, 2 };
        bool printed = printPage(printer);
        assert(printed);
        assert(printer.pagesLoaded == 1);
    }
    std::cout << "tests passed" << std::endl;
}
```

<details>
<summary>Answer</summary>

With assertions enabled, it prints `tests passed`.
The first block's printer rejects the request because it is jammed; both loaded sheets remain.
The second block's printer is not jammed, so its request succeeds and consumes one sheet.
The assertions check the status and the resulting state in each independent case.

The calls to `printPage` are separate from the assertions, so they still execute if assertions are disabled.
Do not place required work only inside `assert`, because its expression may not be evaluated.
With checks disabled, the printed message alone does not establish that the results were verified.
</details>

[Tagged unions and flags](32_tagged_unions_and_flags.md) and [exceptions](33_exceptions.md) have separate later labs.
