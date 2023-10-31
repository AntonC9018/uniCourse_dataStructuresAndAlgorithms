#include <iostream>
#include "template.h"

void f();

int main()
{
    f();
    std::array arr = { 1, 2 };
    std::cout << sum<int>(arr) << std::endl;
    return 0;
}