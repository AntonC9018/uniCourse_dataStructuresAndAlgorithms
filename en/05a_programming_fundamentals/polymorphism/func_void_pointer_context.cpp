#include <iostream>
#include <vector>
#include <array>

struct ComputedState
{
    float a;
    float b;
};

void recomputeState(ComputedState* context)
{
    context->a *= 2.0f;
    context->b += 1.0f;
}
void recomputeStateAdapter(void* context)
{
    ComputedState* typedContext = static_cast<ComputedState*>(context);
    recomputeState(typedContext);
}

void resetState(ComputedState* context)
{
    *context = {};
}
void resetStateAdapter(void* context)
{
    ComputedState* typedContext = static_cast<ComputedState*>(context);
    resetState(typedContext);
}

void printState(ComputedState* context)
{
    std::cout << "a: " << context->a << std::endl;
    std::cout << "b: " << context->b << std::endl;
}
void printStateAdapter(void* context)
{
    ComputedState* typedContext = static_cast<ComputedState*>(context);
    printState(typedContext);
}

void addToFloat(float& value)
{
    float n;
    do
    {
        std::cout << "Enter a number to add to the value:";
        std::cin >> n;
    } 
    while (!std::cin.good());

    value += n;
}
void addToFloatAdapter(void* context)
{
    float* typedContext = static_cast<float*>(context);
    addToFloat(*typedContext);
}

void printHelloAdapter(void*)
{
    std::cout << "Hello!" << std::endl;
}

using ItemFunc = void(*)(void* context);

struct Button
{
    std::string name;
    ItemFunc func;
    void* context;
};

int main()
{
    ComputedState state{};
    float otherNumber = 0.0f;
    std::array buttons{
        // Some of the functions may operate on the state
        Button{"Recompute", recomputeStateAdapter, &state},
        Button{"Reset", resetStateAdapter, &state},
        Button{"Print", printStateAdapter, &state},

        // Others may operate on something else
        Button{"Add to a", addToFloatAdapter, &state.a},
        Button{"Add to b", addToFloatAdapter, &state.b},

        // And some may operate on something completely different
        Button{"Add to other number", addToFloatAdapter, &otherNumber},

        // And some may not require any context at all
        Button{"Print hello", printHelloAdapter, nullptr},
    };

    size_t buttonChoice;
    while (true)
    {
        for (size_t i = 0; i < buttons.size(); i++)
        {
            std::cout << i << " - " << buttons[i].name << std::endl;
        }
        std::cin >> buttonChoice;
        if (!std::cin.good())
            continue;
        if (buttonChoice >= buttons.size())
            break;
        
        Button& button = buttons[buttonChoice];

        // Now this part of code doesn't have to know anything about the context.
        button.func(button.context);
    }

    return 0;
}
