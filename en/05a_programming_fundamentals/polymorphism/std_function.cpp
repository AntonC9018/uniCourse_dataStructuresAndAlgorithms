#include <array>
#include <iostream>
#include <span>
#include <functional>

// Note the missing (*), because it's not a function pointer.
using ItemFunc = void(float&);
using ItemStdFunction = std::function<ItemFunc>;

void forEachItem(std::span<float> items, ItemStdFunction& func)
{
    for (size_t i = 0; i < items.size(); i++)
    {
        func(items[i]);
    }
}

struct ComputeContext
{
    float sum;
    float product;
};

struct Button
{
    std::string name;
    std::function<void()> func;
};

std::function<void()> eachItemFunc(
    std::span<float> items,
    // Moving here makes sense.
    // In case it allocated memory, we don't want to reallocate it again.
    ItemStdFunction&& func)
{
    return [
        // Copy by default.
        =,
        // Need to force a move, or it will be copied.
        func = std::move(func)
    ]() mutable
    {
        forEachItem(items, func);
    };
}

struct AddCurrentValueFunctor
{
    float& currentValue;

    void operator()(float& item)
    {
        item += currentValue;
    }
};

int main()
{
    std::array items{1.0f, 2.0f, 3.0f, 4.0f};

    ComputeContext result{0.0f, 1.0f};

    ItemStdFunction printItemFunc = 
        []
        (float& item) 
        { 
            std::cout << item << ", "; 
        };
    ItemStdFunction computeStuffFunc = 
        [&result]
        (float& item)
        {
            result.sum += item;
            result.product *= item;
        };

    std::array funcs{
        Button{
            "Add current sum to all items",
            eachItemFunc(items, AddCurrentValueFunctor{result.sum})
        },
        Button{
            "Print all items",
            eachItemFunc(items, std::move(printItemFunc))
        },
        Button{
            "Compute sum and product",
            eachItemFunc(items, std::move(computeStuffFunc))
        },
        Button{
            "Print computed sum and product",
            [&result]()
            {
                std::cout << result.sum << ", " << result.product << std::endl;
            },
        },
        Button{
            "Reset items",
            eachItemFunc(items, [](float& item)
            {
                std::cout << "Enter new value: ";
                std::cin >> item;
            }),
        },
    };

    while (true)
    {
        std::cout << "Choose a function: " << std::endl;
        for (size_t i = 0; i < funcs.size(); i++)
        {
            std::cout << i << ": " << funcs[i].name << std::endl;
        }

        size_t input;
        std::cin >> input;
        if (!std::cin.good())
            continue;
        if (input >= funcs.size())
            break;
        
        funcs[input].func();
        std::cout << std::endl;
    }

    return 0;
}
