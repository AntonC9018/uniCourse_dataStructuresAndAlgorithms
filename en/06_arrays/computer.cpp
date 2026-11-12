#include <cstddef>
#include <cstdint>
#include <iostream>

struct Monitor
{
    uint16_t widthPixels;
    uint16_t heightPixels;
};

struct SystemUnit
{
    double priceInDollars;
    uint64_t serialNumber;
};

struct Keyboard
{
    uint8_t rows;
    uint8_t columns;
};

struct Computer
{
    Monitor monitor;
    SystemUnit systemUnit;
    Keyboard keyboard;
};

// One part of each kind holds 4 + 16 + 2 = 22 bytes of actual data.
static_assert(sizeof(Monitor) == 4);
static_assert(sizeof(SystemUnit) == 16);
static_assert(sizeof(Keyboard) == 2);

// A whole computer takes 32 bytes, because the compiler has to insert padding.
static_assert(sizeof(Computer) == 32);

int main()
{
    constexpr size_t numComputers = 1000;

    // One array of whole computers: 32 bytes each.
    Computer computers[numComputers]{};
    size_t bytesOfComputers = sizeof(computers);
    std::cout << bytesOfComputers << std::endl; // 32000

    // Three arrays of parts: 4 + 16 + 2 = 22 bytes each.
    Monitor monitors[numComputers]{};
    SystemUnit systemUnits[numComputers]{};
    Keyboard keyboards[numComputers]{};
    size_t bytesOfParts = sizeof(monitors) + sizeof(systemUnits) + sizeof(keyboards);
    std::cout << bytesOfParts << std::endl; // 22000

    // The parts of the computer at index 3 sit at index 3 in every array.
    monitors[3].widthPixels = 1920;
    systemUnits[3].priceInDollars = 999.99;
    keyboards[3].rows = 6;

    return 0;
}
