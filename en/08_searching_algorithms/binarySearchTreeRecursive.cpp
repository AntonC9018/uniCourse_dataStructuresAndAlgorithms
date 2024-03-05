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
    Node* r = findInSubtree(nextSubtreeRoot, value);
    return r;
}

Node* find(BinarySearchTree tree, int value)
{
    return findInSubtree(tree.root, value);
}

void addNodeIntoSubtree(Node* subtreeRoot, Node* newNode)
{
    Node** nextSubtreeRoot;
    if (newNode->value > subtreeRoot->value)
    {
        nextSubtreeRoot = &subtreeRoot->right;
    }
    else
    {
        nextSubtreeRoot = &subtreeRoot->left;
    }

    if (*nextSubtreeRoot == nullptr)
    {
        *nextSubtreeRoot = newNode;
    }
    else
    {
        addNodeIntoSubtree(*nextSubtreeRoot, newNode);
    }
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

    addNodeIntoSubtree(tree->root, node);

    return node;
}

int main()
{
    std::array values{5, 7, 2, 6, 9, 10, 8};
    BinarySearchTree tree;
    tree.root = nullptr;

    for (size_t i = 0; i < values.size(); i++)
    {
        int currentValue = values[i];
        addNode(&tree, currentValue);
    }

    Node* node = find(tree, 9);
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
