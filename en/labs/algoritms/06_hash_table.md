# Lab 6

Topic: **Hash Tables (Associative Arrays)**

## Concept

The idea behind associative arrays is to associate each array element with an arbitrary *key*, rather than necessarily with an index.
For example, an element can be stored using a *string key*.
This can be achieved by applying a hash function to transform a key into a number,
then using that number as an array index after a modulo operation.

When a non-perfect hash function is used—as in most cases—
*several different keys can be transformed into the same index*.
One of the approaches to handling this problem must therefore be implemented.
Popular approaches include maintaining a linked list for each cell and checking keys,
or using the array itself to store colliding elements.
This situation is called a **collision**.

For example, if the hash function returns the position of a key's first letter in the alphabet,
the keys "abc" and "abd" will both produce 0; after the modulo operation, the result will still be 0,
and the elements will be placed at index 0 in the array.

## Linked-list approach

This approach is the most commonly used in practice.
Each cell points to the start of a dynamically allocated list,
where each node contains the key (to check for collisions)
and the value.

The idea is illustrated in the following code fragment:

```cpp
struct BucketNode
{
    T value;
    std::string_view key;
    BucketNode* next;
};

using HashFunc = size_t(*)(std::string_view key);

struct HashTable
{
    std::span<BucketNode*> buckets;
    HashFunc hashFunc;
};

size_t computeIndex(HashTable* table, std::string_view key)
{
    size_t hash = table->hashFunc(key);
    size_t index = hash % table->buckets.size();
    return index;
}

T* find(HashTable* table, std::string_view key)
{
    size_t index = computeIndex(table, key);
    BucketNode* currentNode = table->buckets[index];
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
```

Fully implement this approach in code:
- The `add` function, which allocates a new node for an element with the specified key.
  It must return the address of the new node's `value` so that the value can be copied there;
- The `createHashTable` function, which creates an associative array with the specified `capacity` (the number of `bucket`s)
  and returns the created associative array;
- The `remove` function, which deletes a value by its key (that is, removes the node from its bucket);
- The `free` function, which frees the nodes and the dynamically allocated array (if one is used);
- Demonstrate its use.

You may keep the bucket array at a fixed size,
either by specifying a `capacity` parameter at creation or by using std::array with a maximum size.


## Open addressing (linear probing)

Instead of placing a value that causes a collision in a linked list within its cell, place it in the next available cell.
This approach is simpler than the previous one, but it limits the maximum number of elements in the table
to the number of cells and, on average, makes finding the required cell take longer.

```cpp
struct Bucket
{
    bool occupied;
    std::string_view key;
    T value;
};

struct HashTable
{
    std::span<Bucket> buckets;
    HashFunc hashFunc;
};

T* find(HashTable* table, std::string_view key)
{
    size_t index = computeIndex(table, key);
    const size_t startIndex = index;
    while (true)
    {
        Bucket* bucket = &table->buckets[index];
        if (bucket->occupied == false)
        {
            return nullptr;
        }
        if (bucket->key == key)
        {
            return &bucket->value;
        }

        index++;
        // Wrap around the edge.
        index = index % table->buckets.size();

        // Traversed the whole array, didn't find the bucket.
        if (index == startIndex)
        {
            return nullptr;
        }
    }
}
```

When adding an element, find the first free cell
by traversing the cells as in the `find` code above, and store the value there.

Implement the same interface as in the previous section.
Implementing a correct `remove` is much more difficult, so you may omit it.

## Analysis

Explain which factors affect the time complexity of insertion and lookup in an associative array.

Explain why, for a perfect hash function, lookup consistently takes a fixed number of operations.

Explain how much lookup speed degrades when using the worst hash function (one that always returns 0).

Explain how the number of cells affects the complexity.

## Additional -- resizing (Advanced level, optional)

Make it possible to add any number of elements to the associative array.
When the ratio of the number of elements to the number of cells reaches a specified threshold
(specified as a parameter at creation or as a constant in the code),
double the size of the array and insert all elements from the old array into the new one (rehashing).
