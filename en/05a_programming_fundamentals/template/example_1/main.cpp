#include <iostream>

template<typename T>
T getValue()
{
    return {};
}

// We can force a different *specialization* manually (but we don't have to).
template<>
int getValue<int>()
{
    return 5;
}

int main()
{
    std::cout << getValue<int>() << std::endl;
    // The compiler sees that getValue<float> has been used,
    // and inserts a definition created from the templated function
    std::cout << getValue<float>() << std::endl;
    return 0;
}
