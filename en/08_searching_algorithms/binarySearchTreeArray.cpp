#include <array>
#include <iostream>
#include <span>

struct Node
{
    int value;
    Node* left;
    Node* right;
};

Node* find(Node* treeRoot, int value)
{
    Node* currentNode = treeRoot;
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

int main()
{
    std::array numbers{ 5, 7, 2, 6, 9 };

    Node* firstNodeAddress = new Node[numbers.size()];
    std::span<Node> nodes {firstNodeAddress, numbers.size()};

    for (size_t count = 0; count < numbers.size(); count++)
    {
        int value = numbers[count];

        Node* newNode = &nodes[count];
        newNode->value = value;
        newNode->left = nullptr;
        newNode->right = nullptr;

        if (count == 0)
        {
            continue;
        }

        Node* currentNode = &nodes[0];
        while (true)
        {
            if (value > currentNode->value)
            {
                if (currentNode->right == nullptr)
                {
                    currentNode->right = newNode;
                    break;
                }
                else
                {
                    currentNode = currentNode->right;
                }
            }
            else
            {
                if (currentNode->left == nullptr)
                {
                    currentNode->left = newNode;
                    break;
                }
                else
                {
                    currentNode = currentNode->left;
                }
            }
        }
    }

    Node* node = find(&nodes[0], 7);
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
