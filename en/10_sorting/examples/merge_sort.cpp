// log_2(N)


#include "common.h"

using MergeResult = std::span<int>;

MergeResult createMergeResultBuffer(size_t size)
{
    int* buffer = new int[size];
    return { buffer, size };
}

void deleteMergeResultBuffer(MergeResult buffer)
{
    delete[] buffer.data();
}

// O(log_2(N) * N) = O(N log(N))
// O(2N) = O(N)
MergeResult mergeSort(std::span<int> arr)
{
    if (arr.size() == 0)
    {
        return MergeResult{};
    }

    if (arr.size() == 1)
    {
        MergeResult result = createMergeResultBuffer(arr.size());
        result[0] = arr[0];
        return result;
    }

    size_t size = arr.size();
    size_t halfSize = size / 2;

    // 2 * X 
    // M was N     M --> N / 2        log_2(N) = 10       log_2(N / 2) = 9
    MergeResult left = mergeSort({ &arr[0], halfSize });
    MergeResult right = mergeSort({ &arr[halfSize], size - halfSize });
    
    MergeResult result = createMergeResultBuffer(size);

    size_t leftIndex = 0;
    size_t rightIndex = 0;
    size_t resultIndex = 0;
    // N
    while (leftIndex < left.size() && rightIndex < right.size())
    {
        int leftValue = left[leftIndex];
        int rightValue = right[rightIndex];

        if (leftValue < rightValue)
        {
            result[resultIndex] = leftValue;
            leftIndex++;
        }
        else
        {
            result[resultIndex] = rightValue;
            rightIndex++;
        }
        resultIndex++;
    }
    while (leftIndex < left.size())
    {
        result[resultIndex] = left[leftIndex];
        leftIndex++;
        resultIndex++;
    }
    while (rightIndex < right.size())
    {
        result[resultIndex] = right[rightIndex];
        rightIndex++;
        resultIndex++;
    }

    deleteMergeResultBuffer(left);
    deleteMergeResultBuffer(right);
    return result;
}

int main()
{
    std::array arr = { 5, 4, 3, 9, 1 };
    MergeResult result = mergeSort(arr);
    assertSorted(result);
    deleteMergeResultBuffer(result);
    return 0;
}