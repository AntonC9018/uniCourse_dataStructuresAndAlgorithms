#include "common.h"

// O(N^2)
// 
// (N - 1) * 4 = 4N - 4 
// O(N) -- memory
void bubbleSort(std::span<int> arr)
{
    if (arr.size() <= 1)
    {
        return;
    }

    for (size_t index = 0; index < arr.size() - 1; index++)
    {
        int left = arr[index];
        int right = arr[index + 1];

        if (left > right)
        {
            arr[index + 1] = left;
            arr[index] = right;
        }
    }

    std::span arr1 = { arr.begin(), arr.size() - 1 };

    bubbleSort(arr1);
}

int main()
{
    std::array<int, 10> arr;
    for (size_t i = 0; i < arr.size(); i++)
    {
        arr[i] = arr.size() - i;
    }

    bubbleSort(arr);
    assertSorted(arr);
}
