#include <assert.h>

struct Node
{
    int value;
    Node* nextNode;
};

struct LinkedList
{
    Node* firstNode;
    Node* lastNode;
};

Node* addNodeToEnd(LinkedList* list, int value) // enqueue
{
    Node* newNode = new Node;
    newNode->nextNode = nullptr; // 0
    newNode->value = value;

    if (list->lastNode != nullptr)
    {
        list->lastNode->nextNode = newNode;
    }
    
    list->lastNode = newNode;

    if (list->firstNode == nullptr)
    {
        list->firstNode = newNode;
    }

    return newNode;
}

int removeFromStart(LinkedList* list) // dequeue
{
    assert(list->firstNode != nullptr);

    Node* firstNode = list->firstNode;
    Node* secondNode = firstNode->nextNode;

    if (firstNode == list->lastNode)
    {
        list->lastNode = nullptr;
    }

    list->firstNode = secondNode;

    int value = firstNode->value;
    delete firstNode;
    return value;
}

void removeAfter(LinkedList* list, Node* node)
{
    assert(node->nextNode != nullptr);

    Node* elementToDelete = node->nextNode;
    Node* elementAfterElementToDelete = elementToDelete->nextNode;

    node->nextNode = elementAfterElementToDelete;

    // if (elementToDelete->nextNode == nullptr)
    if (elementToDelete == list->lastNode)
    {
        list->lastNode = node;
    }

    delete elementToDelete;
}


int main()
{
    LinkedList list{};
    addNodeToEnd(&list, 1);
    addNodeToEnd(&list, 2);
}