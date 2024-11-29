#include <array>
#include <iostream>

struct BufferListNode
{
    BufferListNode* next;
    std::array<float, 8> items;
};

// Creates 4 blocks of 8 floats
// | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
// | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
// | 0 | 2 | 4 | 6 | 8 | 10| 12| 14|
// | 0 | 3 | 6 | 9 | 12| 15| 18| 21|
BufferListNode* createTestBuffer()
{
    BufferListNode* head = new BufferListNode;
    head->items.fill(1.0f);

    BufferListNode* node = head;
    for (int i = 0; i < 3; i++)
    {
        BufferListNode* newNode = new BufferListNode;
        node->next = newNode;
        node = newNode;
        
        for (size_t j = 0; j < newNode->items.size(); j++)
        {
            newNode->items[j] = static_cast<float>(i * j);
        }
    }

    node->next = nullptr;
    return head;
}

using ItemFunc = void(*)(float&);

void forEachItem(BufferListNode* head, ItemFunc func)
{
    BufferListNode* node = head;
    while (node != nullptr)
    {
        for (size_t i = 0; i < node->items.size(); i++)
        {
            func(node->items[i]);
        }
        node = node->next;
    }
}

void printFunc(float& item)
{
    std::cout << item << ", ";
}

void add5Func(float& item)
{
    item += 5;
}

int main()
{
    BufferListNode* head = createTestBuffer();

    {
        // store the address of printFunc.
        // & is optional.
        ItemFunc func = &printFunc;

        // prints each element
        forEachItem(head, func); 

        std::cout << std::endl;
    }

    {
        ItemFunc func = add5Func;
        forEachItem(head, func); // adds 5 to each element
    }
    
    forEachItem(head, printFunc); // prints each element, again
    std::cout << std::endl;
}
