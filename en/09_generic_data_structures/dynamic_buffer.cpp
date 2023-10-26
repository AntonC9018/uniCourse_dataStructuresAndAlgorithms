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
    int* arr;
    size_t maxElementCount;
    size_t currentIndex = 0;
};

void pushElement(Stack* buffer, int value)
{
    size_t maxElementCount = buffer->maxElementCount;
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
    return buffer->maxElementCount;
}

int getElementAtIndex(Stack* buffer, size_t index)
{
    // 15 | 22 | 10 | ** | ... 
    // 3
    size_t elementCount = getElementCount(buffer);
    assert(index < elementCount);
    return buffer->arr[index];
}

Stack createDynamicBuffer(size_t maxElementCount)
{
    void* memoryBlock = malloc(maxElementCount * sizeof(int));
    int* arr = (int*) memoryBlock;

    Stack buffer;
    buffer.arr = arr;
    buffer.maxElementCount = maxElementCount;
    buffer.currentIndex = 0;

    return buffer;
}

void destroyDynamicBuffer(Stack* buffer)
{
    free(buffer->arr);
}


int main()
{
    std::cout << "Enter max number of elements" << std::endl;
    size_t maxElementCount;
    std::cin >> maxElementCount;
    Stack buffer = createDynamicBuffer(maxElementCount);

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

    destroyDynamicBuffer(&buffer);

    return 0;
}