#include <iostream>
#include <string_view>
#include <array>

struct Bucket
{
    int value;
    std::string_view key;
    bool occupied;
};

using HashFunc = size_t(*)(std::string_view key);
static const inline size_t UNDERLYING_ARRAY_LEN = 8;

struct AssociativeArray
{
    HashFunc hashFunc;
    std::array<Bucket, UNDERLYING_ARRAY_LEN> buckets;
};

size_t calculateIndex(AssociativeArray* array, std::string_view key)
{
    const size_t hash = array->hashFunc(key);
    size_t index = hash % array->buckets.size();
    return index;
}

int* addElement(AssociativeArray* array, std::string_view key)
{
    size_t index = calculateIndex(array, key);
    const size_t initialIndex = index;

    while (true)
    {
        Bucket* bucket = &array->buckets[index];
        if (!bucket->occupied)
        {
            bucket->key = key;
            bucket->occupied = true;
            return &bucket->value;
        }

        index = (index + 1) % array->buckets.size();
        if (index == initialIndex)
        {
            return nullptr;
        }
    }
}

int* findElement(AssociativeArray* array, std::string_view key)
{
    size_t index = calculateIndex(array, key);
    const size_t initialIndex = index;

    while (true)
    {
        Bucket* bucket = &array->buckets[index];
        if (!bucket->occupied)
        {
            return nullptr;
        }

        if (bucket->key == key)
        {
            return &bucket->value;
        }

        index = (index + 1) % array->buckets.size();
        if (index == initialIndex)
        {
            return nullptr;
        }
    }
}

size_t firstLetterIndex(std::string_view key)
{
    if (key.empty())
    {
        return 0;
    }

    size_t firstLetter = static_cast<size_t>(key.at(0));
    size_t firstAlphabetLetter = static_cast<size_t>('a');
    return firstLetter - firstAlphabetLetter;
}

int main()
{
    AssociativeArray array{};
    array.hashFunc = firstLetterIndex;

    {
        int* newElement = addElement(&array, "abc");
        *newElement = 2;
    }
    {
        int* newElement = addElement(&array, "c");
        *newElement = 5;
    }
    {
        int* newElement = addElement(&array, "ab");
        *newElement = 6;
    }

    std::cout << "abc: " << *findElement(&array, "abc") << std::endl;
    std::cout << "ab: " << *findElement(&array, "ab") << std::endl;
}
