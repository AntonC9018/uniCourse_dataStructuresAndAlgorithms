#include <iostream>

// globals are implicitly static.
int a = 0;

void staticMemory()
{
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