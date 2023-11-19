#include <iostream>
#include "standard_impl.cpp"

class DFSRange
{
    const Node* root;

public:
    DFSRange(const Node* root) : root(root)
    {
    }

    IteratorDFS begin() const
    {
        return IteratorDFS{this->root};
    }

    IteratorDFS end() const
    {
        return IteratorDFS{};
    }
};

int main()
{
    const std::unique_ptr<Node> root = createGraph();
    const DFSRange range = DFSRange{root.get()};

    for (int value : range)
        std::cout << value << std::endl;
}