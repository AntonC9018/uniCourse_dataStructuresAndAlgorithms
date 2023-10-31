#include "f.h"

template<typename T>
T f(T value)
{
    return value;
}

// Explicit template instantiation.
// Without this line, the linker won't be able to find a definition,
// because none would exist in any of the compilation units.
// You have to do this for each type that you're going to use in the other files.
template int f<int>(int value);