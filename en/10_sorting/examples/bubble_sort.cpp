#include "common.h"

// (N - 1)(C + N / 2)
// N^2/2 + .. N + C
// O(N^2) -- execution
// O(1) -- memory
void bubbleSort(std::span<int> arr)
{
    // N - 1
    while (arr.size() > 1)
    {
        // M = (N - 1) / 2
        // M - 1
        for (size_t index = 0; index < arr.size() - 1; index++)
        {
            // 5
            int left = arr[index];
            int right = arr[index + 1];

            if (left > right)
            {
                arr[index + 1] = left;
                arr[index] = right;
            }
        }

        // 1
        arr = { arr.begin(), arr.size() - 1 };
    }
}

int main()
{
    std::array arr = { 5, 4, 3, 9, 1 };
    bubbleSort(arr);
    assertSorted(arr);
}