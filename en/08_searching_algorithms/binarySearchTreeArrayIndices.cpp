#include <array>
#include <iostream>
#include <vector>

struct Node
{
    int value;
    size_t leftIndex;
    size_t rightIndex;
};

struct BinarySearchTree
{
    std::vector<Node> nodes;
};

Node* addNode(BinarySearchTree* tree, int value)
{
    size_t count = tree->nodes.size();
    tree->nodes.push_back({ value, 0, 0 });

    // nodes.push_back({});
    // Node* node = &nodes.back();
    // node->value = value;
    // node->leftIndex = 0;
    // node->rightIndex = 0;

    if (count == 0)
    {
        return &tree->nodes[count];
    }

    size_t currentIndex = 0;
    while (true)
    {
        Node* currentNode = &tree->nodes[currentIndex];
        size_t* indexSlot;
        if (value > currentNode->value)
        {
            indexSlot = &currentNode->rightIndex;
        }
        else
        {
            indexSlot = &currentNode->leftIndex;
        }

        if (*indexSlot == 0)
        {
            *indexSlot = count;
            break;
        }
        else
        {
            currentIndex = *indexSlot;
        }
    }

    return &tree->nodes[count];
}

Node* find(BinarySearchTree* tree, int value)
{
    if (tree->nodes.size() == 0)
    {
        return nullptr;
    }

    size_t currentIndex = 0;
    while (true)
    {
        Node* currentNode = &tree->nodes[currentIndex];
        if (value == currentNode->value)
        {
            return currentNode;
        }

        if (value > currentNode->value)
        {
            currentIndex = currentNode->rightIndex;
        }
        else
        {
            currentIndex = currentNode->leftIndex;
        }

        if (currentIndex == 0)
        {
            return nullptr;
        }
    }
}

void find9AndPrint(BinarySearchTree* tree)
{
    Node* node = find(tree, 9);
    if (node == nullptr)
    {
        std::cout << "Node not found";
    }
    if (node->leftIndex != 0)
    {
        std::cout << tree->nodes[node->leftIndex].value << std::endl;
    }
    if (node->rightIndex != 0)
    {
        std::cout << tree->nodes[node->rightIndex].value << std::endl;
    }
}

int main()
{
    std::array values{5, 7, 2, 6, 9};

    BinarySearchTree tree{{}};

    // nodes.reserve(values.size() * 2);

    for (size_t count = 0; count < values.size(); count++)
    {
        int value = values[count];
        addNode(&tree, value);
    }

    addNode(&tree, 10);
    find9AndPrint(&tree);

    addNode(&tree, 8);
    find9AndPrint(&tree);
}
