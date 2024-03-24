#include <iostream>
#include <array>
#include <span>

void selectionSort(std::span<int> arr)
{
    size_t currentIndex = 0;

    // 1*c + 2*c + ... + (N-2)*c + (N-1)*c
    // c(1 ... N-1) = c(1+(N-1) * (N-1)) = c * N *(N-1)
    // N - 1
    // O(c N (N-1)) = O(N(N-1)) = O(N*N) = O(N^2)
    while (true)
    {
        if (currentIndex + 1 >= arr.size())
        {
            return;
        }

        int minElement = arr[currentIndex];
        size_t minIndex = currentIndex;

        // M
        // M = N - 1
        // M = 1
        for (size_t i = currentIndex + 1; i < arr.size(); i++)
        {
            // constant
            if (arr[i] < minElement)
            {
                minIndex = i;
                minElement = arr[i];
            }
        }

        arr[minIndex] = arr[currentIndex];
        arr[currentIndex] = minElement;

        currentIndex++;
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
