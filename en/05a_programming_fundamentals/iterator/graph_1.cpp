#include <vector>
#include <memory>
#include <iostream>
#include "graph.h"

void printDFS(const Node* node)
{
    std::cout << node->value << std::endl;
    for (size_t i = 0; i < node->children.size(); i++)
        printDFS(node->children[i]);
}

int main()
{
    const std::unique_ptr<Node> root = createGraph();
    printDFS(root.get());
    return 0;
}
