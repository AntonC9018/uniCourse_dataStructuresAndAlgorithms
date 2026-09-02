This is the math kind of vector, not the dynamic array kind of vector.
The STL actually provides a template class for element-wise operations on numeric arrays,
it's called [`std::valarray`](https://en.cppreference.com/w/cpp/numeric/valarray).
It can apply arithmetic to all elements at once (`a + b`, `a * 2` and so on),
but it's not a full-blown mathematical vector class:
a linear algebra API (dot product, norm and the like) is not part of it.