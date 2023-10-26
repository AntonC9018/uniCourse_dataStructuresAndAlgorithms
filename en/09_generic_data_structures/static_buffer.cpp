#include <iostream>
#include <assert.h>
#include <array>

struct Buffer
{
    // | ** | ?? | ?? | ?? |
    // | 60 | ** | ?? | ?? |
    // | 60 | 79 | ** | ?? |
    // | 60 | 79 | 42 | ** |
    // | 60 | 79 | 42 | 58 | **
    std::array<int, 4> arr;
    size_t currentIndex = 0;
};

void addElement(Buffer* buffer, int value)
{
    size_t maxElementCount = buffer->arr.size();
    assert(buffer->currentIndex < maxElementCount);

    buffer->arr[buffer->currentIndex] = value;
    buffer->currentIndex = buffer->currentIndex + 1;
}

size_t getElementCount(Buffer* buffer)
{
    return buffer->currentIndex;
}

size_t getMaxElementCount(Buffer* buffer)
{
    return buffer->arr.size();
}

int getElementAtIndex(Buffer* buffer, size_t index)
{
    // 15 | 22 | 10 | ** | ... 
    // 3
    size_t elementCount = getElementCount(buffer);
    assert(index < elementCount);
    return buffer->arr[index];
}


int main()
{
    Buffer buffer{};

    for (size_t i = 0; i < getMaxElementCount(&buffer); i++)
    {
        std::cout << "Enter a number: ";
        int input;
        std::cin >> input;

        if (input == -1)
        {
            break;
        }
        addElement(&buffer, input);
    }

    size_t elementCount = getElementCount(&buffer);
    for (size_t i = 0; i < elementCount; i++)
    {
        std::cout 
            << "arr[" 
            << i 
            << "] = " 
            << getElementAtIndex(&buffer, i) 
            << std::endl;
    }

    return 0;
}