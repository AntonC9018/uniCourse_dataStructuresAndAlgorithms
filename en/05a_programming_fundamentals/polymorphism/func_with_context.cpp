#include <array>
#include <iostream>
#include <vector>

template<typename T>
using ItemFunc = void(*)(float&, T context);

template<typename T>
void forEachItem(std::vector<float>& items, ItemFunc<T> func, T context)
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

void computeStuffFunc(const float& item, ComputeContext* context)
{
    context->sum += item;
    context->product *= item;
}

int main()
{
    std::vector<float> items{1.0f, 2.0f, 3.0f, 4.0f};
    
}