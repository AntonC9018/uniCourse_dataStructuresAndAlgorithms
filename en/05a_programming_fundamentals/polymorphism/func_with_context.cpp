#include <array>
#include <iostream>
#include <vector>
#include <span>

template<typename T>
using ItemFunc = void(*)(float&, T context);

template<typename T>
void forEachItem(std::span<float> items, ItemFunc<T> func, T context)
{
    for (size_t i = 0; i < items.size(); i++)
    {
        func(items[i], context);
    }
}

void addFunc(float& item, float n)
{
    item += n;
}

struct ComputeContext
{
    float sum;
    float product;
};

void computeStuffFunc(float& item, ComputeContext* context)
{
    context->sum += item;
    context->product *= item;
}

int main()
{
    std::vector<float> items{1.0f, 2.0f, 3.0f, 4.0f};
    
    forEachItem(items, addFunc, 5.0f);

    {
        ComputeContext result{0.0f, 1.0f};
        forEachItem(items, computeStuffFunc, &result);
        std::cout << result.product << std::endl;
        std::cout << result.sum << std::endl;
    }

    return 0;
}