#include <iostream>
#include <array>

struct Context
{
    float a;
    float b;
};

int main()
{
    Context context{};

    auto increase = [&context]()
    {
        context.a += 1;
        context.b *= 2;
    };

    auto reset = [&context]()
    {
        context.a = 0;
        context.b = 1;
    };

    auto print = [&context]()
    {
        std::cout 
            << context.a
            << ", "
            << context.b
            << std::endl;
    };

    // The functors are copyable.
    auto increase2 = increase;

    print(); // 0, 0
    reset();
    print(); // 0, 1
    increase();
    print(); // 1, 2
    increase();
    print(); // 2, 4
}


// For the type of the functor variable, 
// the compiler generated a type like:
class Functor
{
    // Reference fields are just pointers under the hood.
    Context& context;

public:
    Functor(Context& context) 
        // The *reference* can only be initialized in the member initializer.
        : context(context)
    {
    }

    void operator()() const // <- we haven't said `mutable`
    {
        std::cout 
            << context.a
            << ", "
            << context.b
            << std::endl;
    }
};