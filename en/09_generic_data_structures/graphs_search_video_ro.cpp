#include <array>
#include <cassert>
#include <iostream>
#include <queue>
#include <unordered_set>

static inline const size_t NEIHBOR_COUNT = 2;

struct Node
{
    int value;
    std::array<Node*, NEIHBOR_COUNT> neighbors;
};

void printNeighborNeighbors(const Node* node)
{
    for (const Node* neighbor : node->neighbors)
    {
        if (neighbor == nullptr)
        {
            break;
        }

        for (const Node* neighborNeighbor : neighbor->neighbors)
        {
            if (neighborNeighbor == nullptr)
            {
                break;
            }
            std::cout << neighborNeighbor->value << std::endl;
        }
    }
}

Node* createGraph()
{
    Node* root = new Node;
    root->value = 1;

    Node* node2 = new Node;
    node2->value = 2;

    Node* node3 = new Node;
    node3->value = 3;

    Node* node4 = new Node;
    node4->value = 4;

    Node* node5 = new Node;
    node5->value = 5;

    Node* node6 = new Node;
    node6->value = 6;

    root->neighbors = { node2, node3 };
    node2->neighbors = { node4, nullptr };
    node3->neighbors = { node5, nullptr };
    node4->neighbors = { node3, node5 };
    node5->neighbors = { node6, root };
    node6->neighbors = {};

    return root;
}

template<typename NodeFunc>
struct VisitationContext
{
    std::unordered_set<int> visited;
    NodeFunc func;
};

template<typename NodeFunc>
bool DFS_impl(Node* node, VisitationContext<NodeFunc>* context)
{
    auto result = context->visited.emplace(node->value);
    if (!result.second)
    {
        return false;
    }

    if (context->func(node))
    {
        return true;
    }
    
    for (Node* neighbor : node->neighbors)
    {
        if (neighbor == nullptr)
        {
            break;
        }
        if (DFS_impl(neighbor, context))
        {
            return true;
        }
    }
    return false;
}

template<typename NodeFunc>
bool DFS(Node* node, NodeFunc nodeFunc)
{
    VisitationContext<NodeFunc> context{ {}, nodeFunc };
    // context.visited.reserve(6);
    return DFS_impl(node, &context);
}

bool printNodeValue(Node* node)
{
    std::cout << node->value << std::endl;
    return false;
}

bool calculateSum(int* sum, Node* node)
{
    *sum = *sum + node->value;
    return false;
}

bool findNodeWithValue5(Node** foundNode, Node* node)
{
    if (node->value == 5)
    {
        *foundNode = node;
        return true;
    }
    return false;
}

template<typename NodeFunc>
bool BFS_impl(Node* root, VisitationContext<NodeFunc>* context)
{
    std::queue<Node*> q{};
    q.push(root);
    context->visited.emplace(root->value);

    while (true)
    {
        if (q.empty())
        {
            return false;
        }
        Node* currentNode = q.front();
        q.pop();

        if (context->func(currentNode))
        {
            return true;
        }

        for (Node* neighborNode : currentNode->neighbors)
        {
            if (neighborNode == nullptr)
            {
                break;
            }

            auto t = context->visited.emplace(neighborNode->value);
            if (t.second)
            {
                q.push(neighborNode);
            }
        }
    }
}

template<typename NodeFunc>
bool BFS(Node* root, NodeFunc nodeFunc)
{
    VisitationContext<NodeFunc> context{ {}, nodeFunc };
    return BFS_impl(root, &context);
}


enum class SearchAlgorithm
{
    BFS = 0,
    DFS = 1,
};

template<typename NodeFunc>
bool doSearchAlgo(Node* root, NodeFunc nodeFunc, SearchAlgorithm algo)
{
    switch (algo)
    {
        case SearchAlgorithm::BFS:
        {
            return BFS(root, nodeFunc);
        }
        case SearchAlgorithm::DFS:
        {
            return DFS(root, nodeFunc);
        }
        default:
        {
            assert(false);
            return false;
        }
    };
}

SearchAlgorithm selectAlgoWithValidation()
{
    while (true)
    {
        int algorithm;
        std::cout << "0 -- BFS\n1 -- DFS" << std::endl;

        std::cin >> algorithm;
        if (algorithm < static_cast<int>(SearchAlgorithm::BFS) 
            || algorithm > static_cast<int>(SearchAlgorithm::DFS))
        {
            std::cout << "Please enter a valid algorithm\n";
            continue;
        }

        return static_cast<SearchAlgorithm>(algorithm);
    }
}

int main()
{
    Node* graphRoot = createGraph();

    // printNeighborNeighbors(graphRoot->neighbors[1]);
    // DFS(graphRoot, printNodeValue);

    // {
    //     int sum = 0;
    //     DFS(graphRoot, [&](Node* node) { return calculateSum(&sum, node); });
    //     std::cout << sum << std::endl;
    // }

    {
        SearchAlgorithm selectedAlgo = selectAlgoWithValidation();

        Node* foundNode;
        bool nodeWasFound = doSearchAlgo(graphRoot, [&](Node* node)
        {
            std::cout << "Visiting node " << node->value << std::endl;
            return findNodeWithValue5(&foundNode, node);
        }, selectedAlgo);

        if (nodeWasFound)
        {
            for (Node* neighbor : foundNode->neighbors)
            {
                if (neighbor == nullptr)
                {
                    break;
                }
                std::cout << "Node neighbor is " << neighbor->value << std::endl;
            }
        }
    }

    // BFS(graphRoot, printNodeValue);

    return 0;
}
