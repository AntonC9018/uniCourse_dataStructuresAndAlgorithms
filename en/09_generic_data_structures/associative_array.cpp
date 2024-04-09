#include <cstdint>
#include <iostream>
#include <string_view>
#include <array>
#include <cassert>

struct BucketNode
{
    std::string_view key;
    int value;
    BucketNode* next;
};

static inline const size_t BUCKET_COUNT = 64;

using HashFunc = size_t(*)(std::string_view key);
// using HashFunc = std::function<size_t(std::string_view)>;

struct AssociativeArray
{
    std::array<BucketNode*, BUCKET_COUNT> buckets;
    HashFunc hashFunc;
};

struct AddOrGetElementResult
{
    int* value;
    bool added;
};

size_t computeIndexOfKey(AssociativeArray* arr, std::string_view key)
{
    size_t hash = arr->hashFunc(key);
    size_t index = hash % arr->buckets.size();
    return index;
}

AddOrGetElementResult addOrGetElement(AssociativeArray* arr, std::string_view key)
{
    size_t index = computeIndexOfKey(arr, key);
    BucketNode** currentNode = &arr->buckets[index];
    while (true)
    {
        if (*currentNode == nullptr)
        {
            BucketNode* node = new BucketNode;
            node->key = key;
            node->next = nullptr;
            *currentNode = node;

            return { &node->value, true };
        }
        else if ((*currentNode)->key == key)
        {
            int* valueAddress = &(*currentNode)->value;
            return { valueAddress, false };
        }
        else
        {
            currentNode = &(*currentNode)->next;
        }
    }
}

int* getElement(AssociativeArray* arr, std::string_view key)
{
    size_t index = computeIndexOfKey(arr, key);
    BucketNode* currentNode = arr->buckets[index];
    while (currentNode != nullptr)
    {
        if (currentNode->key == key)
        {
            return &currentNode->value;
        }
        currentNode = currentNode->next;
    }
    return nullptr;
}

size_t dumbHashFunc(std::string_view key)
{
    if (key.empty())
    {
        return 0;
    }

    uint8_t firstLetter = key[0];
    uint8_t positionInAlphabet = firstLetter - static_cast<uint8_t>('a');
    return static_cast<size_t>(positionInAlphabet);
}

int main()
{
    AssociativeArray arr;
    arr.buckets = {};
    arr.hashFunc = dumbHashFunc;

    {
        AddOrGetElementResult result = addOrGetElement(&arr, "abc");
        assert(result.added == true);
        *result.value = 1;
    }
    {
        AddOrGetElementResult result = addOrGetElement(&arr, "bc");
        assert(result.added == true);
        *result.value = 2;
    }
    {
        AddOrGetElementResult result = addOrGetElement(&arr, "a");
        assert(result.added == true);
        *result.value = 3;
    }
    {
        AddOrGetElementResult result = addOrGetElement(&arr, "c");
        assert(result.added == true);
        *result.value = 4;
    }

    {
        AddOrGetElementResult result = addOrGetElement(&arr, "c");
        assert(result.added == false);
        assert(*result.value == 4);
    }

    {
        int* a = getElement(&arr, "a");
        assert(a != nullptr);
        assert(*a == 3);
    }

    std::cout << "All tests went fine" << std::endl;
}
