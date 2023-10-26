#include <iostream>
#include <assert.h>
#include <array>

struct Stack
{
    // | ** | ?? | ?? | ?? |
    // | 60 | ** | ?? | ?? |
    // | 60 | 79 | ** | ?? |
    // | 60 | 79 | 42 | ** |
    // | 60 | 79 | 42 | 58 | **
    std::array<int, 4> arr;
    size_t currentIndex = 0;
};

void pushElement(Stack* buffer, int value)
{
    size_t maxElementCount = buffer->arr.size();
    assert(buffer->currentIndex < maxElementCount);

    buffer->arr[buffer->currentIndex] = value;
    buffer->currentIndex = buffer->currentIndex + 1;
}

size_t getElementCount(Stack* buffer)
{
    return buffer->currentIndex;
}

size_t getMaxElementCount(Stack* buffer)
{
    return buffer->arr.size();
}

int getElementAtIndex(Stack* buffer, size_t index)
{
    // 15 | 22 | 10 | ** | ... 
    // 3
    size_t elementCount = getElementCount(buffer);
    assert(index < elementCount);
    return buffer->arr[index];
}


int main()
{
    Stack buffer{};

    for (size_t i = 0; i < getMaxElementCount(&buffer); i++)
    {
        std::cout << "Enter a number: ";
        int input;
        std::cin >> input;

        if (input == -1)
        {
            break;
        }
        pushElement(&buffer, input);
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