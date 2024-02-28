#include <iostream>
#include <assert.h>

static const inline int DEFAULT_CAPACITY = 4;

struct DynamicArray
{
    int* buffer;
    size_t capacity;
    size_t count = 0;
};

void addElement(DynamicArray* arr, int value)
{
    if (arr->capacity <= arr->count)
    {
        size_t newCapacity;
        if (arr->capacity == 0)
        {
            newCapacity = DEFAULT_CAPACITY;
        }
        else
        {
            newCapacity = arr->capacity * 2;
        }

        int* newArr = new int[newCapacity];
        for (size_t i = 0; i < arr->count; i++)
        {
            newArr[i] = arr->buffer[i];
        }
        delete[] arr->buffer;
        arr->buffer = newArr;
    }

    arr->buffer[arr->count] = value;
    arr->count = arr->count + 1;
}

int getElementAtIndex(const DynamicArray* arr, size_t index)
{
    // 15 | 22 | 10 | ** | ... 
    // 3
    assert(index < arr->count);
    return arr->buffer[index];
}

DynamicArray createDynamicArray(size_t capacity = DEFAULT_CAPACITY)
{
    void* memoryBlock = new int[capacity];
    int* mem = (int*) memoryBlock;

    DynamicArray arr;
    arr.buffer = mem;
    arr.capacity = capacity;
    arr.count = 0;

    return arr;
}

void destroyDynamicArray(DynamicArray* arr)
{
    delete[] arr->buffer;
}


int main()
{
    DynamicArray arr = createDynamicArray();

    while (true)
    {
        std::cout << "Enter a number: ";
        int input;
        std::cin >> input;

        if (input == -1)
        {
            break;
        }
        addElement(&arr, input);
    }

    for (size_t i = 0; i < arr.count; i++)
    {
        std::cout 
            << "arr[" 
            << i 
            << "] = " 
            << getElementAtIndex(&arr, i) 
            << std::endl;
    }

    destroyDynamicArray(&arr);

    return 0;
}
