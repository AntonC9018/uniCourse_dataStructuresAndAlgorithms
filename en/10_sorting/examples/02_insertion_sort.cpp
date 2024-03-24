#include <array>
#include <iostream>
#include <span>


void insertionSort(std::span<int> arr)
{
    size_t sortedArraySize = 0;
    while (true)
    {
        if (sortedArraySize == arr.size())
        {
            return;
        }
        int value = arr[sortedArraySize];

        size_t i = sortedArraySize;
        while (i >= 1)
        {
            int nextValue = arr[i - 1];
            size_t nextPosition = i;
            if (nextValue > value)
            {
                arr[nextPosition] = nextValue;
            }
            else
            {
                break;
            }
            i--;
        }
        arr[i] = value;

        sortedArraySize++;
    }
}

int main()
{
    std::array arr{11, 5, 8, 15, 21, 32, 1, 7};
    insertionSort(arr);

    for (int el : arr)
    {
        std::cout << el << ", ";
    }
}
