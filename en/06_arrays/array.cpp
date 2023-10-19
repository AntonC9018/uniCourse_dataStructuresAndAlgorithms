int main()
{
    // | 18 | 10 | 10 | 10 | 10 |
    int arr[5] = {};
    arr[0] = 8;

    // for (int i = 0; i < 5; i++)
    // {
    //     arr[i] = arr[i] + 10;
    // }

    {
        int i = 0;
        while (i < 5)
        {
            arr[i] = arr[i] + 10;
            i++;
        }
    }

    sum(&arr[0], 5); // pass length explicitly
    sum(&arr[0], sizeof(arr) / sizeof(arr[0])); // 20 / 4 = 5
}

int sum(int* arr, size_t length)
{
    int result = 0;
    for (size_t i = 0; i < length; i++)
    {
        result += arr[i];
        // result = result + *(arr + i);
    }
    return result;
}