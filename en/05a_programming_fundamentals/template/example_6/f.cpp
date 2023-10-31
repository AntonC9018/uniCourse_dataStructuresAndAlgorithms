#include "f.h"

template<typename T>
T Test<T>::getValue()
{
    return this->value;
}

// Constructors work just like regular methods in this regard.
template<typename T>
Test<T>::Test(T value)
{
    this->value = value;
}

// Won't link without this line.
template class Test<int>;