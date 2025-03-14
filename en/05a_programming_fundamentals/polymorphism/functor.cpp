#include <iostream>
#include <span>
#include <vector>

struct Adder
{
    float addedValue;

    void operator()(float& value)
    {
        value += addedValue;
    }
};

struct Multiplier
{
    float factor;

    void operator()(float& value)
    {
        value *= factor;
    }
};

void printFloat(float& value)
{
    std::cout << value;
}

template <typename F>
void forEachItem(std::span<float> values, F functor)
{
    for (float& value : values)
    {
        functor(value);
    }
}

int main()
{
    std::vector<float> values{ 1.0f, 2.0f, 3.0f };
    forEachItem(values, Adder{5.0f});
    forEachItem(values, printFloat);
    forEachItem(values, Multiplier{2.0f});
    forEachItem(values, printFloat);
    forEachItem(values, [&a = values[0]](float& value){ value *= a; });
    return 0;
}
