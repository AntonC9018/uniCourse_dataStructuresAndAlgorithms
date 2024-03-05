#include <array>
#include <iostream>
#include <cassert>

struct Node
{
    int value;
    Node* left;
    Node* right;
};

struct BinarySearchTree
{
    Node* arr;
    size_t capacity;
    size_t count;
};

BinarySearchTree createBinarySearchTree(size_t capacity)
{
    Node* arr = new Node[capacity];
    return { arr, capacity, 0 };
}

Node* find(BinarySearchTree* tree, int value)
{
    if (tree->count == 0)
    {
        return nullptr;
    }
    Node* currentNode = &tree->arr[0];
    while (currentNode != nullptr)
    {
        if (currentNode->value == value)
        {
            // currentNode is the target node;
            break;
        }
        else if (value < currentNode->value)
        {
            currentNode = currentNode->left;
        }
        else
        {
            currentNode = currentNode->right;
        }
    }

    return currentNode;
}

Node* addNode(BinarySearchTree* tree, int value)
{
    if (tree->capacity == tree->count)
    {
        assert(false);
    }

    Node* node = &tree->arr[tree->count];
    node->value = value;
    node->left = nullptr;
    node->right = nullptr;

    {
        size_t count = tree->count;
        tree->count += 1;

        if (count == 0)
        {
            return node;
        }
    }

    Node* currentNode = &tree->arr[0];
    while (true)
    {
        if (value > currentNode->value)
        {
            if (currentNode->right != nullptr)
            {
                currentNode = currentNode->right;
            }
            else
            {
                currentNode->right = node;
                break;
            }
        }
        else
        {
            if (currentNode->left != nullptr)
            {
                currentNode = currentNode->left;
            }
            else
            {
                currentNode->left = node;
                break;
            }
        }
    }
    return node;
}

int main()
{
    std::array<int, 6> values{1, 5, 3, 4, 9, 7};
    BinarySearchTree tree = createBinarySearchTree(values.size());

    for (size_t i = 0; i < values.size(); i++)
    {
        int currentValue = values[i];
        addNode(&tree, currentValue);
    }

    Node* node = find(&tree, 5);
    if (node == nullptr)
    {
        std::cout << "Node not found" << std::endl;
    }
    if (node->left != nullptr)
    {
        std::cout << node->left->value << std::endl;
    }
    if (node->right != nullptr)
    {
        std::cout << node->right->value << std::endl;
    }
    return 0;
}
