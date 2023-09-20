#include <iostream>

void staticMemory()
{
    static int a = 0;
    std::cout << "a: " << a << std::endl;
    a += 1;
}

int main()
{
    stackMemory(); // prints 0
    stackMemory(); // prints 1
    stackMemory(); // prints 2
    return 0;
}