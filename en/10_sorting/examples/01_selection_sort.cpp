#include "common.h"

// (N - 1)(2 + ((N - 1) / 2 - 1) * 3 + 4)
// (N - 1)(2.5 + N/2)
// N^2/2  + ..N + C
// O(N^2) -- execution
// O(1) -- memory
void selectionSort(std::span<int> arr)
{
    // N - 1
    while (arr.size() > 1)
    {
        // M ~ (N - 1) / 2

        // 2
        size_t indexOfMax = 0;
        int max = arr[0];

        // (M - 1) * 3
        for (size_t i = 1; i < arr.size(); i++)
        {
            // 3
            if (arr[i] > max)
            {
                max = arr[i];
                indexOfMax = i;
            }
        }

        // 3
        int lastElement = arr[arr.size() - 1];
        arr[arr.size() - 1] = max;
        arr[indexOfMax] = lastElement;

        // 1
        arr = { arr.begin(), arr.size() - 1 };
    }
}

int main()
{
    std::array<int, 5> arr = { 5, 4, 3, 9, 1 };
    selectionSort(arr);
    assertSorted(arr);
    return 0;
}

