# Lab 5

Topic: **Stack & Queue**

## Stack

Implement a stack.

A stack can be implemented using a dynamic array (`std::vector` or your own implementation) or a linked list.
Implement both variants.

If you have never implemented a dynamic array yourself, I recommend that you do so as well.
An example is available [here](../../../en/09_generic_data_structures/dynamic_array.cpp).

A stack supports the following operations:
- `bool isEmpty(const Stack* stack)` checks whether the stack is empty;
- `void push(Stack* stack, int value)` adds an element to the top of the stack;
- `int* getLastElement(Stack* stack)` (you can name it whatever makes more sense to you) returns the address (or reference) of the top element without removing it;
- `void pop(Stack* stack)` removes the top element (the last one added).

An example is available [here](../../../en/09_generic_data_structures/stack.cpp).
The example differs slightly from the requirements because it uses a stack with a fixed maximum size.


## Queue

Implement a queue.

An unbounded queue can be implemented quite simply using a linked list: remove elements from the beginning and add them to the end.
A fixed-size queue can be implemented with a ring buffer;
with a dynamically resizing ring buffer, the queue can also be made unbounded
(you can come up with creative approaches to expanding the buffer here).

Implement at least one of these approaches (a linked list is the easiest).

A queue supports the following operations:
- `bool isEmpty(const Queue* queue)` checks whether the queue is empty;
- `void enqueue(Queue* queue, int value)` adds an element **to the end** of the queue;
- `int* front(Queue* queue)` returns the address (or reference) of the **first** element in the queue;
- `void dequeue(Queue* queue)` removes an element **from the beginning** of the queue.

An example is available [here](../../../en/09_generic_data_structures/queue.cpp).
However, its basic implementation is essentially a linked list with extra functions
and different function names.
