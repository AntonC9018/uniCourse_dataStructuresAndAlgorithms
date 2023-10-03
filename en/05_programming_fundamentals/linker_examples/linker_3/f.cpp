// This function appears literally nowhere in the compiled executable. 
// It doesn't participate in linking, which means you can put them in header files.
inline int sum()
{
    return 1;
}