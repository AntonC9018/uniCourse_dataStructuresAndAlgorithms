#include <array>
#include <iostream>

struct Node
{
    int value;
    Node* left;
    Node* right;
};

struct BinarySearchTree
{
    Node* root;
};

Node* find(BinarySearchTree tree, int value)
{
    Node* currentNode = tree.root;
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
    Node* node = new Node;
    node->value = value;
    node->left = nullptr;
    node->right = nullptr;

    if (tree->root == nullptr)
    {
        tree->root = node;
        return node;
    }

    Node* currentNode = tree->root;
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
    BinarySearchTree tree;
    tree.root = nullptr;

    for (size_t i = 0; i < values.size(); i++)
    {
        int currentValue = values[i];
        addNode(&tree, currentValue);
    }

    Node* node = find(tree, 5);
    if (node == nullptr)
    {
        std::cout << "Node not found";
    }
    if (node->left != nullptr)
    {
        std::cout << node->left->value;
    }
    if (node->right != nullptr)
    {
        std::cout << node->right->value;
    }
    return 0;
}
