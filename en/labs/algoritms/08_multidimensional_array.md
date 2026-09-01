# Lab Work 8

This assignment is **not required**.

Topic: **Multidimensional arrays**.


## Introduction

The main idea behind multidimensional arrays is that several indices are used to access them.
There is one additional restriction on indices: for each dimension, the possible values must form a consecutive range
from a minimum to a maximum.
Usually, indices range from 0 to the length of that dimension.

The challenge lies in how elements are laid out in memory.
There are 2 main approaches: Iliffe vectors and linear memory.
Linear memory, in turn, requires choosing the order in which the dimensions (index positions) are arranged in memory.
There is also a Dope Vector optimization method that makes calculating a linear index faster.

For example, in the image below, the indices of element 71 are 3 (array), 1 (row), 2 (column).
Note that indexing in the image starts at 1.

![](https://scaler.com/topics/images/javascript-multidimensional-array.webp)


## Iliffe

The idea here is to store only the last dimension as a contiguous block of memory.
In the example from the image, the elements of each row in each square will be stored contiguously in memory
and accessed by their column numbers.

In other words, there will be one *independent* linear array for each row.
The advantage is that rows can have different lengths.
There will be 9 of them in total.

```
10 | 11 | 12

20 | 21 | 22

... more rows here

70 | 71 | 72

80 | 81 | 82

90 | 91 | 92
```

Each row will have its own starting memory address.
These addresses are stored in an array at the next level -- an array of row addresses indexed by row number.
There will be only 3 such arrays.

```
Address of row (10|11|12) | Address of row (20|21|22) | Address of row (30|31|32) --> x

Address of row (40|41|42) | Address of row (50|51|52) | Address of row (60|61|62) --> y

Address of row (70|71|72) | Address of row (80|81|82) | Address of row (90|91|92) --> z
```

The final array will store the addresses of these arrays of row addresses: `x|y|z`.


### Task

Implement code for such arrays.
Start with 2 dimensions.
Then create a generalized version (for any number of dimensions).

For example, the interface will look like this:

- `Iliffe createIliffe(std::span<size_t> sizes);`. `sizes` contains the size of each dimension
  (number of arrays, number of rows, number of columns)
- `T* getElement(Iliffe* array, std::span<size_t> indices)` returns a pointer to the required element using the specified indices.
  Check that the number of indices matches the number of dimensions specified during creation.

You can use `template` to perform dimension checks at compile time instead of runtime:
- `Iliffe<N> createIliffe(std::array<size_t, N> sizes)`. `N` is specified through `template <size_t N>`.
- `T* getElement(Iliffe<N>* array, std::array<size_t, N> indices)`.


## Linear memory

The idea is that elements are stored in one array rather than in independent arrays.
For two-dimensional arrays, for example:

```
    0   1   2
0 | 0 | 1 | 2 |
1 | 3 | 4 | 5 |
2 | 6 | 7 | 8 |
```

The elements can be laid out in memory like this (by rows, row-major order):

```
0 1 2 3 4 5 6 7 8
```

Or like this (by columns, column-major order):

```
0 3 6 1 4 7 2 5 8
```

For multidimensional arrays, this is generalized as follows:
- row-major means that the rightmost dimension varies fastest in memory (`arr[a][b][c] --> c, b, a`).
- column-major means that the leftmost dimension varies fastest in memory (`arr[a][b][c] --> a, b, c`).

Note that the indexing order does not change; only the arrangement of elements in memory changes.

This order determines how indices change as we iterate through elements in memory.
The examples below show how indices change in row-major and column-major layouts.
```
(0,0) (0,1) (0,2) (1,0) (1,1) (1,2) (2,0) (2,1) (2,2)
  0     1     2     3     4     5     6     7     8

(0,0) (1,0) (2,0) (0,1) (1,1) (2,1) (0,2) (1,2) (2,2)
  0     3     6     1     4     7     2     5     8
```

The same principle applies to multidimensional arrays: when iterating in memory order, index positions vary from right to left or from left to right.

### Finding an index

Let us consider how to derive the required linear index from the indices for each dimension,
using the three-dimensional array from the image above in row-major layout as an example.

The idea is to view all elements as groups of 3 while keeping them arranged linearly in memory.
That is, in memory they go from left to right, top to bottom;
if `arr[a][b][c]` is the indexing syntax,
`a` is the row number (in the example below),
`b` is the index of a group of 3 within that row,
`c` is the index within that group.
```
(10|11|12) | (20|21|22) | (30|31|32)
(40|41|42) | (50|51|52) | (60|61|62)
(70|71|72) | (80|81|82) | (90|91|92)
```

Increasing index `a` by one skips 9 elements (an entire row).
Similarly, adding 1 to `b` advances the linear index by 1 group (3 positions).
Adding 1 to `c` changes the index by 1.

We can look at this slightly differently: each value of index `a` corresponds to 3 values of index `b`.
Each value of index `b` corresponds to 3 values of index `c`.

One approach is to first find the index of the group of 3: multiply the row index `a` by 3
(because there are 3 groups in each row), then add `b`.
Then find the linear index: multiply the number of skipped groups of 3 by 3, then add `c`.

$$
i = 3(3a + b) + c
$$

Another approach is to calculate how many elements each skipped row contains:
3 groups of 3 elements, so 9 in total.
This can also be derived by expanding the parentheses:

$$
i = 9a + 3b + c
$$

The values 9, 3, and 1 for `a`, `b`, and `c`, respectively, indicate how many cells each index "costs", which is why they are called costs.
Each cost is denoted by $` D_j `$, where $` j `$ is the dimension number, counted from right to left because this is row-major.

If $` n_j `$ denotes the length of dimension $` j `$ (the length of its index interval),
the expression for $` D_j `$ can be generalized recursively:

$$
\begin{align}
& D_j = D_{j - 1} * n_{j - 1} \\\\
& D_0 = 1
\end{align}
$$

### Task

Implement this in code:

- `Linear createLinear(std::span<size_t> sizes, Order order);`.
  The total number of elements will equal the product of all `sizes`.
  `order` will be either `RowMajor` or `ColumnMajor` (through `enum class`).
- `T* getElement(Linear* array, std::span<size_t> indices)`.
- `std::span<T> elements(Linear* array)` -- provides access to the linear array of elements.

Likewise, you can implement a generalized version using `N` and `template`.


## Dope Vector

A Dope Vector is used when an array's index range does not start at 0 or does not end at length - 1.
In other words, it applies only to arrays with non-standard index intervals.

For non-standard index intervals, the straightforward approach calculates the memory index
by subtracting the lower bound of the interval, so that the first available index maps to 0 -- the first linear index.
The interval length is the upper bound - lower bound + 1 (because the upper bound is included in the interval).

The lookup can be expressed by the following formula ($` l_j `$ is the lower bound for dimension $` j `$, $` h_j `$ is its upper bound, $` N `$ is the number of dimensions, $` k_j `$ is the value of the requested index in dimension $` j `$, and $` n_j `$ is the length of the index interval for dimension $` j `$):

$$
\begin{align}
& n_j = h_j - l_j + 1 \\\\
& D_0 = 1 \\\\
& D_j = n_{j - 1} * D_{j - 1} \\\\
& i = \\sum_{j=0}^{N - 1} (k_j - l_j) D_j = \\sum_{j=0}^{N - 1} k_j D_j - c \\\\
& c = \\sum_{j=0}^{N - 1} l_j D_j
\end{align}
$$

Thus, by calculating all $` D_j `$ and $` c `$ in advance, the index can be calculated without subtracting the lower bounds, which speeds up linear-index calculation.

A Dope Vector consists of all $` D_j `$ values and the value $` c `$.


### Task

Allow elements to be stored using indices that do not start at zero.
Then add the use of a Dope Vector to the implementation.
Calculate the Dope Vector once during creation.

```cpp
using SignedSize = std::make_signed_t<size_t>;

struct Range
{
    SignedSize from;
    SignedSize toInclusive;
};
```

- `LinearRanged createLinearRanged(std::span<Range> ranges, Order order)` --
  accepts index intervals, calculates their lengths and the Dope Vector itself, and stores the resulting information in a struct field.
- `T* getElement(LinearRanged* array, std::span<SignedSize> indices)`.
