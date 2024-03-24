#include "linked_list_impl.cpp"
#include <array>
#include <iostream>
#include <span>

struct Queue
{
    std::span<int> buffer;
    size_t len;
    size_t currentIndex;
};

Queue createQueue(size_t capacity)
{
    return {
        { new int[capacity], capacity },
        0,
        0,
    };
}

void deleteQueue(Queue* queue)
{
    delete[] queue->buffer.data();
}

bool isEmpty(const Queue* queue)
{
    return queue->len == 0;
}

void enqueue(Queue* queue, int value)
{
    size_t capacity = queue->buffer.size();
    assert(capacity > queue->len);
    queue->buffer[queue->currentIndex] = value;
    queue->currentIndex = (queue->currentIndex + 1) % capacity;
    queue->len += 1;
}

int dequeue(Queue* queue)
{
    size_t capacity = queue->buffer.size();
    assert(!isEmpty(queue));
    size_t oldestItemIndex = (queue->currentIndex + capacity - queue->len) % capacity;
    int result = queue->buffer[oldestItemIndex];
    queue->len -= 1;
    return result;
}

int main()
{
    std::array arr{ 1, 2, 3, 4, 5 };
    Queue queue = createQueue(5);
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

    deleteQueue(&queue);

    return 0;
}
