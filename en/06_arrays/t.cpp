#include <stdlib.h>

template<size_t N>
int sum(int (&arr)[N])
{
    int result = 0;
    for (size_t i = 0; i < N; i++)
    {
        result += arr[i];
    }
    return result;
}

int main()
{
    int arr[4]{};
    sum(arr);
    return 0;
}