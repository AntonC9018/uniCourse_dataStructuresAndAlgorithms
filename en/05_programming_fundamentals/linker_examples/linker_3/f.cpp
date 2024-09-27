// This function appears literally nowhere in the compiled executable. 
// It doesn't participate in linking, which means you can put them in header files.
// It's better to also make them static to avoid confusing the linker.
static inline int sum()
{
    return 1;
}
