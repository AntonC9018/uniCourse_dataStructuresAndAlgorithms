#include <iostream>
#include <assert.h>
#include <array>

struct Stack
{
    int* arr;
    size_t maxElementCount;
    size_t currentIndex = 0;
};

void pushElement(Stack* stack, int value)
{
    size_t maxElementCount = stack->maxElementCount;
    assert(stack->currentIndex < maxElementCount);

    stack->arr[stack->currentIndex] = value;
    stack->currentIndex = stack->currentIndex + 1;
}


size_t getElementCount(Stack* stack);
int popElement(Stack* stack)
{
    assert(getElementCount(stack) > 0);
    size_t newCurrentIndex = stack->currentIndex - 1;
    int value = stack->arr[newCurrentIndex];
    stack->currentIndex = newCurrentIndex;
    return value;
}

size_t getElementCount(Stack* stack)
{
    return stack->currentIndex;
}

size_t getMaxElementCount(Stack* stack)
{
    return stack->maxElementCount;
}

int getElementAtIndex(Stack* stack, size_t index)
{
    // 15 | 22 | 10 | ** | ... 
    // 3
    size_t elementCount = getElementCount(stack);
    assert(index < elementCount);
    return stack->arr[index];
}

Stack createDynamicStack(size_t maxElementCount)
{
    void* memoryBlock = malloc(maxElementCount * sizeof(int));
    int* arr = (int*) memoryBlock;

    Stack stack;
    stack.arr = arr;
    stack.maxElementCount = maxElementCount;
    stack.currentIndex = 0;

    return stack;
}

void destroyDynamicStack(Stack* stack)
{
    free(stack->arr);
}


int main()
{
    std::cout << "Enter max number of elements" << std::endl;
    size_t maxElementCount;
    std::cin >> maxElementCount;
    Stack stack = createDynamicStack(maxElementCount);

    for (size_t i = 0; i < getMaxElementCount(&stack); i++)
    {
        std::cout << "Enter a number: ";
        int input;
        std::cin >> input;

        if (input == -1)
        {
            break;
        }
        pushElement(&stack, input);
    }

    size_t elementCount = getElementCount(&stack);
    for (size_t i = 0; i < elementCount; i++)
    {
        int topElement = popElement(&stack);
        std::cout 
            << topElement
            << std::endl;
    }

    std::cout 
        << "Number of elements left in the stack = "
        << getElementCount(&stack)
        << std::endl;

    destroyDynamicStack(&stack);

    return 0;
}