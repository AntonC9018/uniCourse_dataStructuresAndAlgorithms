#include <cstddef>
#include <iostream>
#include <ostream>
#include <span>
#include <cassert>

struct Iliffe
{
    void* arr;
    size_t numDimensions;
    size_t* dimensionSize;
};

void* createArrayAtLevel(
    std::span<size_t> dimensionSizes,
    size_t currentDimensionIndex,
    int* currentElement)
{
    const size_t currentDimensionSize = dimensionSizes[currentDimensionIndex];
    if (currentDimensionIndex == dimensionSizes.size() - 1)
    {
        int* const result = new int[currentDimensionSize];
        for (size_t i = 0; i < currentDimensionSize; i++)
        {
            result[i] = (*currentElement);
            (*currentElement)++;
        }
        return result;
    }
    else
    {
        void** const arr = new void*[currentDimensionSize];
        const size_t nextDimensionIndex = currentDimensionIndex + 1;
        for (size_t i = 0; i < currentDimensionSize; i++)
        {
            void* const newArr = createArrayAtLevel(
                dimensionSizes,
                nextDimensionIndex,
                currentElement);
            arr[i] = newArr;
        }
        return arr;
    }
}

Iliffe createIliffe(std::span<size_t> dimensionSizes)
{
    size_t* dimensionSizesCopy = new size_t[dimensionSizes.size()];
    for (size_t i = 0; i < dimensionSizes.size(); i++)
    {
        dimensionSizesCopy[i] = dimensionSizes[i];
    }

    int count = 0;
    void* arr = createArrayAtLevel(dimensionSizes, 0, &count);
    std::cout << "Count is: " << count << std::endl;

    return {
        arr,
        dimensionSizes.size(),
        dimensionSizesCopy,
    };
}

int* elementAtIndex(Iliffe* iliffe, std::span<size_t> indices)
{
    assert(indices.size() == iliffe->numDimensions);
    void* currentArray = iliffe->arr;
    for (size_t i = 0; i < indices.size() - 1; i++)
    {
        size_t index = indices[i];
        assert(index < iliffe->dimensionSize[i]);

        void** arrayOfPointers = static_cast<void**>(currentArray);
        currentArray = arrayOfPointers[index];
    }

    {
        int* lastLevelArray = static_cast<int*>(currentArray);

        size_t index = indices[indices.size() - 1];
        assert(index < iliffe->dimensionSize[indices.size() - 1]);

        return &lastLevelArray[index];
    }
}

void deleteIliffeArray(
    void* arr,
    std::span<size_t> dimensionSizes,
    size_t currentDimensionIndex)
{
    if (currentDimensionIndex == dimensionSizes.size() - 1)
    {
        int* numbers = (int*) arr;
        delete[] numbers;
    }
    else
    {
        void** pointerArray = (void**) arr;
        
        const size_t currentDimensionSize = dimensionSizes[currentDimensionIndex];
        const size_t nextDimensionIndex = currentDimensionIndex + 1;
        for (size_t i = 0; i < currentDimensionSize; i++)
        {
            deleteIliffeArray(
                pointerArray[i],
                dimensionSizes,
                nextDimensionIndex);
        }

        delete[] pointerArray;
    }
}

void deleteIliffe(Iliffe* iliffe)
{
    deleteIliffeArray(
        iliffe->arr,
        { iliffe->dimensionSize, iliffe->numDimensions },
        0);
}

int main()
{
    std::array<size_t, 3> indices{ 3, 4, 5 };
    Iliffe arr = createIliffe(indices);

    {
        // (0,1,2,3,4)      | (5,6,7,8,9) | (10,11,12,13,14) | (15,16,17,18,19) 
        // (20,21,22,23,24) | ()          | ()               | () 
        // () | () | () | () 
        std::array<size_t, 3> i{ 1, 0, 4 };
        int* element = elementAtIndex(&arr, i);
        std::cout << *element;
    }

    deleteIliffe(&arr);
    return 0;
}
