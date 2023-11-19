#include <iostream>
#include <span>
#include <vector>

struct Adder
{
    float addedValue;

    void execute(float& value)
    {
        value += addedValue;
    }
};

struct Multiplier
{
    float factor;

    void execute(float& value)
    {
        value *= factor;
    }
};

struct Printer
{
    void execute(float& value)
    {
        std::cout << value;
    }
};

template <typename F>
void forEachItem(std::span<float> values, F functor)
{
    for (float& value : values)
    {
        functor.execute(value);
    }
}

int main()
{
    std::vector<float> values{ 1.0f, 2.0f, 3.0f };
    forEachItem(values, Adder{5.0f});
    forEachItem(values, Printer{});
    forEachItem(values, Multiplier{2.0f});
    forEachItem(values, Printer{});
    return 0;
}