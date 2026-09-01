# C++ arrays (`std::array`)

- [Information](../../../en/06_arrays/doc.md)

## Concepts

- The advantage of C++ arrays over C arrays
- Copying and initializing arrays
- Indexing C++ arrays
- `data`
- Obtaining references to array elements
- Obtaining addresses of array elements
- Data types other than `int` for array elements

## Examples

### 1. C++ arrays
```cpp
std::array<int, 2> arr{ 1, 2 };
int* pa = a.data();
int& b = *pa;
pa += 1;
std::cout << b << std::endl;
```
<details>
<summary>

What is `data`?</summary>

`a.data()` returns the address of the first element in the array
(`&a[0]`; `a[0]` yields a reference, whose address is then taken).
</details>

<details>
<summary>Answer</summary>

`b` will continue to refer to the first element, even though the pointer has been updated.
</details>


### 2. Initializing C++ arrays (1)
```cpp
std::array<int, 2> arr{ 1, 2 };
std::array<int, 2> other{ 3, 4 };
arr = other;
```

<details>
<summary>Answer</summary>

Here, each element is copied from `other` into `arr`.
</details>

### 3. Initializing C++ arrays (2)
```cpp
std::array<int, 2> arr{ 1, 2 };
std::array<int, 2> other{ arr };
```

<details>
<summary>Answer</summary>

The same copying occurs here, when `other` is created.
</details>

### 4. Reference to an array
```cpp
std::array<int, 2> arr{ 1, 2 };
std::array<int, 2>& other{ arr };
other[0] = 3;
std::cout << arr[0] << std::endl;
```

<details>
<summary>Answer</summary>

This illustrates creating a reference to an object of C++ array type.
You can think of `other` as another name for `arr`.
</details>

### 5. Address of an array
```cpp
std::array<int, 2> arr{ 1, 2 };
std::array<int, 2>* p{ &arr };
*p = { 3, 4 };
std::cout << arr[0] << std::endl;
std::cout << arr[1] << std::endl;
```

<details>
<summary>Answer</summary>

`p` will contain the address of the beginning of the entire array object.
The array object covers all of its elements.

Here, the original elements are overwritten with `3, 4`.
</details>

### 6. Dereferencing an array address
```cpp
std::array<int, 2> arr{ 1, 2 };
std::array<int, 2>* p{ &arr };
std::array<int, 2> arr1{ *p };
arr1[0] = 3;
arr1[1] = 4;
std::cout << arr[0] << std::endl;
std::cout << arr[1] << std::endl;
```

<details>
<summary>Answer</summary>

`p` points to an object of type `std::array<int, 2>`, and the expression `*p` gives a value
of type `std::array<int, 2>`, so `arr1` receives a copy of the entire array.

Since `arr1` is a copy, its changes will not affect `arr`.
</details>


### 7. Reference to an array element
```cpp
std::array<int, 2> arr{ 1, 2 };
int& a = arr[0];
a = 3;
```

<details>
<summary>Answer</summary>

`a = 3` overwrites the first element of the array
because `a` refers to element 1 (an object inside the array).
</details>

### 8. Indexing elements through an address
```cpp
std::array<int, 2> arr{ 1, 2 };
std::array<int, 2>* p{ &arr };
(*p)[0] = 3;
(*p)[1] = 4;
std::cout << arr[0] << std::endl;
std::cout << arr[1] << std::endl;
```

<details>
<summary>Answer</summary>

Here, `*p` is an expression of type `std::array<int, 2>&`, meaning it gives a reference to the array—that is,
to the memory occupied by the `arr` variable (because `p` contains the address of `arr`).

Indexing `(*p)` gives *references to elements in the array*.
For example, the type of the expression `(*p)[0]` is `int&`, and it refers 
to the first element of the `arr` array.

Assignments through these references update the elements of `arr`.
</details>

### 9. Address of an element through `data`
```cpp
std::array<int, 2> arr { 1, 2 };
int& arr1 = *(p.data() + 1)
```

<details>
<summary>Answer</summary>

This is similar to the code above, but the expression is more complex.
Here, `arr1` becomes a reference to `arr[1]`.
</details>


### 10. Relative locations of the base address and the array object itself
```cpp
std::array<int, 2> arr { 1, 2 };
ptrdiff_t diff { reinterpret_cast<uint8_t*>(arr.data()) - reinterpret_cast<uint8_t*>(&arr) };
std::cout << diff << std::endl;
```

<details>
<summary>Answer</summary>

The beginning of the entire array object is at the same address as its first element.
**A `std::array` is its elements**.

It prints 0.
</details>

### 11. Matrices (two-dimensional arrays)
```cpp
std::array<std::array<int, 2>, 3> arr{ 
    std::array{ 1, 2 },
    { 3, 4 },
    { 5, 6 },
};
std::array<int, 2> firstRow { arr[0] };
std::array<int, 2> lastRow { arr[2] };
arr[0][0] = 7;
arr[2][1] = 8;
arr[1] = { 9, 10 };
```

<details>
<summary>Answer</summary>

This illustrates an array whose element type is another array rather than `int`.
Each array element therefore effectively stores two ints.

> In the initialization of `arr`, you need to specify `std::array`
> because otherwise the compiler cannot determine the element type from the initialization.
> It needs a little help.
>
> You do not need to understand this mechanism yet.
</details>

<details>
<summary>Can a user-defined type be used as an array element?</summary>

Yes. Try defining a type, for example:
```cpp
struct Item
{
    int f1;
    int f2;
};
```

And use it as the element type, like this:
```cpp
std::array<Item, 3> arr{
    Item{ 1, 2 },
    { 3, 4 },
    { 5, 6 },
};
```
</details>
