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
The first three problems and the advanced byte-storage problem have possible solutions.
Solve the remaining problems yourself.

### 1. Feeding aquarium fish

Three aquariums hold 10, 20, and 30 fish.
Their fish need 1, 1.5, and 2 grams of feed per fish per day, respectively.
Report the fish count and daily feed portion per fish for the second aquarium.

<details>
<summary>Possible solution</summary>

```cpp
#include <array>
#include <iostream>

int main()
{
    std::array<int, 3> fishCounts{ 10, 20, 30 };
    std::array<float, 3> feedGramsPerFish{ 1.0f, 1.5f, 2.0f };
    int fishCount{ fishCounts[1] };
    float feedPortion{ feedGramsPerFish[1] };
    std::cout << fishCount << std::endl;
    std::cout << feedPortion << std::endl;
}
```

It prints `20` and `1.5`.
Indexing selects the fish count and feeding requirement for the same aquarium.
The `f` suffix makes these decimal literals have type `float`.

</details>

### 2. Compiling source code

Source code has a line count, and machine code has an instruction count.
There are three optimization levels: no optimization, basic optimization, and full optimization.
The ratio of machine instructions per source line depends on the compiler and optimization level.
In this simplified model, MSVC uses 2.5, 1.5, and 1.25; GCC uses 3, 1.75, and 1.
Compile 101 source lines with each compiler at full optimization, keeping only whole instructions.

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
    Compiler msvc{ std::array<double, 3>{ 2.5, 1.5, 1.25 } };
    Compiler gcc{ std::array<double, 3>{ 3.0, 1.75, 1.0 } };
    SourceCode source{ 101 };
    OptimizationLevel level{ 2 };
    MachineCode msvcResult{ compile(&msvc, source, level) };
    MachineCode gccResult{ compile(&gcc, source, level) };
    std::cout << msvcResult.instructionCount << std::endl;
    std::cout << gccResult.instructionCount << std::endl;
}
```

It prints `126` and `101`.
For MSVC, the level selects `1.25`; multiplication gives `126.25`, and conversion to `int` discards the fraction.
For GCC, the same level selects `1`, producing `101` instructions.
The cast changes the expression's type.
The type of `source.lineCount` remains `int`.

</details>

### 3. Fridge slots

A fridge has three slots, each holding one milk bottle.
The bottles contain 100 ml, 300 ml, and 200 ml.
Pour 120 ml from the second bottle into an empty cup.
Report the milk left in that bottle, the cup's contents, and the milk in the first bottle.

<details>
<summary>Possible solution</summary>

```cpp
#include <array>
#include <cstddef>
#include <iostream>

struct MilkBottle
{
    int milkMl;
};

struct Fridge
{
    std::array<MilkBottle, 3> slots;
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
        std::array<MilkBottle, 3>{ MilkBottle{ 100 }, MilkBottle{ 300 }, MilkBottle{ 200 } }
    };
    Cup cup{};
    pourMilk(&fridge, 1, &cup, 120);
    std::cout << fridge.slots[1].milkMl << std::endl;
    std::cout << cup.milkMl << std::endl;
    std::cout << fridge.slots[0].milkMl << std::endl;
}
```

It prints `180`, `120`, and `100`.
The function changes the selected slot and the caller's cup through pointers.
The other bottles remain unchanged.

</details>

### 4. Editing a file

A file contains five lines, each with a character count.
Add characters to one selected line and swap two selected lines.

### 5. Bus fares

A bus service has a table of fares for three passenger categories.
Buy a given number of tickets for a selected category and calculate the money remaining from a supplied payment.

### 6. Bakery batches

A bakery has three recipes, each describing flour and sugar needed per batch.
Choose a recipe and prepare a given number of batches, updating the ingredient store and the count of finished batches.

### 7. Storage drawers

A cabinet has four drawers; each drawer holds a fastener type and a count.
Move the entire contents of one selected drawer into an empty drawer, leaving the original drawer empty.

### 8. Train carriages

A train has three carriages, each with a seat capacity and a passenger count.
Move passengers from one selected carriage to another and report both carriages' free seats.

### 9. Cropping a film frame

A film strip contains four frames, each with a width and height in pixels.
Crop a selected frame by specified amounts from its left, right, top, and bottom edges.
Return the cropped frame without changing the original, then replace a different frame with the result.

### 10. Hotel minibar

A hotel room has a minibar with four product slots, and the hotel has a price table.
Take specified quantities from two selected slots and update both their stock and the room's bill.

### 11. Playlist playback

A playlist holds five tracks with durations in seconds.
A player records which track is playing and the elapsed time within it.
Seek to a supplied time in the current track and report how many seconds remain.
Select another track and start it from the beginning.

### 12. Mixing stage lights

A lighting desk stores four colors, each with red, green, and blue intensities between 0 and 1.
Mix two selected colors using a supplied fraction of the first color and the remaining fraction of the second.
Store the resulting color in a selected spotlight without changing the desk's original colors.

### 13. Theater seating

A theater has three rows of four seats; each seat stores a ticket number, with zero meaning empty.
Seat a customer at a supplied row and column, then move their ticket to another empty seat.
Leave the original seat empty.

### 14. Robot delivery route

A robot starts at a given position, and a delivery map stores four destinations as x/y coordinates.
Move to two destinations chosen by index, in order.
For each leg, report the movement vector; report the final position too.

### 15. Race finish photo

A race records three finish times in seconds, already in finishing order.
A finish photo shows the runners at the instant the winner finishes.
Each runner's speed is constant over the 100-meter race.
Calculate the two other runners' distances from the finish line at that instant.

### 16. Linking freight wagons

Three freight wagons have cargo weights and are stored together.
Connect them in order so each wagon knows which wagon follows it.
Starting from the first wagon, follow the connections to add cargo to the last wagon without selecting it by index.
Report the last wagon's new cargo weight.

### 17. Raw-byte storage (advanced)

Store a coin and a measurement in a fixed byte buffer, recording the used byte count with a `size_t` position.
Reserve space using the item's size and alignment,
and return an address that the caller converts with `reinterpret_cast`.
Assume the buffer has enough room for both items and any alignment padding.

<details>
<summary>Possible solution</summary>

```cpp
#include <array>
#include <cstddef>
#include <iostream>
#include <memory>
#include <new>

struct Storage
{
    alignas(std::max_align_t) std::array<std::byte, 64> bytes{};
    size_t position{};
};

void* reserve(Storage* storage, size_t itemSize, size_t itemAlignment)
{
    void* address{ storage->bytes.data() + storage->position };
    size_t remaining{ storage->bytes.size() - storage->position };
    [[maybe_unused]] void* aligned{ std::align(itemAlignment, itemSize, address, remaining) };
    storage->position = storage->bytes.size() - remaining + itemSize;
    return address;
}

struct Coin
{
    int value;
};

struct Measurement
{
    double value;
};

int main()
{
    Storage storage{};
    void* coinAddress{ reserve(&storage, sizeof(Coin), alignof(Coin)) };
    Coin* coin{ reinterpret_cast<Coin*>(coinAddress) };
    [[maybe_unused]] Coin* createdCoin{ new (coin) Coin{ 5 } };

    void* measurementAddress{ reserve(&storage, sizeof(Measurement), alignof(Measurement)) };
    Measurement* measurement{ reinterpret_cast<Measurement*>(measurementAddress) };
    [[maybe_unused]] Measurement* createdMeasurement{ new (measurement) Measurement{ 2.5 } };

    std::cout << coin->value << std::endl;
    std::cout << measurement->value << std::endl;
    std::cout << storage.position << std::endl;
}
```

It prints `5`, `2.5`, and typically `16` used bytes.
`sizeof` supplies the object size, and `alignof` supplies the required alignment.
`std::align` moves `address` forward if padding is needed and reduces `remaining` by that padding.
The new position includes both the padding and the reserved object size.
`reinterpret_cast` supplies the pointer type; placement `new` begins the object's lifetime and initializes its fields.

> This advanced example introduces alignment and object lifetimes beyond the earlier labs.
> Assume every reservation fits; a reusable allocator would also handle `std::align` returning a null pointer.
> The exact used byte count depends on sizes and alignment; these trivial objects need no explicit destruction.

</details>
