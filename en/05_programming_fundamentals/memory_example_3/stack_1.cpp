#include <iostream>

void stackMemory()
{
    int a = 0;
    std::cout << "a: " << a << std::endl;
    a += 1;
}

int main()
{
    stackMemory(); // prints 0
    stackMemory(); // prints 0
    stackMemory(); // prints 0
    return 0;
}