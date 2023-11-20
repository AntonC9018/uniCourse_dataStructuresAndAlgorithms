#include <iostream>

using OperatorFunc = int(*)(int a, int b);

int main()
{
    OperatorFunc addFunc = [](int a, int b)
    {
        return a + b;
    };
    std::cout << addFunc(1, 2);

    // This has a bit of a different effect.
    // The type of addFunc2 here is *not* a function pointer.
    auto addFunc2 = [](int a, int b)
    {
        return a + b;
    };
    // Doesn't go through a function pointer indirection.
    std::cout << addFunc2(1, 2);

    // Still implicitly converts to a function pointer.
    OperatorFunc addFunc3 = addFunc2;

    return 0;
}


// addFunc2 creates a functor class without private state.
// Like this:
class Functor
{
public:
    int operator()(int a, int b)
    {
        return a + b;
    }
};