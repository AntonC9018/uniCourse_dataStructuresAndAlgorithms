#include <assert.h>
#include "linked_list_impl.cpp"

int main()
{
    LinkedList list{};
    addNodeToEnd(&list, 1);
    addNodeToEnd(&list, 2);
}
