#include <iostream>

using Context = uintptr_t;

void add5(Context context)
{
    int* value = reinterpret_cast<int*>(context);
    *value += 5;
}

void printInt(Context context)
{
    int value = static_cast<int>(context);
    std::cout << value;
}

int main()
{
    int value = 0;
    add5(reinterpret_cast<Context>(&value));
    printInt(static_cast<Context>(value)); // 5
    return 0;
}