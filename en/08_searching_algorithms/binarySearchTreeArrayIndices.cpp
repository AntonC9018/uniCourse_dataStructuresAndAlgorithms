#include <array>
#include <iostream>
#include <vector>

struct Node
{
    int value;
    size_t left;
    size_t right;
};

static const inline size_t INVALID_INDEX = 0;

struct BinarySearchTree
{
    std::vector<Node> nodes;
};

BinarySearchTree createBinarySearchTree(size_t capacity)
{
    BinarySearchTree result {};
    result.nodes.reserve(capacity);
    return result;
}

Node* find(BinarySearchTree* tree, int value)
{
    if (tree->nodes.size() == 0)
    {
        return nullptr;
    }

    size_t currentNodeIndex = 0;
    while (true)
    {
        Node* currentNode = &tree->nodes[currentNodeIndex];
        if (currentNode->value == value)
        {
            // currentNode is the target node;
            break;
        }
        else if (value < currentNode->value)
        {
            currentNodeIndex = currentNode->left;
        }
        else
        {
            currentNodeIndex = currentNode->right;
        }

        if (currentNodeIndex == INVALID_INDEX)
        {
            return nullptr;
        }
    }

    return &tree->nodes.at(currentNodeIndex);
}

Node* addNode(BinarySearchTree* tree, int value)
{
    size_t newNodeIndex = tree->nodes.size();
    tree->nodes.push_back({});
    Node* node = &tree->nodes.at(newNodeIndex);
    node->value = value;
    node->left = INVALID_INDEX;
    node->right = INVALID_INDEX;

    if (newNodeIndex == 0)
    {
        return node;
    }

    Node* currentNode = &tree->nodes[0];
    while (true)
    {
        if (value > currentNode->value)
        {
            if (currentNode->right != INVALID_INDEX)
            {
                currentNode = &tree->nodes[currentNode->right];
            }
            else
            {
                currentNode->right = newNodeIndex;
                break;
            }
        }
        else
        {
            if (currentNode->left != INVALID_INDEX)
            {
                currentNode = &tree->nodes[currentNode->left];
            }
            else
            {
                currentNode->left = newNodeIndex;
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
    if (node->left != INVALID_INDEX)
    {
        std::cout << tree.nodes[node->left].value << std::endl;
    }
    if (node->right != INVALID_INDEX)
    {
        std::cout << tree.nodes[node->right].value << std::endl;
    }
    return 0;
}
