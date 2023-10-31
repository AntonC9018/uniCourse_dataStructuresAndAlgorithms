#include <span>

template<typename T>
T sum(std::span<T> arr)
{
    T result {};
    for (size_t i = 0; i < arr.size(); i++)
        result += arr[i];
    return result;
}