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

void printGradeError(GradeError error)
{
    switch (error)
    {
    case GradeError::None:
        std::cout << "valid grade" << std::endl;
        break;
    case GradeError::TooLow:
        std::cout << "grade too low" << std::endl;
        break;
    case GradeError::TooHigh:
        std::cout << "grade too high" << std::endl;
        break;
    }
}

int main()
{
    printGradeError(validateGrade(0));
    printGradeError(validateGrade(11));
    printGradeError(validateGrade(10));
    printGradeError(validateGrade(5));
}
```

<details>
<summary>Answer</summary>

It prints `grade too low`, `grade too high`, `valid grade`, and `valid grade`.
This interface accepts integer grades from `1` through `10`, including `10`.
A single parameter is checked in two ways: `0` is too low, `11` is too high, and both `10` and `5` are valid.
The enum communicates the failure kind to the caller. The helper then translates that status into a message for a person.
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

void printPrinterError(PrintError error)
{
    switch (error)
    {
    case PrintError::None:
        std::cout << "page printed" << std::endl;
        break;
    case PrintError::Jammed:
        std::cout << "printer is jammed" << std::endl;
        break;
    case PrintError::NoPaper:
        std::cout << "no paper" << std::endl;
        break;
    }
}

int main()
{
    {
        Printer printer{ true, 0 };
        PrintError error = printPage(printer);
        printPrinterError(error);
    }
    {
        Printer printer{ false, 0 };
        PrintError error = printPage(printer);
        printPrinterError(error);
    }
    {
        Printer printer{ false, 1 };
        PrintError error = printPage(printer);
        printPrinterError(error);
        std::cout << printer.pagesLoaded << std::endl;
    }
}
```

<details>
<summary>Answer</summary>

It prints `printer is jammed`, `no paper`, `page printed`, and `0`.
Each block creates a printer for a separate case. A successful print consumes one sheet; a failed request leaves that printer unchanged.

In the first case, both problems are present, but the jam check returns immediately, so `Jammed` is reported.
The second printer is not jammed but has no paper, so it reports `NoPaper`.
The third printer has one sheet and succeeds, reducing `pagesLoaded` from `1` to `0`.
The helper prints a message for each enum result without replacing the enum status returned to the caller.
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

### 7. An output with no initial value

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
        int quotient;
        bool success = divideExactly(8, 2, quotient);
        if (success)
        {
            std::cout << quotient << std::endl;
        }
    }
    {
        int quotient;
        bool success = divideExactly(9, 2, quotient);
        if (success)
        {
            std::cout << quotient << std::endl;
        }
        else
        {
            std::cout << "not exact" << std::endl;
        }
    }
}
```

<details>
<summary>Answer</summary>

It prints `4` and `not exact`.
Each `quotient` is declared without an initial value.
In the successful call, the function assigns `4` through the reference before the caller reads it.
In the failed call, the function does not assign anything, and the caller never reads that quotient.

This is allowed in standard C++: the integer object already exists, and binding a reference to it does not read its value.
Writing through that reference can supply its first value. The same applies to passing its address to an output pointer.
In C++20, reading this uninitialized integer before a successful assignment would be undefined behavior.
Checking the status is essential when the output has no initial value.
</details>

### 8. Ignoring the status

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

### 9. An enum and an output value

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

### 10. A null pointer means failure

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

### 11. Returning a custom result structure

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

### 12. Returning std::optional

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

### 13. Collecting multiple errors

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

### 14. Reusing the error list

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

### 15. An assertion that passes

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

### 16. An assertion that fails

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

### 17. An assertion for an output-parameter contract

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

### 18. Checking success and failure with assertions

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

## Practice tasks

Model each domain with structs and write procedural functions. Decide what each function receives, what it changes, and how the caller learns whether it succeeded. Use the error-reporting techniques from this lab. The first task has a full solution; the remaining tasks have no supplied solutions.

### 19. Vending machine

A vending machine sells water for 3 coins and juice for 5 coins. It starts with two bottles of water and one bottle of juice. A customer selects a product by its index and pays a whole number of coins. Report an invalid selection, a negative payment, an empty product slot, or insufficient payment. A successful purchase removes one bottle and returns the change through a reference parameter. A failed purchase changes neither the stock nor the output variable.

<details>
<summary>Possible solution</summary>

Each product needs a name, a price, and a stock count. The machine holds a fixed array of products. The error enum describes the outcome; the change is a separate output, meaningful only on success.

Check the selection before accessing the array. Then check the payment and availability. Only after every check passes, decrease the stock and write the change. Prices must be positive and stock counts nonnegative: those are assumptions about the machine's state, checked with assertions.

```cpp
#include <array>
#include <cassert>
#include <iostream>
#include <string_view>

struct Product
{
    std::string_view name;
    int price;
    int stock;
};

struct VendingMachine
{
    std::array<Product, 2> products;
};

enum class PurchaseError
{
    None,
    InvalidSelection,
    InvalidPayment,
    SoldOut,
    NotEnoughMoney,
};

PurchaseError buyProduct(
    VendingMachine& machine,
    int productIndex,
    int payment,
    int& change)
{
    if (productIndex < 0 || productIndex >= int(machine.products.size()))
    {
        return PurchaseError::InvalidSelection;
    }
    if (payment < 0)
    {
        return PurchaseError::InvalidPayment;
    }

    Product& product = machine.products[productIndex];
    assert(product.price > 0);
    assert(product.stock >= 0);
    if (product.stock == 0)
    {
        return PurchaseError::SoldOut;
    }
    if (payment < product.price)
    {
        return PurchaseError::NotEnoughMoney;
    }

    product.stock -= 1;
    change = payment - product.price;
    return PurchaseError::None;
}

int main()
{
    VendingMachine machine{
        std::array<Product, 2>{ Product{ "water", 3, 2 }, Product{ "juice", 5, 1 } }
    };
    {
        int change = 99;
        PurchaseError error = buyProduct(machine, 1, 4, change);
        assert(error == PurchaseError::NotEnoughMoney);
        assert(machine.products[1].stock == 1);
        assert(change == 99);
        std::cout << "not enough money" << std::endl;
    }
    {
        int change;
        PurchaseError error = buyProduct(machine, 1, 7, change);
        assert(error == PurchaseError::None);
        if (error == PurchaseError::None)
        {
            std::cout << machine.products[1].name << ": change " << change << std::endl;
        }
        assert(machine.products[1].stock == 0);
    }
    {
        int change = 99;
        PurchaseError error = buyProduct(machine, 1, 7, change);
        assert(error == PurchaseError::SoldOut);
        assert(machine.products[1].stock == 0);
        assert(change == 99);
        std::cout << "sold out" << std::endl;
    }
}
```

The program prints:

```text
not enough money
juice: change 2
sold out
```

The same machine is used across the three blocks so the second purchase consumes the juice. Each attempt has its own status and output variables. The failed attempts keep the output's initial value, but that value is not change from a purchase. The successful attempt assigns its output before the caller reads it.

The assertions test the outcomes and state changes. Calls to `buyProduct` occur outside the assertions, so disabling assertions does not remove the purchases.

</details>

### 20. Library checkout

A small library has a fixed-size buffer of books, with one copy of each book. Each borrower has a fixed-size buffer of borrowed book IDs and a count of occupied entries. Find a book by ID, returning a null pointer if it is absent. Check out a book to a borrower passed by pointer. Report a missing book, an already borrowed book, or a full borrower buffer. A successful checkout updates both the book's availability and the borrower's buffer; a failed checkout changes neither. Choose capacities small enough to try every case by hand.

### 21. Configurable parcel shipping

A shipping service receives a parcel and a configuration containing dimension and weight limits, supported destinations, prices, and delivery times. Validate the parcel against the supplied configuration and calculate a shipping quote. Return a custom result struct with a status, price, and estimated delivery time; the quote fields are meaningful only on success. Try the same parcel with two different configurations.

### 22. Ticket booking

A vehicle has a fixed-size array of seats with prices and information about which seats are by a window. Support three requests: a specific seat, the first available window seat, or any available seat. For the last option, take the first available seat; no random-number generation is needed. Receive the customer's money by reference, return an error enum, and fill a ticket struct through a pointer parameter. The ticket records the assigned seat, price, and money remaining. On success, reserve the seat and deduct its price. Report an invalid seat, an occupied seat, no matching seat, or insufficient funds. On failure, leave the seats, money, and ticket output unchanged.

### 23. Exam registration

A student wants to register for an exam. Each exam has prerequisites and a limited number of places. A student may lack several prerequisites, the exam may be full, or the student may already be registered. Collect all applicable problems in an error vector passed by reference, identifying each missing prerequisite. Register the student only if there are no problems. Decide whether the function clears the supplied vector or appends to it, and make that contract clear to the caller.

### 24. Sensor readings

A sensor supplies a buffer of temperature readings and an allowed range. Reject readings outside that range and calculate the average of the valid readings. Return an empty `std::optional` if no valid readings remain, and let the caller report the rejected readings. Distinguish expected invalid readings from assumptions about the function's inputs that should be checked with assertions.

### 25. Currency exchange

An exchange service has a fixed table of supported currency pairs, exchange rates, and fees. A customer requests an exchange and supplies a source-currency balance by reference. Return an error enum and fill a receipt struct through a pointer parameter. The receipt records the amount received, rate used, and fee charged. Report an unsupported pair, an invalid amount, or insufficient funds including the fee. On success, deduct the exchanged amount and fee from the balance; on failure, leave the balance and receipt unchanged. Choose and document units and a rounding rule for monetary amounts.


[Tagged unions and flags](34_tagged_unions_and_flags.md) and [exceptions](35_exceptions.md) have separate later labs.
