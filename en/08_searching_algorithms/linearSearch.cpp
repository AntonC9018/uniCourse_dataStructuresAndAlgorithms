#include <span>
#include <array>
#include <iostream>

struct SearchResult
{
    size_t foundIndex;
    bool isElementFound;
};

// N / 2 * 1
// N = 1000 -> 1 000 000
// N = 500 -> 500 000
// O(N / 2 + 1) = O(N)
// O(5 * 1) = O(1)
SearchResult linearSearch(std::span<int> arr, int elementToFind)
{
    for (size_t i = 0; i < arr.size(); i++) // N / 2
    {
        int currentElement = arr[i];
        if (currentElement == elementToFind) // 1
        {
            // SearchResult result;
            // result.foundIndex = i;
            // result.isElementFound = true;
            // return result;
            return { i, true };
        }
    }
    return { 0, false };
}

// O(N^2 + N) = O(N^2)

// N * N * 2 = N^2 * 2
// N = 1000 -> 2 000 000
// N = 1 000 000 -> 2 000 000 000 000
// O(N * N * 2) = O(N * N) = O(N^2)
// O(5) = O(1)
int someProduct(std::span<int> arr)
{
    int result = 0;
    for (size_t i = 0; i < arr.size(); i++) // N
    {
        for (size_t j = 0; j < arr.size(); j++) // N
        {
            result += arr[i] * arr[j]; // 2
        }
    }
    return result;
}

int main()
{
    std::array<int, 5> arr = { 1, 6, 2, 5, 9 };
    SearchResult result = linearSearch(arr, 5);

    if (result.isElementFound)
    {
        std::cout << "Element found at index " << result.foundIndex;
    }
    else
    {
        std::cout << "Elemenet not found.";
    }

    return 0;
}
