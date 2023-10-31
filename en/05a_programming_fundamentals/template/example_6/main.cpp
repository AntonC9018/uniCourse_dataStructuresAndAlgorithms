#include <iostream>
#include "f.h"

int main()
{
    Test t{5};
    std::cout << t.getValue() << std::endl;
    return 0;
}