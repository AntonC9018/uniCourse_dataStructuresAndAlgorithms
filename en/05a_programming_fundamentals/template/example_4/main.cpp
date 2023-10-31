#include <iostream>
#include "two_values.h"

void f();

int main()
{
    TwoValues<int> t {1, 2};
    // TwoValues<int>::getFirst() is compiled once
    std::cout << t.getFirst() << std::endl;

    return 0;
}