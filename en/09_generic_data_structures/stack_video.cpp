#include <cassert>

struct Node
{
    int value;
    Node* next;
};

struct Stack
{
    Node* firstNode;
};

void push(Stack* stack, int value)
{
    Node* node = new Node;
    node->value = value;
    node->next = stack->firstNode;

    stack->firstNode = node;
}

bool isEmpty(const Stack* stack)
{
    return stack->firstNode == nullptr;
}

int pop(Stack* stack)
{
    Node* firstNode = stack->firstNode;
    stack->firstNode = firstNode->next;
    int result = firstNode->value;
    delete firstNode;
    return result;
}

int main()
{
    Stack stack{};

    push(&stack, 1);
    push(&stack, 2);
    push(&stack, 3);

    assert(pop(&stack) == 3);
    assert(pop(&stack) == 2);

    push(&stack, 4);
    assert(pop(&stack) == 4);

    assert(!isEmpty(&stack));

    pop(&stack);

    assert(isEmpty(&stack));
    return 0;
}
