#include <iostream>

void staticMemory()
{
    static int a = 0;
    std::cout << "a: " << a << std::endl;
    a += 1;
}

int main()
{
    staticMemory(); // prints 0
    staticMemory(); // prints 1
    staticMemory(); // prints 2
    return 0;
}