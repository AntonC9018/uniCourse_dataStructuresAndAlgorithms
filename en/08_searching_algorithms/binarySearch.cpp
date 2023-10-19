#include <span>
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
// | 1 | 3 | 6 | 10 | 15 | 25 |    3
//               ^
//               ^
//
// | 1 | 3 | 6 | 9 | 15 | 25 |
//               |

SearchResult binarySearch(std::span<int> arr, int elementToFind)
{
    if (arr.size() == 0)
        return { 0, false };

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
    SearchResult result = binarySearch(arr, 89);

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