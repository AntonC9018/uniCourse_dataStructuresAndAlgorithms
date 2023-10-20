#include <span>
#include <iostream>

// struct std::span
// {
//     int* ptr;
//     size_t length;
// };

int sum(std::span<int> arr);

int main()
{
    int arr[5]{};
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

    std::cout << sum(arr);
}

// std::span = { pointer to first element, length }
int sum(std::span<int> arr)
{
    int result = 0;
    for (size_t i = 0; i < arr.size(); i++)
    {
        result += arr[i];
    }
    return result;
}