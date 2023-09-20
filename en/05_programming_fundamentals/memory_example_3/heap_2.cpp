#include <iostream>
#include <stdlib.h>

// This is the same example, but with the malloc() function,
// it uses the C heap instead of the C++ heap.

int* heapMemory()
{
    void* memory = malloc(sizeof(int));
    int* a = (int*) memory;
    std::cout << "a: " << *a << std::endl;
    *a = *a + 1;
}

int main()
{
    int* a = stackMemory(); // prints 0
    int* b = stackMemory(); // prints 0

    // no
    bool areAddressesEqual = ((size_t) a == (size_t) b);
    std::cout << "are addresses equal: " << areValuesEqual ? "yes" : "no" << std::endl;

    // yes
    bool areValuesEqual = (*a == *b);
    std::cout << "are values equal: " << areValuesEqual ? "yes" : "no" << std::endl;

    *a = 5;
    *b = 10;
    // Prints -5.
    std::cout << (*a - *b) << std::endl;

    free(a);
    free(b);

    return 0;
}