
#include <array>
#include <iostream>
#include <span>

void insertionSort(std::span<int> arr)
{
    size_t sortedCount = 0;

    while (sortedCount < arr.size())
    {
        int addedElement = arr[sortedCount];

        size_t targetPosition = 0;
        for (size_t i = sortedCount; i >= 1; i--)
        {
            int currentElement = arr[i - 1];
            if (currentElement < addedElement)
            {
                targetPosition = i;
                break;
            }
        }

        for (size_t newIndex = sortedCount; newIndex > targetPosition; newIndex--)
        {
            size_t oldIndex = newIndex - 1;
            arr[newIndex] = arr[oldIndex];
        }

        arr[targetPosition] = addedElement;
        sortedCount += 1;
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
