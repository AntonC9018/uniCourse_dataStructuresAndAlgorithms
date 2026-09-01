# Lab Assignment 2

Topic: **Search Algorithms**.

Lab objectives:
- Implement search methods for unsorted arrays (linear search, binary search tree)
- Implement search methods for sorted arrays (binary search and one other method of your choice)
- Record algorithm execution time as a function of array size and element arrangement
  (sorted order, reverse-sorted order, random order).

## System for measuring algorithm execution time

Since you will later need to analyze algorithm performance in practice
in different situations, you need to create a system that will allow you to take these measurements.

There are many possible approaches; the most basic one (without using polymorphism) would probably
involve using several nested loops and a switch statement.
An approximate outline:

```cpp
std::array<std::vector<int>, DATA_COUNT> allData;
std::array<std::string_view, DATA_COUNT> fileNames =
{
    { "small.data" },
    { "medium.data" },
    { "large.data" },
};

bool hasErrors = false;
for (int di; di < DATA_COUNT; di++)
{
    std::string_view fileName = fileNames[di];
    std::ifstream file{fileName};
    bool success = readDataFromFile(file, allData[di]);
    if (!success)
    {
        // You might return more context here,
        // depends on the implementation of the csv parser.
        std::cout << "Could not parse file " << fileName;
        hasErrors = true;
    }
}

if (hasErrors)
{
    return 1;
}

std::vector<int> items;
for (int ai = 0; ai < ALGORITHM_COUNT; ai++)
{
    for (int di; di < DATA_COUNT; di++)
    {
        std::span<int> sortedData = allData[di];
        items.resize(sortedData.size());

        for (int si = 0; si < SHUFFLE_COUNT; si++)
        {
            time_t totalTime = 0;
            for (int ei = 0; ei < EXPERIMENT_COUNT; ei++)
            {
                switch (si)
                {
                    // Sorted array
                    case 0:
                    {
                        // Copy from sortedData into items
                        break;
                    }

                    // Unsorted array
                    case 1:
                    {
                        // Copy from sortedData in some random order
                        break;
                    }

                    // Unsorted
                    case 2:
                    {
                        // Copy in reverse order
                        break;
                    }
                }

                time_t experimentStartTime = ...;

                switch (ai)
                {
                    // Linear search
                    case 0:
                    {
                        // ...
                        break;
                    }

                    // Binary search tree
                    case 1:
                    {
                        // ...
                        break;
                    }
                }

                time_t experimentEndTime = ...;
                totalTime += experimentEndTime - experimentStartTime;
            }

            // Store the time for this type of shuffle
            // ...
        }

        // Store the times for each shuffle for this data size
    }

    {
        // Print the total times for this algorithm
        std::array<std::string_view, ALGORITHM_COUNT> algorithmNames =
        {
            { "Linear" },
            { "Binary Search Tree" },
        };
        std::string_view algorithmName = algorithmNames[ai];

        std::cout << "Average time for the algorithm " << algorithmName << ": ";
        // ...
    }
}
```

However, while programming, you will probably notice
that it is difficult to separate out the common timing code.
This is better handled using polymorphism (pass the algorithm function as a parameter).
Read about polymorphism [here](../../../en/05a_programming_fundamentals/11_polymorphism.md),
and make sure you have a basic understanding of [templates](../../../en/05a_programming_fundamentals/07_template.md)
and function pointers.


## Implementing the algorithms

Write code for the following algorithms:
- Linear search
- Binary search tree
- Binary search
- One search algorithm of your choice for sorted arrays

Test the algorithms on arrays of different sizes and with different element arrangements (where applicable):
- Sorted array (ascending)
- Reverse-sorted array (descending)
- Random element order

Run the tests several times (5+) and average the results.

You may run all tests in one program, run each test in a separate program,
or use command-line arguments to select the test
(look up how to do this if you decide to take this approach).

For timing, use the `std::chrono` or `ctime` libraries.
Alternatively, you may use the console commands
`Measure-Command` in PowerShell (Windows) or `time` in bash (Linux/Mac/WSL).

Analyze the results obtained:
- Compare how execution time depends on the number
  and arrangement of elements for each algorithm.
- Compare the practical complexity of each algorithm
  (how execution time depends on the number of elements) with its theoretical complexity.
- Explain in which situations each algorithm should be used,
  and why it is more suitable than the others for those tasks.
