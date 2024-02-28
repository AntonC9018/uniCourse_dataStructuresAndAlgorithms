#include <stdlib.h>

struct Node
{
    int value;
    Node* next;
};

struct Queue
{
    Node* firstNode;
    Node* lastNode;
};

Queue createEmptyQueue()
{
    return {};
}

void enqueue(Queue* queue, int value)
{
    void* newNodeMemory = malloc(sizeof(Node));
    Node* newNode = (Node*) newNodeMemory;

    if (queue->lastNode != nullptr)
    {
        queue->lastNode->next = newNode;
    }

    queue->lastNode = newNode;

    if (queue->firstNode == nullptr)
    {
        queue->firstNode = newNode;
    }

    newNode->value = value;
    newNode->next = nullptr;
}


int main()
{

    return 0;
}
