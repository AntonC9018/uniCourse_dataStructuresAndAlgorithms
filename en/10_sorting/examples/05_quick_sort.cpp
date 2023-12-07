#include "common.h"
#include <iostream>

// O(N log(N)) -- execution
// O(log N) -- memory
void quickSort(std::span<int> arr)
{
    if (arr.size() <= 1)
        return;

    size_t pivotIndex = 0;
    int pivotValue = arr[pivotIndex];
    size_t lessThanCounter = 0;
    for (size_t i = 1; i < arr.size(); i++)
    {
        if (arr[i] >= pivotValue)
            continue;

        lessThanCounter++;

        int lesserValue = arr[i];
        int otherValue = arr[lessThanCounter];

        arr[i] = otherValue;
        arr[lessThanCounter] = lesserValue;
    }

    arr[pivotIndex] = arr[lessThanCounter];
    arr[lessThanCounter] = pivotValue;

    {
        int* leftStart = arr.data(); // &arr[0]
        size_t leftLength = lessThanCounter;
        quickSort({ leftStart, leftLength });
    }
    {
        size_t rightStartIndex = lessThanCounter + 1;
        int* rightStart = &arr[rightStartIndex];
        size_t rightLength = arr.size() - rightStartIndex;
        quickSort({ rightStart, rightLength });
    }
}

int main()
{
    std::array arr = { 5, 4, 3, 9, 1, 10, 1, 8, 12 };
    quickSort(arr);
    assertSorted(arr);
    return 0;
}