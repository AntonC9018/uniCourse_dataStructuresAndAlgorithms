#include <array>
#include <iostream>
#include <queue>

static inline const int MAX_NEIGHBOR_COUNT = 2;

struct Node
{
    int version;
    int value;
    std::array<Node*, MAX_NEIGHBOR_COUNT> neighbors;
};

Node* createGraph()
{
    Node* node1 = new Node;
    node1->value = 1;
    node1->version = 0;

    Node* node2 = new Node;
    node2->value = 2;
    node2->version = 0;

    Node* node3 = new Node;
    node3->value = 3;
    node3->version = 0;

    Node* node4 = new Node;
    node4->value = 4;
    node4->version = 0;

    node3->neighbors = {};

    node4->neighbors[0] = node1;
    node4->neighbors[1] = nullptr;

    node2->neighbors[0] = node1;
    node2->neighbors[1] = node4;

    node1->neighbors[0] = node2;
    node1->neighbors[1] = node3;

    return node1;
}

void printNeighborsValues(Node* node)
{
    for (size_t i = 0; i < MAX_NEIGHBOR_COUNT; i++)
    {
        Node* neighbor = node->neighbors[i];
        if (neighbor != nullptr)
        {
            std::cout << neighbor->value << std::endl;
        }
    }
}

template<typename Func>
void DFS_impl(Node* node, Func func, int version)
{
    if (node->version == version)
    {
        return;
    }

    func(node);

    node->version = version;

    for (size_t i = 0; i < MAX_NEIGHBOR_COUNT; i++)
    {
        Node* neighbor = node->neighbors[i];
        if (neighbor != nullptr)
        {
            DFS_impl(neighbor, func, version);
        }
    }
}

template<typename Func>
void DFS(Node* node, Func func)
{
    DFS_impl(node, func, node->version + 1);
}

void printValuesBFS(Node* node)
{
    std::queue<Node*> nodesToProcess{};
    nodesToProcess.push(node);
    int version = node->version + 1;
    node->version = version;

    while (!nodesToProcess.empty())
    {
        Node* oldestNode = nodesToProcess.front();
        nodesToProcess.pop();

        for (size_t i = 0; i < MAX_NEIGHBOR_COUNT; i++)
        {
            Node* neighbor = oldestNode->neighbors[i];
            if (neighbor != nullptr)
            {
                if (neighbor->version == version)
                {
                    continue;
                }

                neighbor->version = version;
                nodesToProcess.push(neighbor);
            }
        }

        std::cout << oldestNode->value << std::endl;
    }
}


void deleteGraph(Node* rootNode)
{
    std::vector<Node*> allNodes{};
    DFS(rootNode, [&](Node* node) { allNodes.push_back(node); });
    for (auto node : allNodes)
    {
        std::cout << "Deleting node " << node->value << std::endl;
        delete node;
    }
}

void printFunc(Node* node)
{
    std::cout << node->value << ", version " << node->version << std::endl;
}

int main()
{
    Node* rootNode = createGraph();
    printNeighborsValues(rootNode->neighbors[0]);
    DFS(rootNode, printFunc);
    DFS(rootNode, printFunc);
    DFS(rootNode, printFunc);
    printValuesBFS(rootNode);
    deleteGraph(rootNode);
}
