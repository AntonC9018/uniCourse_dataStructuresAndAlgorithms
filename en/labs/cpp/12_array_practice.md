---
slug: en/cpp/labs/array-practice
---
<!-- course-site-backlink:start -->
[This lesson on the website](https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms/en/cpp/labs/array-practice/)
<!-- course-site-backlink:end -->
# Array practice

## Practice

Use the concepts from the earlier labs to model each problem and write procedural functions.
Use `std::array` for fixed-size storage.
Do not use loops.
Assume supplied indices are valid and quantities are sufficient unless the problem says otherwise.
The first three problems have possible solutions.
Solve the remaining problems yourself.

### 1. Constants selected by index

A shop has three price categories.
Their base prices are 10, 20, and 30 coins, and their multipliers are 1, 1.5, and 2.
Look up the price and multiplier for the second category.

<details>
<summary>Possible solution</summary>

```cpp
#include <array>
#include <iostream>

int main()
{
    std::array<int, 3> prices{ 10, 20, 30 };
    std::array<float, 3> multipliers{ 1.0f, 1.5f, 2.0f };
    int price{ prices[1] };
    float multiplier{ multipliers[1] };
    std::cout << price << std::endl;
    std::cout << multiplier << std::endl;
}
```

It prints `20` and `1.5`.
The arrays contain fixed configuration values; indexing selects the value for one category.
The `f` suffix makes these decimal literals have type `float`.

</details>

### 2. Compiling source code

Source code has a line count, and machine code has an instruction count.
A compiler stores instructions-per-line coefficients for three optimization levels: 2.5, 1.5, and 1.25.
Compile 101 source lines using the third level.
Keep only whole instructions in the result.

<details>
<summary>Possible solution</summary>

```cpp
#include <array>
#include <cstddef>
#include <iostream>

struct SourceCode
{
    int lineCount;
};

struct MachineCode
{
    int instructionCount;
};

struct OptimizationLevel
{
    size_t index;
};

struct Compiler
{
    std::array<double, 3> instructionsPerLine;
};

MachineCode compile(Compiler* compiler, SourceCode source, OptimizationLevel level)
{
    double coefficient{ compiler->instructionsPerLine[level.index] };
    double estimate{ static_cast<double>(source.lineCount) * coefficient };
    return MachineCode{ static_cast<int>(estimate) };
}

int main()
{
    Compiler compiler{ std::array<double, 3>{ 2.5, 1.5, 1.25 } };
    SourceCode source{ 101 };
    OptimizationLevel level{ 2 };
    MachineCode result{ compile(&compiler, source, level) };
    std::cout << result.instructionCount << std::endl;
}
```

It prints `126`.
The level selects coefficient `1.25`; multiplication gives `126.25`, and conversion to `int` discards the fraction.
The cast changes the expression's type.
The type of `source.lineCount` remains `int`.

</details>

### 3. Fridge slots

A fridge has three slots, each holding milk and eggs.
The slots initially contain `(100 ml, 2 eggs)`, `(300 ml, 0 eggs)`, and `(0 ml, 5 eggs)`.
Pour 120 ml from the second slot into an empty cup.
Report the remaining milk, the cup's contents, and the first slot's eggs.

<details>
<summary>Possible solution</summary>

```cpp
#include <array>
#include <cstddef>
#include <iostream>

struct Slot
{
    int milkMl;
    int eggs;
};

struct Fridge
{
    std::array<Slot, 3> slots;
};

struct Cup
{
    int milkMl;
};

void pourMilk(Fridge* fridge, size_t slotIndex, Cup* cup, int amountMl)
{
    fridge->slots[slotIndex].milkMl -= amountMl;
    cup->milkMl += amountMl;
}

int main()
{
    Fridge fridge{
        std::array<Slot, 3>{ Slot{ 100, 2 }, Slot{ 300, 0 }, Slot{ 0, 5 } }
    };
    Cup cup{};
    pourMilk(&fridge, 1, &cup, 120);
    std::cout << fridge.slots[1].milkMl << std::endl;
    std::cout << cup.milkMl << std::endl;
    std::cout << fridge.slots[0].eggs << std::endl;
}
```

It prints `180`, `120`, and `2`.
The function changes the selected slot and the caller's cup through pointers.
The other slots and the egg counts remain unchanged.

</details>

### 4. Editing a file

A file contains five lines, each with a character count.
Add characters to one selected line, swap two selected lines, and move the first line after the third.
Keep the relative order of the other lines when moving a line.

### 5. Raw-byte storage (advanced)

Store several small structs in a fixed byte buffer, recording how many bytes have been used with a `size_t` position.
Reserve space by receiving the item's `sizeof` as a parameter, then advance the position.
Return an address that the caller converts with `reinterpret_cast`.
Account for alignment and available capacity, and demonstrate two different item types occupying separate storage.

This problem needs additional knowledge of alignment and object lifetimes.
Use suitably aligned storage and begin each object's lifetime before accessing its fields.
For example, use placement `new`.
Casting an address alone does not create an object.
Restrict the exercise to trivial structs.

### 6. Bus fares

A bus service has a table of fares for three passenger categories.
Buy a given number of tickets for a selected category and calculate the money remaining from a supplied payment.

### 7. Bakery batches

A bakery has three recipes, each describing flour and sugar needed per batch.
Choose a recipe and prepare a given number of batches, updating the ingredient store and the count of finished batches.

### 8. Inventory transfer

An inventory has four slots, each holding an item ID and a quantity.
Move a given quantity between two selected slots that contain the same item, then swap two complete slots.

### 9. Train carriages

A train has three carriages, each with a seat capacity and a passenger count.
Move passengers from one selected carriage to another and report both carriages' free seats.

### 10. Photo sizes

A photo has a width and height.
Three export presets provide scale factors.
Create an exported photo using a selected preset, keeping whole pixels and leaving the original photo unchanged.

### 11. Hotel minibar

A hotel room has a minibar with four product slots, and the hotel has a price table.
Take specified quantities from two selected slots and update both their stock and the room's bill.

### 12. Parcel pricing

A parcel has a weight, and a delivery service has three destination categories with different price coefficients.
Calculate a whole-number shipping price for a selected destination and apply it to the customer's balance.

### 13. Playlist editing

A playlist holds five tracks, each with an ID and duration.
Replace one selected track, swap two tracks, and calculate the duration of the first three tracks.

### 14. Greenhouse watering

A greenhouse has three beds with water reserves, and a watering program specifies amounts for the three bed types.
Water a selected bed from a tank, updating both the bed and tank quantities.

### 15. Laundry programs

A washing machine has three programs with different durations and detergent requirements.
Run one selected program, consuming detergent and adding its duration to the machine's accumulated working time.

### 16. Robot movements

A robot has a position, and its controller stores three movement commands as coordinate offsets.
Apply three commands chosen by index in the supplied order.
Report the robot's final position.

### 17. Exam scores

An exam has three parts with different weights, and a student has a score for each part.
Calculate a weighted result, keeping only the whole-number part.
Allow the same scores to use a different set of weights.
