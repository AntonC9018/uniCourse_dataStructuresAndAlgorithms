#include <vector>
#include <memory>

struct Node
{
    int value; 
    std::vector<Node*> children;

    // NOTE: This leaks the nodes
};

static std::unique_ptr<Node> createGraph()
{
    std::unique_ptr<Node> root{new Node{1}};

    Node* a = new Node{2};
    Node* b = new Node{3};
    Node* c = new Node{4};
    Node* d = new Node{5};
    Node* e = new Node{6};
    Node* f = new Node{7};

    root->children.push_back(a);
    root->children.push_back(b);
    root->children.push_back(c);

    a->children.push_back(e);
    a->children.push_back(d);

    e->children.push_back(f);

    return root;
}
