#include <array>
#include <iostream>
#include "template.h"

void f()
{
    std::array arr = { 1, 2, 3, 4, 5 };
    std::cout << sum<int>(arr) << std::endl;
}