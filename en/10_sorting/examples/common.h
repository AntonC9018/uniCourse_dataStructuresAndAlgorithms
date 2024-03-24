#include <span>
#include <array>
#include <cassert>

static void assertSorted(std::span<int> arr)
{
    for (size_t i = 1; i < arr.size(); i++)
    {
        assert(arr[i - 1] <= arr[i]);
    }
}
