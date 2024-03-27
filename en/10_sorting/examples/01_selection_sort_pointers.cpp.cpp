#include <iostream>
#include <array>
#include <span>

void selectionSort(std::span<int> arr)
{
    size_t sortedCount = 0;

    while (true)
    {
        if (sortedCount + 1 >= arr.size())
        {
            return;
        }

        int* minElement = &arr[sortedCount];
        int* currentElement = minElement + 1;

        while (true)
        {
            if (currentElement > &arr.back())
            {
                break;
            }

            if (*currentElement < *minElement)
            {
                minElement = currentElement;
            }

            currentElement += 1;
        }

        {
            int t = *minElement;
            *minElement = arr[sortedCount];
            arr[sortedCount] = t;
        }

        sortedCount += 1;
    }
}

int main()
{
    std::array arr{11, 5, 8, 15, 21, 32, 1, 7};
    selectionSort(arr);

    for (int el : arr)
    {
        std::cout << el << ", ";
    }
}
