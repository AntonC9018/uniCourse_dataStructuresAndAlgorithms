# Laboratory Work 3

Topic: **Linked Lists**

## Linked lists

Write the code for the following data structures.

> You may allocate memory dynamically on the heap using `new` or `malloc`, separately for each node.
> You may use the [examples](../../../en/09_generic_data_structures).

You may use `template<typename T>`.

1. Singly linked list:
    - The structure must have fields for pointers to the first and last nodes of the list;

    - `Node* insertAfter(LinkedList* list, Node* node, int value)` creates a new node
      and adds it after the given node.
      If `node == nullptr`, the node is added to the beginning of the list.
      Returns a pointer to the created node;

    - `FindNodeResult find(LinkedList* list, int value)` searches for a node with the specified value in the list
      and returns both that node and the node preceding it.
      Define `FindNodeResult` yourself.

      If you use a `template`, you may add another parameter and pass a search functor;

    - `void removeAfter(LinkedList* list, Node* node)` removes the node following the given node from the list.
      If `node == nullptr`, the first node of the list is removed;

    - `void assertNoCycles(LinkedList* list)` verifies that there are no cycles in the list.
      Use this function to test your implementation; you may use `assert` in other functions to ensure that this
      condition holds (this is called a `contract`).
      This function is rather difficult to implement without additional information in the structure,
      so I also recommend that you store the current number of nodes in the `LinkedList` structure.
      In this function, simply count the length again. If the count becomes greater than the stored length,
      there is a cycle somewhere.

2. Doubly linked list:
    - The structure must have fields for pointers to the first and last nodes of the list;

    - `Node* insertAfter(LinkedList* list, Node* node, int value)`;

    - `Node* insertBefore(LinkedList* list, Node* node, int value)`;

    - `Node* find(LinkedList* list, int value)` searches for a node with the given value in the list
      (the notes above about `find` also apply);

    - `void remove(LinkedList* list, Node* node)` removes a node from the list;

    - `void assertNoCycles(LinkedList* list)` verifies that there are no cycles in the list.
      You can use either the length-based approach or verify this by checking
      the links in all nodes and at both ends of the list, since each node
      can have at most 2 links.

Write test functions for each function and call them in `main`.
