struct Node
{
    int value;
    Node* next;
};

#include <stdlib.h>

int main()
{
    Node n15;
    n15.value = 15;

    Node n7;
    n7.value = 7;
    n7.next = nullptr; //0;

    n15.next = &n7;

    n15.next->value = 10;


    void* nodeMemory = malloc(sizeof(Node));
    Node* node9 = (Node*) nodeMemory;
    node9->value = 9;
    node9->next = nullptr;

    n7.next = node9;
}