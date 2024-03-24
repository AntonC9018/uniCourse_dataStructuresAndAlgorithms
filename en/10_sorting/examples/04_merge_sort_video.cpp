#include <iostream>
#include <array>
#include <span>

void deleteMergeArr(std::span<int> arr)
{
    if (arr.size() < 2)
    {
        return;
    }

    delete[] arr.data();
}

std::span<int> allocMergeArr(std::span<int> arr)
{
    if (arr.size() >= 2)
    {
        return arr;
    }
    if (arr.size() == 0)
    {
        return { (int*) nullptr, 0 };
    }
    int* resultPointer = new int[1]{ arr[0] };
    return { resultPointer, 1 };
}

std::span<int> mergeSort(std::span<int> arr)
{
    if (arr.size() <= 1)
    {
        return arr;
    }

    // Floor
    size_t middle = arr.size() / 2;
    size_t leftSize = middle;
    size_t rightSize = arr.size() - leftSize;

    int* leftStart = arr.data();
    std::span<int> leftArr{ leftStart, leftSize };

    int* rightStart = arr.data() + leftSize;
    std::span<int> rightArr{ rightStart, rightSize };

    std::span<int> sortedLeftArr = mergeSort(leftArr);
    std::span<int> sortedRightArr = mergeSort(rightArr);

    size_t leftIndex = 0;
    size_t rightIndex = 0;
    size_t resultIndex = 0;
    int* resultPointer = new int[arr.size()];
    std::span<int> resultArr{ resultPointer, arr.size() };

    while (leftIndex < sortedLeftArr.size() 
            && rightIndex < sortedRightArr.size())
    {
        int leftEl = sortedLeftArr[leftIndex];
        int rightEl = sortedRightArr[rightIndex];
        if (leftEl < rightEl)
        {
            resultArr[resultIndex] = leftEl;
            leftIndex++;
            resultIndex++;
        }
        else
        {
            resultArr[resultIndex] = rightEl;
            rightIndex++;
            resultIndex++;
        }
    }

    while (leftIndex < sortedLeftArr.size())
    {
        resultArr[resultIndex] = sortedLeftArr[leftIndex];
        leftIndex++;
        resultIndex++;
    }

    while (rightIndex < sortedRightArr.size())
    {
        resultArr[resultIndex] = sortedRightArr[rightIndex];
        rightIndex++;
        resultIndex++;
    }

    deleteMergeArr(sortedLeftArr);
    deleteMergeArr(sortedRightArr);

    return resultArr;
}

int main()
{
    std::array arr{11, 5, 8, 15, 21, 32, 1, 7};
    std::span<int> sortedArray = mergeSort(arr);

    for (int el : sortedArray)
    {
        std::cout << el << ", ";
    }

    deleteMergeArr(sortedArray);
}
