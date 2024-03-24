#include <cassert>
#include <iostream>
#include <span>

struct LinearArray
{
    std::span<size_t> dimensions;
    int* firstElement;
};

size_t computeTotalSize(std::span<size_t> dimensions)
{
    size_t totalSize = 1;
    for (size_t d : dimensions)
    {
        totalSize *= d;
    }
    return totalSize;
}

LinearArray createLinearArray(std::span<size_t> dimensions)
{
    size_t totalSize = computeTotalSize(dimensions);
    int* memory = new int[totalSize];
    return { dimensions, memory };
}

int* getElementAtIndex(LinearArray* arr, std::span<size_t> indices)
{
    assert(arr->dimensions.size() == indices.size());
    for (size_t i = 0; i < indices.size(); i++)
    {
        assert(indices[i] < arr->dimensions[i]);
    }

#if ROW_MAJOR
    size_t index = indices[indices.size() - 1];
    for (size_t i = indices.size() - 1; i >= 1; i--)
    {
        size_t indexAtDim = indices[i - 1];
        index *= arr->dimensions[i - 1];
        index += indexAtDim;
    }
#else
    size_t index = indices[0];
    for (size_t i = 0; i < indices.size(); i++)
    {
        size_t indexAtDim = indices[i];
        index *= arr->dimensions[i];
        index += indexAtDim;
    }
#endif

    return &arr->firstElement[index];
}

std::span<int> getLinearMemory(LinearArray* arr)
{
    size_t totalSize = computeTotalSize(arr->dimensions);
    return { arr->firstElement, totalSize };
}

int main()
{
    std::array<size_t, 3> dimensions{ 3, 4, 5 };
    LinearArray arr = createLinearArray(dimensions);

    std::cout << arr.dimensions.size() << std::endl;
    for (size_t d : arr.dimensions)
        std::cout << d << std::endl;

    std::span linearMemory = getLinearMemory(&arr);
    for (size_t i = 0; i < linearMemory.size(); i++)
    {
        linearMemory[i] = i;
    }

    for (size_t i0 = 0; i0 < dimensions[0]; i0++)
    {
        for (size_t i1 = 0; i1 < dimensions[1]; i1++)
        {
            std::cout << "(";
            for (size_t i2 = 0; i2 < dimensions[2]; i2++)
            {
                std::array indices = { i0, i1, i2 };
                int* element = getElementAtIndex(&arr, indices);
                std::cout << *element;
                if (i2 != dimensions[2] - 1)
                {
                    std::cout << ", ";
                }
            }
            std::cout << ")";
        }
        std::cout << "\n";
    }

    return 0;
}
