#include "linked_list_impl.cpp"
#include <array>
#include <iostream>

struct Queue
{
    LinkedList list;
};

void enqueue(Queue* queue, int value)
{
    addNodeToEnd(&queue->list, value);
}

int dequeue(Queue* queue)
{
    int result = removeFromStart(&queue->list);
    return result;
}

bool isEmpty(const Queue* queue)
{
    return isEmpty(&queue->list);
}

int main()
{
    std::array arr{ 1, 2, 3, 4, 5 };
    Queue queue{};
    for (int v : arr)
    {
        enqueue(&queue, v);
    }

    while (!isEmpty(&queue))
    {
        int item = dequeue(&queue);
        std::cout << item << std::endl;
        if (item == 3)
        {
            enqueue(&queue, 10);
        }
    }

    return 0;
}
