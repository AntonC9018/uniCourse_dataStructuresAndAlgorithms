#include <assert.h>

struct Node
{
    int value;
    Node* nextNode;
    Node* previousNode;
};

struct LinkedList
{
    Node* firstNode;
    Node* lastNode;
};

Node* addNodeToEnd(LinkedList* list, int value)
{
    Node* newNode = new Node;
    newNode->nextNode = nullptr; // 0
    newNode->value = value;

    newNode->previousNode = list->lastNode;

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

void removeFromStart(LinkedList* list)
{
    assert(list->firstNode != nullptr);

    Node* firstNode = list->firstNode;
    Node* secondNode = firstNode->nextNode;

    if (secondNode != nullptr)
        secondNode->previousNode = nullptr;

    if (firstNode == list->lastNode)
        list->lastNode = nullptr;

    list->firstNode = secondNode;

    delete firstNode;
}

void removeFromEnd(LinkedList* list)
{
    assert(list->lastNode != nullptr);

    Node* lastNode = list->lastNode;
    Node* nextToLastNode = lastNode->previousNode;

    if (list->firstNode == lastNode)
    {
        list->firstNode = nullptr;
    }

    if (nextToLastNode != nullptr)
    {
        nextToLastNode->nextNode = nullptr;
    }


    list->lastNode = nextToLastNode;
}


void remove(LinkedList* list, Node* node)
{
    Node* nextNode = node->nextNode;
    Node* previousNode = node->previousNode;

    if (nextNode != nullptr)
    {
        nextNode->previousNode = previousNode;
    }
    else
    {
        assert(list->lastNode == node);
        list->lastNode = previousNode;
    }

    if (previousNode != nullptr)
    {
        previousNode->nextNode = nextNode;
    }
    else
    {
        assert(list->firstNode == node);
        list->firstNode = nextNode;
    }

    delete node;
}


int main()
{
    LinkedList list{};
    Node* n1 = addNodeToEnd(&list, 1);
    Node* n2 = addNodeToEnd(&list, 2);
    Node* n3 = addNodeToEnd(&list, 3);
    Node* n9 = addNodeToEnd(&list, 9);

    remove(&list, n3);
    remove(&list, n9);
}