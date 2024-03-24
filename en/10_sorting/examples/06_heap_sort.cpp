#include <array>
#include <iostream>
#include <span>

void heapify(std::span<int> arr, size_t parentIndex)
{
    while (true)
    {
        size_t leftIndex = parentIndex * 2 + 1;
        size_t rightIndex = parentIndex * 2 + 2;
        size_t indexOfLargest = parentIndex;

        if (leftIndex < arr.size())
        {
            int largest = arr[indexOfLargest];
            int left = arr[leftIndex];
            if (largest < left)
            {
                indexOfLargest = leftIndex;
            }
        }

        if (rightIndex < arr.size())
        {
            int largest = arr[indexOfLargest];
            int right = arr[rightIndex];
            if (largest < right)
            {
                indexOfLargest = rightIndex;
            }
        }

        if (indexOfLargest == parentIndex)
        {
            return;
        }

        {
            int largest = arr[indexOfLargest];
            arr[indexOfLargest] = arr[parentIndex];
            arr[parentIndex] = largest;

            parentIndex = indexOfLargest;
        }
    }
}

void heapSort(std::span<int> arr)
{
    for (size_t i = (arr.size() / 2) + 1; i >= 1; i--)
    {
        heapify(arr, i - 1);
    }

    for (size_t i = 0; i < arr.size(); i++)
    {
        int root = arr[0];
        size_t currentLast = arr.size() - i - 1;
        
        arr[0] = arr[currentLast];
        arr[currentLast] = root;

        size_t newLen = currentLast;
        std::span<int> heapArr{ arr.data(), newLen };

        heapify(heapArr, 0);
    }
}

int main()
{
    std::array arr{11, 5, 8, 15, 21, 32, 1, 7};
    heapSort(arr);

    for (int el : arr)
    {
        std::cout << el << ", ";
    }
}
