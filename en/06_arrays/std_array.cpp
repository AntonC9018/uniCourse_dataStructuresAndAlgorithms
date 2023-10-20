#include <array>
int main()
{
    // int arr[5]{};
    // arr[0] = 8;

    std::array<int, 5> arr {};
    arr[0] = 8;

    for (int i = 0; i < 5; i++)
    {
        arr[i] = arr[i] + 10;
    }

    {
        int i = 0;
        while (i < 5)
        {
            arr[i] = arr[i] + 10;
            i++;
        }
    }

    sum(arr);
}

// Don't focus too much on the syntax (the template bit),
// you don't have to remember this yet.
template<int N>
int sum(std::array<int, N> arr)
{
    int result = 0;
    for (size_t i = 0; i < arr.size(); i++)
    {
        result += arr[i];
        // NOTE: can't use pointer arithmetic here.
    }
    return result;
}

#if false

// NOTE: 
// The above copies all elements of the array passed in into the parameter `arr`.
// You can use a pointer (or a reference) if you don't want to copy.
// Example:
template<int N>
int sum(std::array<int, N>* arr)
{
    int result = 0;
    for (size_t i = 0; i < (*arr).size(); i++)
    {
        result += (*arr)[i];
    }
    return result;
}

// Or with a reference:
template<int N>
int sum(std::array<int, N>& arr)
{
    int result = 0;
    for (size_t i = 0; i < arr.size(); i++)
    {
        result += arr[i];
    }
    return result;
}

#endif