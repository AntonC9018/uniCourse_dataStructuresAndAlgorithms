#include <array>
#include <iostream>
#include <span>

void quickSort(std::span<int> arr)
{
    if (arr.size() <= 1)
    {
        return;
    }

    size_t pivotIndex = 0;
    size_t smallerThanPivotIndex = pivotIndex + 1; // a
    size_t currentIndex = smallerThanPivotIndex; // b
    int pivot = arr[pivotIndex];

    while (true)
    {
        int currentElement = arr[currentIndex];
        if (currentElement < pivot)
        {
            int a = arr[smallerThanPivotIndex];
            arr[smallerThanPivotIndex] = currentElement;
            arr[currentIndex] = a;
            smallerThanPivotIndex++;
        }
        currentIndex++;

        if (currentIndex == arr.size())
        {
            break;
        }
    }

    {
        int a = arr[smallerThanPivotIndex - 1];
        arr[smallerThanPivotIndex - 1] = arr[pivotIndex];
        arr[pivotIndex] = a;
    }

    std::span<int> left{ arr.data(), smallerThanPivotIndex - 1 };
    std::span<int> right{ &arr[smallerThanPivotIndex], arr.size() - smallerThanPivotIndex };

    quickSort(left);
    quickSort(right);
}

int main()
{
    std::array arr{11, 5, 8, 15, 21, 32, 1, 7};
    quickSort(arr);

    for (int el : arr)
    {
        std::cout << el << ", ";
    }
}
