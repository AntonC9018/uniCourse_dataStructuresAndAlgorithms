#include <vector>
#include <memory>
#include <iostream>
#include "graph.h"

class IteratorDFS
{
    std::vector<const Node*> stack;
    std::vector<size_t> ownIndexInParentStack;

public:
    IteratorDFS(const Node* root)
    {
        this->stack.push_back(root);
    }

    IteratorDFS(const IteratorDFS& other) : 
        stack(other.stack),
        ownIndexInParentStack(other.ownIndexInParentStack)
    {
    }

    bool empty() const
    {
        return this->stack.empty();
    }

    int value() const
    {
        return this->stack.back()->value;
    }

    void advance()
    {
        const Node* node = this->stack.back();
        if (node->children.size() > 0)
        {
            this->stack.push_back(node->children[0]);
            this->ownIndexInParentStack.push_back(0);
            return;
        }

        while (true)
        {
            this->stack.pop_back();
            if (this->stack.empty())
                return;

            const Node *parent = this->stack.back();

            size_t ownIndex = this->ownIndexInParentStack.back();
            this->ownIndexInParentStack.pop_back();

            size_t nextNodeIndex = ownIndex + 1;

            if (nextNodeIndex < parent->children.size())
            {
                this->stack.push_back(parent->children[nextNodeIndex]);
                this->ownIndexInParentStack.push_back(nextNodeIndex);
                return;
            }

            // Finished with the parent, keep walking up the stack.
        }
    }
};

int main()
{
    const std::unique_ptr<Node> root = createGraph();

    // if (false)
    {
        IteratorDFS it{root.get()};

        while (!it.empty())
        {
            std::cout << it.value() << std::endl;
            it.advance();
        }
    }

    // Could iterate two graphs in lockstep now.
    // if (false)
    {
        IteratorDFS it1{root.get()};
        IteratorDFS it2{root.get()}; // imagine this was a different graph

        int result = 0;
        while (!it1.empty() && !it2.empty())
        {
            result += it1.value() + it2.value();
            it1.advance();
            it2.advance();
        }
    }

    // Can store the state to resume later.
    {
        IteratorDFS it{root.get()};

        // Just skip 3 elements.
        for (int i = 0; i < 3; i++)
            it.advance();

        // Copy the state
        IteratorDFS it2{it};

        // Finish executing the first iterator
        while (!it.empty())
        {
            std::cout << it.value() << std::endl;
            it.advance();
        }

        std::cout << "Iterator 1 finished" << std::endl;

        // Now count the sum with the second iterator
        int result = 0;
        while (!it2.empty())
        {
            result += it2.value();
            it2.advance();
        }

        std::cout << "Iterator 2 computed the sum: " << result << std::endl;
    }

    return 0;
}
