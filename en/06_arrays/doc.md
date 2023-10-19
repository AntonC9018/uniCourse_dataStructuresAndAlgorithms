## On C arrays

C arrays is the arrays that we have learned in the previous chapter.
As a reminder, here is an example of a C array:

```c
int a[4];
```

They support the indexing operator and represent a linear block of memory.


### Functions that take arrays as arguments

You cannot pass C arrays to functions.
You can only pass the address to the memory of an array.


### Sum example

For example, let's define a function `sum` that takes in the address
of the first element of some array and sums up all elements one by one,
returning the sum as the result.
Note that the function has to know how many elements that block is in size.

```c
int sum(int* a)
{
    int result = 0;
    for (size_t i = 0; i < 4; i++)
    {
        int* pointerToElmement = a + i;
        int elementAtIndex = *pointerToElement;
        result = result + elementAtIndex;
    }
}
```

The prototype of the function can be instead:

```c
int sum(int a[]);
```

which means the same thing.
I'm going to stick to the pointer notation, because the latter makes no sense in my opinion.


Now let's try to call this function:
```c
int main()
{
    // Note that the length has to be the exact same as used in the function.
    int arr[4]{};
    arr[0] = 5;
    arr[1] = 10;

    // Pass it the pointer to the start of the memory of the array.
    int sum = f(&arr[0]); // 15

    // Passing the array variable implicitly passes the address of the first element.
    // This is also referred to as the array "decaying" to a pointer.
    int sum1 = f(arr); // 15

    return 0;
}
```

### Stack corruption

Notice how if you make an error with the array length,
for example make the array in `main` have a length less than expected in the function,
the compiler won't give you any warnings.
In fact, it's very likely that the program will execute without an issue, 
but product garbage results.

Imagine if `main` went like this:

```c
int main()
{
    int arr[2]{};
    sum(arr);
}
```

The `sum` function would try to sum memory after the memory assigned to the array elements,
which will in fact read the memory that comes after it on the stack.
The next thing after the local array variable `arr` on the stack 
will most likely be the return address for the `sum` function.

Now imagine if the `sum` function wrote to that memory, instead of just reading from it.

```c
void setZeros(int* a)
{
    for (size_t i = 0; i < 4; i++)
    {
        a[i] = 0;
    }
}
```

If executed with a wrong size, this could lead to *stack corruption* --
the return address on the stack could be overwritten with zeros,
which would cause the program to crash when the function tries to return.

Stack corruption means messing with memory outside of the expected memory that is available. 


### Passing the length as a parameter

To avoid this, you should always pass the length along with the pointer.
See the complete example in [array.cpp](array.cpp).

Now in order not to repeat the length multiple times,
you can either define a constant to hold it, like this (fine):

```cpp
const size_t arrayLength = 4;

int main()
{
    int arr[arrayLength]{};
    sum(arr, arrayLength);
    return 0;
}
```

Or use a `define` (don't do this):
    
```cpp
#define ARRAY_LENGTH 4UL

int main()
{
    int arr[ARRAY_LENGTH]{};
    sum(arr, ARRAY_LENGTH);
    return 0;
}
```

Or compute it at compile time where you call the function using `sizeof`.
`sizeof(arr)` gets you the length in bytes of the whole array, and we have to
divide that with the length of a single element `sizeof(arr[0])`
to get the number of elements.

```cpp
int main()
{
    int arr[4]{};
    sum(arr, sizeof(arr) / sizeof(arr[0]));
    return 0;
}
```

In C++, there's one more option: a template parameter, not explained in too much detail.
But basically, it can understand the length from the array type.

```cpp
template<size_t N>
int sum(int (&arr)[N])
{
    int result = 0;
    for (size_t i = 0; i < N; i++)
    {
        result += arr[i];
    }
    return result;
}

int main()
{
    int arr[4]{};
    sum(arr);
    return 0;
}
```


