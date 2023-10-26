#include <iostream>
#include <assert.h>
#include <array>

int main()
{
    std::array<int, 4> arr;
    size_t currentIndex = 0;

    for (; currentIndex < arr.size(); currentIndex++)
    {
        std::cout << "Enter a number: ";
        int input;
        std::cin >> input;

        if (input == -1)
        {
            break;
        }
        arr[currentIndex] = input;
    }

    size_t elementCount = currentIndex; 
    for (size_t i = 0; i < elementCount; i++)
    {
        std::cout 
            << "arr[" 
            << i 
            << "] = " 
            << arr[i]
            << std::endl;
    }

    return 0;
}