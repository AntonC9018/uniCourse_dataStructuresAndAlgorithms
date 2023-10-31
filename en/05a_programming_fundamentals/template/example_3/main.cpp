#include <iostream>

template<typename T>
struct TwoValues
{
    T first;
    T second;
};

template<typename T>
T sum(const TwoValues<T>& values)
{
    return values.first + values.second;
}

int main()
{
    {
        TwoValues<int> t {1, 2};
        std::cout << sum<int>(t) << std::endl;
    }

    {
        // Omitting the types is allowed.
        TwoValues t{1, 2};
        std::cout << sum(t) << std::endl;
    }

    return 0;
}