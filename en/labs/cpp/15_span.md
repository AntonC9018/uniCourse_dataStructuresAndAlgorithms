# `std::span`

- [Video](https://www.youtube.com/watch?v=3aXFuiHxb9k&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=19)

## Examples to aid understanding

### 1. Pointer indexing
```cpp
std::array<int, 3> arr{ 0, 1, 2 };
int* arrStart{ arr.data() };
*arrStart = 3;
*(arrStart + 0) = 4;
arrStart[0] = 5;
*(arrStart + 1) = 6;
arrStart[1] = 7;
*(arrStart + 2) = 8;
arrStart[2] = 9;

int item0{ *arrStart };
item0 = arrStart[0];
int item1{ *(arrStart + 1) };
item1 = arrStart[1];
```

<details>
<summary>Answer:</summary>

`arrStart` is assigned the address of the first element in the array using `.data()`.

Then `*arrStart` refers to the first element in the array at that address.
`*arrStart` is equivalent to `*(arrStart + 0)`.

The expression `*(x + 1)` is equivalent to `x[1]`.
Accordingly, `*(arrStart + 0)` can be written using indexing as `arrStart[0]`.

> `x[1]` is also equivalent to `1[x]`

`*(arrStart + 1)` is equivalent to `arrStart[1]`, which is equivalent to `arr[1]`.
Starting at the first element (`arrStart`), `+ 1` moves to the next memory location.

These expressions can be used both to write values
and to read them.
</details>
### 2. Passing an array as a pointer
```cpp
#include <iostream>
#include <array>

void func(int* arr)
{
   std::cout << arr[0] << std::endl;
   std::cout << arr[1] << std::endl;
}

int main()
{
   std::array<int, 2> arr{ 1, 2 };
   func(arr.data());
}
```

<details>
<summary>Answer:</summary>

Here, the function receives the address of the first element of the array.

`arr[0]` is equivalent to `*(arr + 0)`
and reads the first element of the `arr` array in the `main` function.

Accordingly, `arr[1]` is equivalent to `*(arr + 1)` and prints the second element.

It prints `1` and `2`.
</details>

### 3. Special syntax for passing an array
```cpp
#include <iostream>
#include <array>

void func(int arr[])
{
   std::cout << arr[0] << std::endl;
   std::cout << arr[1] << std::endl;
}

int main()
{
   std::array<int, 2> arr{ 1, 2 };
   func(arr.data());
}
```

<details>
<summary>Answer:</summary>

`int* arr` is equivalent to `int arr[]` when used as a parameter.
This example is equivalent to the previous one.
</details>

### 4. Reading beyond an array
```cpp
#include <iostream>
#include <array>

void func(int arr[])
{
   std::cout << arr[0] << std::endl;
   std::cout << arr[1] << std::endl;
   std::cout << arr[2] << std::endl;
}

int main()
{
   std::array<int, 2> arr{ 1, 2 };
   func(arr.data());
}
```

<details>
<summary>Answer:</summary>

`arr[2]` in the statement `std::cout << arr[2] << std::endl` attempts to read index `2` from the array.
In C++, attempting to access a nonexistent index is undefined behavior (UB).
This code will compile and may appear to run normally,
but reading `arr[2]` can have any result at runtime.

This is considered a logical error in the code.
</details>

<details>
<summary>How can this error be prevented?</summary>

Before reading an element, you need to check that its index is within the array bounds.
To perform this check, in addition to a pointer to the beginning of the array,
you also need the array length.
In this example, the array length is known (`2`), but in the general case, it must also be passed.
This is covered in the following examples.
</details>

### 5. Calling the same function for different arrays
```cpp
#include <iostream>
#include <array>

void func(int arr[])
{
   std::cout << arr[0] << std::endl;
   std::cout << arr[1] << std::endl;
   std::cout << arr[2] << std::endl;
}

int main()
{
   std::array<int, 3> arr1{ 0, 1, 2 };
   std::array<int, 2> arr2{ 0, 1 };
   func(arr1.data());
   func(arr2.data());
}
```

<details>
<summary>Answer:</summary>

There is no UB for the first array,
because all indices from 0 to 2 are valid.

However, the situation from the example above repeats for the second array.

This illustrates that the same function can be used
for arrays of different lengths while being unable to know their lengths in advance.
</details>

### 6. Printing with a loop
```cpp
#include <iostream>
#include <array>

void print(int* arr)
{
   for (size_t i = 0; i < 2; i++)
   {
       std::cout << arr[i] << std::endl;
   }
}

int main()
{
   std::array<int, 2> arr{ 0, 1 };
   print(arr.data());
}
```

<details>
<summary>Answer:</summary>

This illustrates how all elements of an array can be printed to the console using a loop.

`2` in the loop condition refers to the array length.
</details>

<details>
<summary>How can you avoid duplicating the array length?</summary>

There are several options:
- Pass a static array or a reference to it as a parameter;
- Pass the length as a separate parameter;
- Create a global constant for the length, but then the function will be limited to that length only;
- Pass a `span` (a pointer to the first element and the length in one parameter).

These approaches are described in the following examples.
</details>

<details>
<summary>What happens if the lengths do not match?</summary>

If the loop uses a length different from the array length:
```cpp
for (size_t i = 0; i < 3; i++)
```
the program will read an element beyond the array bounds, resulting in UB.

If the array has a greater length:
```cpp
std::array<int, 3> arr{ 0, 1, 2 };
```
the entire array will not be printed.

If the array has a smaller length:
```cpp
std::array<int, 1> arr{ 0 };
```
the `print` loop again causes UB.
</details>

### 7. Array length constant

What is the advantage of this approach compared to the previous one?

```cpp
#include <iostream>
#include <array>

constexpr size_t ARRAY_LENGTH = 2;

void print(int* arr)
{
   for (size_t i = 0; i < ARRAY_LENGTH; i++)
   {
       std::cout << arr[i] << std::endl;
   }
}

int main()
{
   std::array<int, ARRAY_LENGTH> arr{ 0, 1 };
   print(arr.data());
}
```

<details>
<summary>What is <code>constexpr</code>?</summary>

`constexpr` (short for constant expression) declares a constant (an immutable named value)
whose value is known at compile time.
The compiler effectively replaces it with its value everywhere it is mentioned.

We need a compile-time constant
because `ARRAY_LENGTH` in `std::array<int, ARRAY_LENGTH>` is part of the type,
and C++ type sizes are always known at compile time.

For example, the following will not compile:
```cpp
#include <array>

int main()
{
   size_t len = 2;
   std::array<int, len> arr{ 1, 2 };
}
```

But the following will:
```cpp
#include <array>

int main()
{
   constexpr size_t len = 2;
   std::array<int, len> arr{ 1, 2 };
}
```

`constexpr` in this example can be replaced with `static inline const`
(this will be covered in more detail in the topic on linking) to achieve the same behavior
(`const` `int`s in C++ are also compile-time constants).
</details>

<details>
<summary>Answer</summary>

The advantage is that it is now harder to pass an array of the wrong length,
although it is still possible.
For example:
```cpp
std::array<int, 3> arr{};
print(arr.data());
```

This happens because there is no check of *where the pointer came from* when calling the function.
</details>

### 8. How can you get the length of a C array? What about `std::array`?

<details>
<summary>A C array? What do you mean?</summary>

This is the definition of a C array:
```cpp
int arr[2]{};
```

Here is a C++ `std::array`:
```cpp
std::array<int, 2> arr{};
```

If you initialize the elements, you do not need to write `int` and `2`; the compiler will infer them:
```cpp
std::array arr{1, 2};
```
</details>

<details>
<summary>Hint 1</summary>

A C array has no `.size()` method like `std::array` does.
</details>

<details>
<summary>Hint 2</summary>

You can work around this by using `sizeof`.
</details>

<details>
<summary>Hint 3</summary>

`sizeof` for the whole array gives its size in bytes.
</details>

<details>
<summary>Hint 4</summary>

`sizeof` applied to an expression for one of the elements or to the base type gives the size of one element.
This can be combined with the previous hint.
</details>

<details>
<summary>Answer</summary>

Divide the number of bytes occupied by the array by
the number of bytes occupied by one element to get the number of elements.

> For example, there is an array of 3 elements: `int arr[3]{}`.
> In total, it occupies 12 bytes (3 times 4 bytes for each element).
> Each element occupies 4 bytes.
>
> If the goal is to get the array length (3), given the total size in bytes (12),
> you need to calculate how many groups, each the size of 1 element (4 bytes), fit into the total size (12).
> For this, division is used (12 / 4 = 3).

If `arr` has already been defined:
```cpp
int arr[3]{};
```

This can be calculated as follows:
```cpp
constexpr size_t len{ sizeof(arr) / sizeof(int) };
```

Or like this, which is more flexible:
```cpp
constexpr size_t len{ sizeof(arr) / sizeof(arr[0]) };
```

`sizeof(arr[0])` yields a constant because `sizeof` considers only the *type of the expression* —
the `arr[0]` operation will not actually be evaluated — the compiler looks at the type the expression *would* have.
</details>

### 9. Passing an array using a pointer and a length parameter

What are the advantages and disadvantages of this approach?
```cpp
#include <array>
#include <iostream>

void print(int* arr, size_t length)
{
    for (size_t i = 0; i < length; i++)
    {
         std::cout << arr[i] << std::endl;
    }
}

int main()
{
    std::array<int, 2> arr{ 0, 1 };
    print(arr.data(), arr.size());

    int arr1[3]{};
    print(arr1, sizeof(arr1) / sizeof(arr1[0]));
}
```

<details>
<summary>Answer</summary>

The advantage is that the function will now work for arrays of different lengths.

Another advantage is that it is even harder to make a mistake when passing the length —
you simply need to pass the length of the array you are passing.

The main drawback is that the length still has to be passed correctly,
and a mistake can still be made at this point.
For example:
```cpp
std::array<int, 2> arr{};
print(arr.data(), 3);
```
</details>


### 10. (advanced level) Reference to a C array
```cpp
#include <iostream>

int main()
{
   int arr[3]{};
   int (&arrRef)[3]{ arr };
   arrRef[0] = 1;
   std::cout << arr[0] << std::endl;
}
```

### 11. (advanced level) Passing a reference to a C array
```cpp
#include <iostream>

void print(int (&arr)[3])
{
    for (size_t i = 0; i < 3; i++)
    {
         std::cout << arr[i] << std::endl;
    }
}

int main()
{
    int arr1[3]{};
    print(arr1);
}
```

### 12. (advanced level) Array length template
```cpp
#include <iostream>

template<size_t len>
void print(int (&arr)[len])
{
    for (size_t i = 0; i < len; i++)
    {
         std::cout << arr[i] << std::endl;
    }
}

int main()
{
    int arr1[3]{};
    print(arr1);
}
```

<details>
<summary>What is a <code>template</code>?</summary>

The compiler will create a separate `print` function for each array length,
substituting the appropriate value for `len`.

For example, here `print` will be instantiated with `3` substituted for `len`, which can also be written
like this:
```cpp
print<3>(arr1);
```

</details>

<details>
<summary>Answer</summary>

References to arrays can be passed to templates in this way.
</details>

### 13. Changing elements of a C++ array passed as a parameter (1)
```cpp
#include <array>
#include <iostream>

void change(std::array<int, 3> arr)
{
    arr[0] = 1;
}

int main()
{
    std::array<int, 3> arr{};
    change(arr);
    std::cout << arr[0] << std::endl;
}
```

<details>
<summary>Answer</summary>

`arr` will not change because a copy of the array was passed to the function.
</details>

### 14. Changing elements of a C++ array passed as a parameter (2)
```cpp
#include <array>
#include <iostream>

void change(std::array<int, 3>& arr)
{
    arr[0] = 1;
}

int main()
{
    std::array<int, 3> arr{};
    change(arr);
    std::cout << arr[0] << std::endl;
}
```

<details>
<summary>Answer</summary>

`1` will be written to `arr[0]` because a *reference* to the array object in `main` was passed to the function.
</details>

### 15. Passing a C++ array by reference
```cpp
#include <array>
#include <iostream>

void print(std::array<int, 3>& arr)
{
   for (size_t i = 0; i < arr.size(); i++)
   {
       std::cout << arr[i] << std::endl;
   }
}

int main()
{
    std::array<int, 3> arr{};
    print(arr);
}
```

<details>
<summary>Answer</summary>

Here, the array was passed to the function by reference.
It is now impossible to pass an array of the wrong length!
For example, the following will not compile:
```cpp
std::array<int, 2> arr{};
print(arr);
```

The drawback of this approach is that the function supports only arrays of length 3.
</details>

### 16. (advanced level) C++ array length template
```cpp
#include <array>
#include <iostream>

template<size_t len>
void print(std::array<int, len>& arr)
{
   for (size_t i = 0; i < arr.size(); i++)
   {
       std::cout << arr[i] << std::endl;
   }
}

int main()
{
    std::array<int, 3> arr{};
    print(arr);

    std::array<int, 2> arr1{};
    print(arr1);
}
```

<details>
<summary>Answer</summary>

This approach makes it possible to create one function for each array length.
The function now supports arrays of any length!

There are now 2 drawbacks:
- The function supports only C++ arrays with a *statically* known length
 (the length is part of the type and is known at compile time);
- One new function will be created for each length, which
 will consume extra memory in the form of instructions in the compiled program
 (more on this in its own topic).

These drawbacks can be solved by passing the length as a value parameter,
rather than as part of the type.
</details>

### 17. `std::span`
```cpp
#include <span>
#include <iostream>
#include <array>

int main()
{
   std::array<int, 6> arr{0, 1, 2, 3, 4, 5};
   std::span<int> span{ arr };

   std::cout << "Item 1: " << span[1] << std::endl;
   std::cout << "Item 4: " << span[4] << std::endl;
   std::cout << "arr size in bytes: " << sizeof(arr) << std::endl;
   std::cout << "span size in bytes: " << sizeof(span) << std::endl;
   std::cout << "span length: " << span.size() << std::endl;
}
```

<details>
<summary><code>span</code></summary>

`span` combines a pointer to the first element with the length in one object.
</details>

<details>
<summary>Answer (indexing):</summary>

`span` indexing accesses the array's underlying memory.

It will print `1` and `4` from `arr`.
</details>

<details>
<summary>Answer (<code>sizeof</code>):</summary>

`arr` consists of 6 `int`s, each of which occupies 4 bytes.
In total, 6 × 4 = 24 bytes.

Although `span` refers to `arr`, it does so through a pointer.
`span` consists of one `int*` pointer to the beginning of the array and one `size_t` containing the array length.

In total, `sizeof(int*)` + `sizeof(size_t)` = 8 + 8 = 16.
</details>

<details>
<summary>Answer (<code>span.size()</code>):</summary>

`span.size()` accesses the length stored in `span` and returns `6`.
</details>

### 18. `std::span` from a C++ array
```cpp
#include <span>
#include <iostream>
#include <array>

int main()
{
   std::array<int, 2> arr{1, 2};
   std::span<int> span{ arr };
   arr[0] = 3;
   arr[1] = 4;

   std::cout << span[0] << std::endl;
   std::cout << span[1] << std::endl;
}
```

<details>
<summary>Answer:</summary>

Since `span` stores the *address of the beginning of the array*, rather than a copy of the array,
it always reflects the array's current values.

It prints `3` and `4`.
</details>

### 19. The `at` method
```cpp
#include <iostream>
#include <array>

int main()
{
   std::array<int, 2> arr{1, 2};
   std::cout << arr[0] << std::endl;
   std::cout << arr.at(0) << std::endl;
   std::cout << arr[2] << std::endl;
   std::cout << arr.at(2) << std::endl;
}
```

<details>
<summary>What does <code>arr.at</code> do?</summary>

`at` provides access to an element just like indexing (`arr[...]`),
but also checks the bounds.
If the specified index is beyond the array bounds, the program will crash.

> In fact, an exception will be thrown, which can be caught, but we have not covered that.
</details>

<details>
<summary>Answer</summary>

`arr[0]` reads the value of the first element from the array as usual.

`arr.at(0)` does the same after a successful bounds check.
The bounds check succeeds because index `0` is valid:
the array length is greater than `0`.

`arr[2]` is UB (discussed earlier).

`arr.at(2)` will crash the program during the bounds check.
The bounds check fails because the array has no index `2`:
its length is not greater than `2`.

> This length check is properly called a "bounds check".

> `at` is available for `std::span` starting with the `C++ 26` standard.
</details>

### 20. Passing `std::span` as a parameter
```cpp
#include <iostream>
#include <array>
#include <span>

void print(std::span<int> s)
{
   for (size_t i = 0; i < s.size(); i++)
   {
       std::cout << s[i] << std::endl;
   }
}

int main()
{
   std::array<int, 3> arr{ 1, 2, 3 };
   std::span<int> span{ arr };
   print(span);

   print({ arr });
   print(arr);
}
```

<details>
<summary>Answer</summary>

All 3 forms, `print(span)`, `print({ arr })`, and `print(arr)`, will work and do the same thing.

`print(span)` passes a copy of the already created `span`.

`print({ arr })` and `print(arr)` each initialize a temporary
`std::span<int>` and pass it to the `print` function.

In each case, `print` will loop over the elements of `arr` from `main` and print them.
</details>

### 21. Creating a subspan manually
```cpp
#include <iostream>
#include <array>
#include <span>

void print(std::span<int> s)
{
   for (size_t i = 0; i < s.size(); i++)
   {
       std::cout << s[i] << std::endl;
   }
}

int main()
{
   std::array<int, 4> arr{1, 2, 3, 4};
   std::span<int> wholeSpan{ arr };
   std::span<int> span123{ arr.data(), 3 };
   std::span<int> span234{ arr.data() + 1, 3 };

   print(wholeSpan);

   std::cout << std::endl;
   print(span123);

   std::cout << std::endl;
   print(span234);
}
```

<details>
<summary>Answer</summary>

`std::span` can be created either from an entire array or from a separate *pointer* and *length*.

For example, `std::span<int> span123{ arr.data(), 3 };` initializes the span with:
- The address of the beginning of the array (`arr.data()`) as the pointer,
- `3` as the length.

`std::span<int> span234{ arr.data() + 1, 3 };` initializes the span with:
- The address of the second element of the array (`arr.data() + 1` = `&arr[1]`) as the pointer,
- `3` as the length.

When `span123` is printed, the first 3 elements will be printed.

When `span234` is printed, 3 elements starting from the second one will be printed (2, 3, and 4).
</details>

### 22. Understanding the `data` method

What happens if you change
```cpp
std::span<int> span123{ arr.data(), 3 };
std::span<int> span234{ arr.data() + 1, 3 };
```
to
```cpp
std::span<int> span123{ wholeSpan.data(), 3 };
std::span<int> span234{ span123.data() + 1, 3 };
```
in the previous example?

<details>
<summary>Answer:</summary>

The `data` method of `std::span` returns its stored pointer.

The result will be the same, because both `wholeSpan` and `span123`
store pointers to the first element of `arr`.
</details>

### 23. A subspan with the `subspan` method
```cpp
#include <iostream>
#include <array>
#include <span>

void print(std::span<int> s)
{
   for (size_t i = 0; i < s.size(); i++)
   {
       std::cout << s[i] << std::endl;
   }
}

int main()
{
   std::array<int, 4> arr{1, 2, 3, 4};
   std::span<int> wholeSpan{ arr };
   std::span<int> span123{ wholeSpan.subspan(0, 3) };
   std::span<int> span234{ wholeSpan.subspan(1, 3) };

   print(wholeSpan);

   std::cout << std::endl;
   print(span123);

   std::cout << std::endl;
   print(span234);
}
```

<details>
<summary>Answer</summary>

`subspan` takes 2 arguments:
- The starting index;
- The desired length.

`wholeSpan.subspan(0, 3)` means start at index `0`, with a length of `3`.
This is equivalent to `wholeSpan.data() + 0, 3`.

`wholeSpan.subspan(1, 3)` means start at index `1`, with a length of `3`.
This is equivalent to `wholeSpan.data() + 1, 3`.

If the length parameter is omitted, `subspan` determines it automatically
so that the `span` extends to the end of the array.

For example, instead of `wholeSpan.subspan(1, 3)`, you can use `wholeSpan.subspan(1)`.
</details>

### 24. Details of `subspan`

What happens if, in the previous example, you go beyond the array bounds, for example:
```cpp
std::span<int> s{ wholeSpan.subspan(2, 3) };
```

<details>
<summary>Answer</summary>

There is no bounds check here; accessing index `2` of `s` is simply UB.

> Creating an invalid `std::span` is not considered UB,
> by analogy with pointers, but reading beyond the array bounds is.
</details>

### 25. Looping in reverse (1)

What will this print?
```cpp
#include <iostream>
#include <array>
#include <span>
#include <cassert>

void print(std::span<int> s)
{
   int lastIndex = static_cast<int>(s.size()) - 1;
   for (int i { lastIndex }; i >= 0; i--)
   {
       size_t si = static_cast<size_t>(i);
       assert(si < s.size());

       std::cout << s[si] << std::endl;
   }
}

int main()
{
   std::array<int, 4> arr{1, 2, 3, 4};
   print({ arr });
}
```

<details>
<summary>Answer</summary>

The example prints the array elements in reverse order.

`static_cast` is used to avoid warnings
about possible information loss (a narrowing conversion from `size_t` to `int`)
and implicit sign conversion (from `int` to `size_t`).
</details>

### 26. Looping in reverse (2)

What will this print?
```cpp
#include <iostream>
#include <array>
#include <span>
#include <cassert>

void print(std::span<int> s)
{
   for (size_t i { s.size() - 1 }; i >= 0; i--)
   {
       assert(i < s.size());

       std::cout << s[i] << std::endl;
   }
}

int main()
{
   std::array<int, 4> arr{1, 2, 3, 4};
   print({ arr });
}
```

<details>
<summary>Answer</summary>

All elements will be printed, and then the program will crash.

Since `i` is an unsigned type,
`0 - 1` as `size_t` will not be `-1`; an underflow will occur and the result will be the maximum `size_t` value.
Then `assert(i < s.size())` will crash the program, because `i` becomes greater than the array size.

This can be avoided by checking manually:

```cpp
void print(std::span<int> s)
{
   if (s.size() == 0)
   {
       return;
   }
   size_t i { s.size() - 1 };
   while (true)
   {
       assert(i < s.size());
       std::cout << s[i] << std::endl;
       if (i == 0)
       {
           return;
       }
       i--;
   }
}
```

Or treat the maximum value as an invalid index and compare it with `-1` converted to `size_t`:

```cpp
void print(std::span<int> s)
{
   for (size_t i { s.size() - 1 }; i != static_cast<size_t>(-1); i--)
   {
       assert(i < s.size());
       std::cout << s[i] << std::endl;
   }
}
```
</details>
```cpp
#include <iostream>
#include <array>
#include <cassert>

void print(int* start, int* end)
{
   for (int* current{start}; current <= end; current++)
   {
       std::cout << *current << std::endl;
   }
}

int main()
{
   std::array<int, 4> arr{1, 2, 3, 4};
   print(arr.data(), &arr[arr.size() - 1]);
}
```
```cpp
#include <iostream>
#include <array>
#include <cassert>

void print(int* start, int* pastEnd)
{
   for (int* current{start}; current != pastEnd; current++)
   {
       std::cout << *current << std::endl;
   }
}

int main()
{
   std::array<int, 4> arr{1, 2, 3, 4};
   print(arr.data(), &arr[arr.size()]);
   print(arr.begin(), arr.end());
}
```
