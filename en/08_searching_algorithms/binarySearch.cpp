#include <span>
#include <array>
#include <iostream>

struct SearchResult
{
    size_t foundIndex;
    bool isElementFound;
};

// | 1 | 3 | 6 | 9 | 15 | 25 |
// 9
//
// | 1 | 3 | 6 | 9 | 15 | 25 |
//   ^       |            ^
// 
// | 1 | 3 | 6 | 9 | 15 | 25 |
//               ^   |     ^
//
// | 1 | 3 | 6 | 9 | 15 | 25 |    3
//               ^
//               ^
//
// | 1 | 3 | 6 | 9 | 15 | 25 |
//               |

SearchResult binarySearch(std::span<int> arr, int elementToFind)
{
    if (arr.empty())
    {
        return { 0, false };
    }

    // This is to account for the case where it would *underflow*.
    //
    // It would underflow when we try to move the high index to the left of the 0th position,
    // which would take it to -1, which is also size_t's max value,
    // so it will make the check pass, even though 
    // the high index is now in front of the low index.
    //
    // You can try and debug the application without this check, and try and search for
    // an element that is smaller than the first element in the array, 
    // to see for youself what I mean.
    if (arr[0] < elementToFind)
    {
        return { 0, false };
    }

    size_t indexLow = 0;
    size_t indexHigh = arr.size() - 1;

    while (indexLow <= indexHigh)
    {
        size_t currentIndex = (indexHigh - indexLow) / 2 + indexLow;
        int currentElement = arr[currentIndex];

        if (elementToFind > currentElement)
        {
            indexLow = currentIndex + 1;
        }
        else if (elementToFind < currentElement)
        {
            indexHigh = currentIndex - 1;
        }
        else // if (elementToFind == currentElement)
        {
            return { currentIndex, true };
        }
    }

    return { 0, false };
}


int main()
{
    std::array arr = { 1, 5, 7, 10, 15, 32, 89 };
    SearchResult result = binarySearch(arr, 0);

    if (result.isElementFound)
    {
        std::cout << "Element found at index " << result.foundIndex;
    }
    else
    {
        std::cout << "Element not found.";
    }

    return 0;
}