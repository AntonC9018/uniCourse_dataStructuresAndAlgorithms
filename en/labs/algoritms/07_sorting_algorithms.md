# Laboratory Work 7

Topic: **Sorting algorithms.**

## Algorithm Implementation

Implement 4 sorting algorithms:
- 2 with a time complexity of $` O(N^2) `$ (Bubble, Insertion, Selection, Shell).
- 2 with a time complexity of $` O(N log(N)) `$ (Heap, Merge, Quick).
- You may also implement Radix Sort, which has some unique characteristics.

Each algorithm must be implemented as a function that takes `std::span<T>` as a parameter,
as well as any other context required for
sorting (for example, an element comparison function).
The function must return either `void` when sorting is performed in-place,
or a sorted copy of the array when sorting is not performed in-place (merge sort),
in which case the memory of the input `std::span` must not be modified.
You may put the parameters into a single context structure if you consider it necessary.

## Collecting Data for Analysis

As in Lab 2, test the algorithms with:
- Different array sizes (large arrays have 1000+ elements);
- Different initial arrangements of elements in the array.

Record the following for each algorithm run:
- Execution time;
- Number of comparisons between elements;
- Number of swaps or copies performed;
- Other data you consider necessary.

Calculate the total and average execution times of the algorithms.

## Analysis of the Collected Data

Analyze the collected data:
- Compare how execution time and other metrics vary with the algorithm,
  array size, and element arrangement.
- Determine the practical time complexity of the algorithms
  (how execution time increases as array size grows) and their memory complexity.
- Determine the theoretical time and memory complexities of the implemented algorithms,
  based on the algorithm descriptions or the code you wrote.
- Explain the advantages and disadvantages of the algorithms with $` O(N log(N)) `$ time complexity compared with one another.
  How does each approach affect best- and worst-case execution times? Do these times depend on the arrangement of elements?
