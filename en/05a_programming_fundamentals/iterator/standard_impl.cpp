#include "graph.h"
#include <vector>
#include <memory>

class IteratorDFS
{
    std::vector<const Node*> stack;
    std::vector<size_t> ownIndexInParentStack;

public:
    IteratorDFS()
    {
    }

    IteratorDFS(const Node* root)
    {
        this->stack.push_back(root);
    }

    IteratorDFS(const IteratorDFS& other) : 
        stack(other.stack),
        ownIndexInParentStack(other.ownIndexInParentStack)
    {
    }

    bool operator==(const IteratorDFS& other) const
    {
        return this->stack == other.stack &&
            this->ownIndexInParentStack == other.ownIndexInParentStack;
    }
    // operator!= added automatically: !(this == other)

    int operator*() const
    {
        return this->stack.back()->value;
    }

    IteratorDFS& operator++() // ++i
    {
        this->advance();
        return *this;
    }

private:
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