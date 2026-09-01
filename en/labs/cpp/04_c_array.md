# C arrays (groups of variables)

- [Arrays and indexes](https://www.youtube.com/watch?v=859Y0Q8pyLg&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=8)
- [A video that covers the fundamentals in more depth](https://www.youtube.com/watch?v=9AhNOjjyAwU&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=14)

## Concepts

- Indexing
- Getting the address of the first element

## Examples to aid understanding

### 1. Array

```cpp
int arr[2]{};
arr[0] = 1;
arr[1] = 2;

std::cout << arr[0];
std::cout << std::endl;

std::cout << arr[1];
std::cout << std::endl;
```

<details>

<summary>

What does `int arr[2]{}` mean?

</summary>

It declares an array of 2 elements, all initialized to zero by `{}`.
</details>

<details>
<summary>What is an array?</summary>

An array is like several variables combined into one. 
In this case, there are effectively 2 variables: `arr[0]` and `arr[1]`.

The phrase “effectively” is intentional here, because in fact `arr[0]` and `arr[1]` are objects,
not variables, but that is covered in another lesson.
</details>

<details>
<summary>Answer</summary>

`arr[0]` and `arr[1]` can effectively be treated like variable names.
So 1 and 2 will be printed.
</details>

### 2. Array initialization
```cpp
int arr1[2]{ 21, 32 };

std::cout << arr1[0];
std::cout << std::endl;

std::cout << arr1[1];
std::cout << std::endl;
```

<details>
<summary>What does this syntax mean?</summary>

Here, the array elements are initialized when the array is created, in index order (0, 1).
</details>

### 3. Array with an unspecified length
```cpp
int arr1[3]{ 1, 2, 3 };
int arr2[]{ 1, 2, 3, 4 };

std::cout << sizeof(arr1);
std::cout << std::endl;

std::cout << sizeof(arr2);
std::cout << std::endl;
```

<details>

<summary>

What is `sizeof`?

</summary>

It is an operator evaluated at compile time that gives the size of the entire array in bytes.
In this example, the `arr1` array has 3 ints, each 4 bytes, so the total size is 12.
</details>

<details>

<summary>

What is the size of `arr2`?

</summary>

`arr2` has no explicitly specified size; its size is determined automatically from its elements.
</details>

<details>

<summary>

What does `[]` mean?

</summary>

In this context, the array length is determined at compile time by the number of elements on the right
(4 in this example).
</details>

<details>
<summary>Answer</summary>

3 ints of 4 bytes each make 12.

4 ints of 4 bytes each make 16.
</details>

### 4. Reading by index
```cpp
int arr[3]{ 1, 2, 3 };
size_t index { 2 };
int it { arr[index] };
std::cout << it;
std::cout << std::endl;
```

<details>
<summary>Answer</summary>

You can use a variable or expression to specify an index.

The answer is 3.
</details>

### 5. Writing by index
```cpp
int arr[3]{};
size_t index { 2 };
arr[index] = 5;
std::cout << arr[2];
std::cout << std::endl;
```

<details>
<summary>Answer</summary>

You can also write by index using an index produced by an expression.
</details>

### 6. An expression as an index
```cpp
int arr[3]{};
size_t index { 1 };
arr[index + 1] = 5;
std::cout << arr[2];
std::cout << std::endl;
```

<details>
<summary>Answer</summary>

This demonstrates using a more complex expression
to obtain an index.
</details>

### 7. Copying an array element into a variable
```cpp
int arr[3]{ 0, 2, 1 };
size_t index { 2 };
int it { arr[index] };
arr[index] = 5;
std::cout << it;
std::cout << std::endl;
```

<details>
<summary>Answer</summary>

On the line `int it { arr[index] }`, the *value `1`* is copied into `it`,
not a reference to an array element, because the type of `it` is `int`.
Since it is just an `int`, changing the array element from which its value originated
after assignment does not affect `it`.

`1` will be printed.
</details>

### 8. A pointer as the element type
```cpp
int a = 1;
int b = 2;
int* arr[]{ &a, &b };
*arr[0] = 3;
*arr[1] = *arr[0];

std::cout << arr[0] << std::endl;
std::cout << arr[1] << std::endl;

std::cout << *arr[0] << std::endl;
std::cout << *arr[1] << std::endl;
```

<details>
<summary>Answer</summary>

Arrays can store data other than `int` values.
In this example, the array stores pointers to `int` values (`int*`).

- `arr[0]` contains the address of variable `a`.
- `arr[1]` contains the address of variable `b`.
- `a`, equivalent to `*arr[0]`, equals `3`.
- `b`, equivalent to `*arr[1]`, equals `3`.
</details>

### 9. Using an array as a pointer
```cpp
int arr[2]{};
int* p = arr;
*arr = 1;

std::cout << *p;
std::cout << std::endl;

std::cout << arr[0];
std::cout << std::endl;

std::cout << arr[1];
std::cout << std::endl;
```

<details>
<summary>Answer</summary>

When `arr` is used as an expression in `int* p = arr`,
it decays into a pointer to the first element of the array.
Here, `arr` is equivalent to `&arr[0]` or `&(arr[0])`.

`*p`, `*arr`, and `arr[0]` all access the same array element.

1 will be printed twice.
</details>

<!-- Missing: get address of item at index, different type than int -->
