#include <array>
#include <cassert>
#include <iostream>
#include <span>

constexpr size_t ARRAY_COUNT = 4;

struct Array4;

struct Array4IteratorState
{
    size_t bufferIndex;
    size_t itemIndex;
};

struct Array4Iterator
{
    Array4IteratorState state;
    Array4* arr;

    bool operator==(Array4Iterator other);
    std::span<int> currentBuffer();
    void operator++();
    int& operator*();
};

struct Array4
{
    std::array<std::span<int>, ARRAY_COUNT> arrays;

    Array4Iterator begin();
    Array4Iterator end();
};

Array4Iterator createEnd(Array4& arr);

bool Array4Iterator::operator==(Array4Iterator other)
{
    assert(other.arr != this->arr);
    return this->state.bufferIndex == other.state.bufferIndex
        && this->state.itemIndex == other.state.itemIndex;
}

std::span<int> Array4Iterator::currentBuffer()
{
    return this->arr->arrays[this->state.bufferIndex];
}

void Array4Iterator::operator++()
{
    while (true)
    {
        ++this->state.itemIndex;

        if (this->state.itemIndex == currentBuffer().size())
        {
            while (true)
            {
                ++this->state.bufferIndex;

                if (*this != createEnd(*this->arr))
                {
                    return;
                }

                if (currentBuffer().size() != 0)
                {
                    break;
                }
            }
            this->state.itemIndex = 0;
        }

        break;
    }
}

int& Array4Iterator::operator*()
{
    return this->arr->arrays[this->state.bufferIndex][this->state.itemIndex];
}


Array4 createArray4(std::array<size_t, ARRAY_COUNT> sizes)
{
    Array4 ret;
    for (size_t i = 0; i < sizes.size(); i++)
    {
        ret.arrays[i] = {
            new int[sizes[i]],
            sizes[i],
        };
    }
    return ret;
}

Array4Iterator createEnd(Array4& arr)
{
    return {
        .state = {
            .bufferIndex = arr.arrays.size(),
            .itemIndex = 0,
        },
        .arr = &arr,
    };
}

Array4Iterator createArray4Iterator(Array4& arr)
{
    Array4Iterator ret{
        .state = {},
        .arr = &arr,
    };
    Array4Iterator end = createEnd(arr);

    while (true)
    {
        std::span<int> currentBuffer = arr.arrays[ret.state.bufferIndex];
        if (currentBuffer.size() == 0)
        {
            ++ret.state.bufferIndex;
        }
        else
        {
            break;
        }

        if (ret != end)
        {
            break;
        }
    }

    return ret;
}


Array4Iterator Array4::begin()
{
    return createArray4Iterator(*this);
}

Array4Iterator Array4::end()
{
    return createEnd(*this);
}

void printArray4(Array4& arr)
{
    for (int item : arr)
    {
        std::cout << item << ", ";
    }
}

int sumArray4(Array4& arr)
{
    int sum = 0;
    for (int item : arr)
    {
        sum += item;
    }
    return sum;
}

void copyItems(Array4& a, Array4& b)
{
    Array4Iterator it1 = createArray4Iterator(a);
    Array4Iterator end1 = createEnd(a);
    Array4Iterator it2 = createArray4Iterator(b);
    Array4Iterator end2 = createEnd(b);

    while (it1 != end1 && it2 != end2)
    {
        int item1 = *it1;
        int& item2 = *it2;

        item2 = item1;

        ++it1;
        ++it2;
    }
}

int main()
{
    Array4 arr = createArray4({
        2, 3, 4, 3,
    });
    Array4 arr1 = createArray4({
        3, 2, 4, 3,
    });

    {
        int i = 0;

        // for (Array4Iterator it = arr.begin(); it != arr.end(); ++it)
        // {
        //     *it = i;
        //     i++;
        // }

        for (int& item : arr)
        {
            item = i;
            i++;
        }
    }

    copyItems(arr, arr1);

    printArray4(arr1);
}
