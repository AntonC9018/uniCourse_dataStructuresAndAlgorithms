#include <iostream>
#include "standard_impl.cpp" // see this file

int main()
{
    const std::unique_ptr<Node> root = createGraph();
    const IteratorDFS end{};

    // if (false)
    {
        IteratorDFS it{root.get()};

        while (it != end)
        {
            std::cout << *it << std::endl;
            ++it;
        }
    }

    // Could iterate two graphs in lockstep now.
    // if (false)
    {
        IteratorDFS it1{root.get()};
        IteratorDFS it2{root.get()}; // imagine this was a different graph

        int result = 0;
        while (it1 != end && it2 != end)
        {
            result += *it1 + *it2;
            ++it1;
            ++it2;
        }
    }

    // Can store the state to resume later.
    {
        IteratorDFS it{root.get()};

        // Just skip 3 elements.
        for (int i = 0; i < 3; i++)
            ++it;

        // Copy the state
        IteratorDFS it2{it};

        // Finish executing the first iterator
        while (it != end)
        {
            std::cout << *it << std::endl;
            ++it;
        }

        std::cout << "Iterator 1 finished" << std::endl;

        // Now count the sum with the second iterator
        int result = 0;
        while (it2 != end)
        {
            result += *it2;
            ++it2;
        }

        std::cout << "Iterator 2 computed the sum: " << result << std::endl;
    }

    return 0;
}
