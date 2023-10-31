#include <iostream>
#include "two_values.h"

void f()
{
    TwoValues<int> t {1, 2};
    // TwoValues<int>::getFirst compiled for the second time.
    std::cout << t.getFirst() << std::endl;
}