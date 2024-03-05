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

Node* findInSubtree(Node* subtreeRoot, int value)
{
    if (subtreeRoot == nullptr)
    {
        return nullptr;
    }

    if (value == subtreeRoot->value)
    {
        return subtreeRoot;
    }

    Node* nextSubtreeRoot;
    if (value > subtreeRoot->value)
    {
        nextSubtreeRoot = subtreeRoot->right;
    }
    else
    {
        nextSubtreeRoot = subtreeRoot->left;
    }
    return findInSubtree(nextSubtreeRoot, value);
}

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

void internalAddNode(Node* subtreeRoot, Node* node)
{
    Node** nextSubtreeRoot;
    if (node->value > subtreeRoot->value)
    {
        nextSubtreeRoot = &subtreeRoot->right;
    }
    else
    {
        nextSubtreeRoot = &subtreeRoot->left;
    }

    if (*nextSubtreeRoot == nullptr)
    {
        *nextSubtreeRoot = node;
        return;
    }
    internalAddNode(*nextSubtreeRoot, node);
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

    internalAddNode(tree->root, node);
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
