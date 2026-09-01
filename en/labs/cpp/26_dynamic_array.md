# Dynamic Array — Practice

## 1. Procedural Dynamic Array

Videos:
- [Arrays](https://www.youtube.com/watch?v=3aXFuiHxb9k&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=11)
- [Memory Types](https://www.youtube.com/watch?v=jAr_jicQv4Y&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=14)
- [Basic Programming Techniques](https://www.youtube.com/watch?v=gLp7OtaNGrs&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=15)


Write the code for a dynamic array data structure:

```cpp
struct DynamicArray
{
    // ...
}
```

1. Create a factory function that returns an array with the initial capacity
   specified by the `capacity` parameter.
   Create another factory function that uses a default `capacity` (for example, 4).

```cpp
void test1()
{
    DynamicArray arr = createDynamicArrayWithCapacity(10);
    assert(arr.capacity == 10);
}
```

2. It must expose its buffer capacity (`capacity`)
   and store the current number of elements (`length` / `count`).

```cpp
void test2()
{
    DynamicArray arr = createDynamicArray();
    assert(arr.length == 0);
    addElementToArray(&arr, 5);
    assert(arr.length == 1);
}
```

3. When adding elements to the array, double its capacity if the array is full.
   That is, allocate a buffer twice as large and copy all elements into it.
   Add the element at the end of the array.

```cpp
void test3()
{
    DynamicArray arr = createDynamicArrayWithCapacity(1);
    addElementToArray(&arr, 5);
    assert(arr.capacity == 1);
    addElementToArray(&arr, 10);
    assert(arr.capacity == 2);
    addElementToArray(&arr, 20);
    assert(arr.capacity == 4);
}
```

4. Create a function to access array elements by index.
   Perform a bounds check based on the length in this function using `assert`.

```cpp
void test4()
{
    DynamicArray arr = createDynamicArray();
    addElementToArray(&arr, 5);
    int el = getElementAtIndex(&arr, 0);
    assert(el == 5);
}
```

5. Create a function that returns the currently used portion of the array as a `std::span`.
   Adding elements to the array may invalidate a previously returned `std::span`.
   This means you can simply release the old buffer when necessary, without extra checks.
   Invalidation means that existing pointers to array elements become invalid
   (the memory they point to may have been deleted).


```cpp
void test5()
{
    DynamicArray arr = createDynamicArray();
    addElementToArray(&arr, 5);
    addElementToArray(&arr, 6);
    addElementToArray(&arr, 7);

    std::span<int> span = getCurrentSpan(&arr);

    assert(span.size() == 3);
    assert(span[0] == 5);
    assert(span[1] == 6);
    assert(span[2] == 7);
}
```

6. Create a function that releases the dynamic memory allocated for the array.
   Call this function when the array memory is no longer needed (`free` / `destroy`).

7. Create a `main` function that checks all these features
   (in separate functions or separate scopes).
   Make the test functions static so they cannot be linked from other code.
   Add your own tests as needed (at least 1).

8. Put the code related to the structure in separate files—make the dynamic array a module.
   - Put the function *declarations* for working with the structure and the structure itself in `dynamicArray.h`.
   - Include `dynamicArray.h` in `main.cpp`.
   - Put the function *definitions* in `dynamicArray.cpp`.
     > You may put very short functions in `dynamicArray.h` as `inline`.
   - If there are helper functions that you use in the array code but not in `main`,
     make them `static` and do not add them to `dynamicArray.h`.
   - Add the compilation command to a `.bat` (or `.sh`) script in the lab folder.

  
## 2. The Same, but Using RAII

Videos:
- [OOP, RAII](https://www.youtube.com/watch?v=Lc2VUm09-6s&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=16)

Do the same thing, but:

1. Instead of factory functions, use a default constructor and a constructor with a `capacity` parameter.
2. Instead of `free` / `destroy`, define a destructor.
3. Define a copy constructor.
4. Overload the assignment operator.
5. Define a move constructor.
5. Define an overload of the assignment operator that takes an rvalue reference parameter.
6. Overload the subscript operator for element access.
7. Make `addElementToArray` a method and call it `add`.
8. Make the fields `private` by changing `struct` to `class`.
9. Allow field values to be read
   by defining `size` and `capacity` accessor methods.
11. In the `main` function, test all features and show usage examples.

> The interface here should be roughly like that of `std::vector`.

- What mistakes does the procedural version allow compared with the OOP version?
  (hint: public fields, creating copies).
- Which version is easier to understand / use? In which situations? Why?
- What role does encapsulation play here?

Iterators (additional):

1. Make range-based `for` iteration possible.
   To do this, you can either create your own iterator or use a method that returns `std::span`.
