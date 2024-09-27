// Macros work at TEXT level (they do textual substitution 
// as a separate pass before actual compilation).
#define SUM(a, b) ((a) + (b))

// Inline functions work at instruction level
// (the instructions of the function are pasted in place of the function call).
inline int sum(int a, int b)
{
    return a + b;
}

int main()
{
    // Gets LITERALLY replaced with, before the actual compiling starts:
    // int s1 = ((4) + (5)); 
    int s1 = SUM(4, 5);

    // The instructions that would be executed when calling sum
    // will be placed directly in place of the function call.
    // This can be useful for functions that do very little work:
    // using these adds to the size of the executable, but it can speed up
    // the program when the cost of invoking the function 
    // (as in, storing the next instruction address,
    // jumping to the function address, returning from it)
    // is high enough compared to the actual work that the function does.
    int s2 = sum(4, 5);

    return 0;
}
