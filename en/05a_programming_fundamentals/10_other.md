## `const`

`const` means that the value of something cannot be changed.

### Basic usage

You can define `const` variables, which will prevent you from modifying their value.

```cpp
const int a = 5;
a = 10; // compile time error
```

This applies to any types, including custom types.

```cpp
struct T
{
    int value;
};

// ...

const T a{5};
a.value = 10; // not allowed, because a.value is part of the memory of the `a` variable.
a = { 50 }; // it is not allowed to change the whole memory either.
```

You can apply `const` to parameters as well.
It means the function is not allowed to change the value of the parameter.
While pretty useless by itself for copies, it's very useful for references and pointers.
For example, let's say we had a `Demo` type:

```cpp
struct Demo
{
    int value;
    int expensiveToCopy[1000];
};

void stuff(const Demo& demo)
{
    int value = demo.value; // reading is allowed.
    demo.value = 5; // writing not allowed.
    demo = { 6 }; // overwriting also not allowed.
}
```

### `const` with pointers

Generally, `const` only applies one level deep for pointers.
For example, a `const int*` or `int const*` means that the *memory pointed at* cannot be changed,
but the pointer itself can,
and `int* const` means that *the pointer address itself* cannot be changed,
but the memory pointed at can.
Similarly, `const int* const` means that neither can be changed.

For pointers multiple levels deep, you need to specify the `const` for each level.

```cpp
void func(
    int* p, // mutable address, mutable object
    const int* p1, // mutable address, immutable object
    int* const p2, // immutable address, mutable object
    const int* const p3 // immutable address, immutable object
)
{
    int local = 8;

    *p = 10;
    p = &local;

    // *p1 = 10;
    p1 = &local;

    *p2 = 10;
    // p2 = &local;

    // *p3 = 10;
    // p3 = &local;
}
```

For pointers to objects with pointers, `const` is only applied at the first level.
It won't be applied to the nested pointer's memory.

```cpp
struct Demo
{
    int someValue;
    int* pointer;
};

void func(const Demo* demo)
{
    int local = 8;
    // demo->someValue = 10;
    // demo->pointer = &local;
    *demo->pointer = 10; // this is allowed.
}
```

### `const` vs `constexpr`

The value of a `const` variable used 
with compile-time known constants of a primitive type
can be used in a compile-time context.
For example, it can be used as the size of
a static array, or as a template parameter. 

```cpp
#include <array>
static inline const size_t arrayLength = 10;

int arr[arrayLength];
std::array<int, arrayLength> arr2;
```

It won't work if you were to use a struct for example:
```cpp
#include <array>
struct Test
{
    size_t value;
};

// This will only be available at runtime,
// because it's not a primitive type.
static inline const Test arrayLength = { 10 };

int arr[arrayLength.value]; // not allowed
std::array<int, arrayLength.value>; // not allowed
```

But you can make it work if you changed `const` to `constexpr` in this example.
`constexpr` makes it a compile-time constant.

`constexpr` can also be used with functions to tell
the compiler that they can be evaluated at compile time.
`constexpr` functions can only call other `constexpr` functions.
It's yet another rabbit hole, so I'll stop here. 

### `const` methods

`const` can be applied to a method, which just applies to the `this*` pointer.
The syntax is like this:

```cpp
class Demo
{
    int state;

private:
    int readState() const
    {
        return this->state;
    }
};

// Which conceptually means basically:
int readState(const Demo* const this)
{
    return this->state;
}
```

### `const_cast`

This can be useful when you know an operation will not modify an object,
even though it is not declared const.
A valid use case is for example a function that provides access 
to the n-th element of an array.

```cpp
struct Buffer
{
    int* elements;
    size_t length;
};

int& getRefAtIndex(Buffer& buff, size_t index)
{
    return buff.elements[index];
}

// Have to implement the same method for a const Buffer.
// The result should be const, because we want the const of the Buffer 
// to be transitive for the items in the buffer.
const int& getRefAtIndex(const Buffer& buff, size_t index)
{
    // Note how we have to provide the exact same implementation.
    return buff.elements[index];
}

int main()
{
    Buffer buff{new int[5], 5};
    const Buffer buffConst{new int[5], 5};

    // Calls the mutable overload
    getRefAtIndex(buff, 0);

    // Calls the const overload
    getRefAtIndex(buffConst, 0);

    return 0;
}
```

In order not to have to implement the same function body a second time,
we can make the first mutable function call the second `const` one.
This means we have to cast the parameter to `const`,
and then cast the result back to non-const.
You can see how it will in fact be a valid implementation, since
that `const` only affects the return type.

```cpp
int& getRefAtIndex(Buffer& buff, size_t index)
{
    // first cast the buffer type
    const Buffer& constBuff = buff;
    // now call the const function
    const int& element = getRefAtIndex(constBuff, index);
    // now remove `const`
    return const_cast<int&>(element);
}
```


### Good practices

It's considered good practice and leads to more robust code
to follow const-correctness, meaning that one should
always apply `const` wherever appropriate.


## Smart pointers

If you understand RAII, it should be easy to grasp smart pointers as well.

### `std::unique_ptr`

`std::unique_ptr` is a templated type that represents dynamically allocated memory
that follows RAII.

### `std::shared_ptr`


## `auto` and `decltype`

The section about polymorphism kind of requires `auto` when discussing lambdas,
so I figured I'll explain this here.

### `decltype`

`decltype` is an operator that returns you the type of an expression:

```cpp
struct T { float x; };

int main()
{
    int a{1};
    decltype(a) b{2}; // int b{2};
    b += a;

    T t{1.0f};
    decltype(t) t1{2.0f}; // T t1{2.0f};
    decltype(t.x) x{3.0f}; // float x{3.0f};
    decltype(T::x) x1{4.0f}; // float x1{4.0f};
    return 0;
}
```

It cannot be used at time of declaration.

```cpp
decltype(a) a = 5; // doesn't compile
decltype(5) a = 5; // this is fine
```

The expression can be more complicated:

```cpp
#include <math>
decltype(std::max(5, 6) - static_cast<float>(5)) a = 5.0f; // float a = 5.0f;
```

### `auto`

`auto` is a keyword that allows the compiler to *deduce* or *imply* the type of a variable
from the expression type that you assign to it.

`auto x = y;` is equivalent to `decltype(y) x = y;`.

```cpp
int a1 = 5;
auto a2 = 5; // int a2{5};
```

It can also be used as the return type of functions.
In the following example, the compiler deduces that the return type of `f` is `int`:

```cpp
auto f()
{
    return 5;
}
```

To be extra clear, variables declared with `auto` as the type are still statically typed.
You cannot reassign a different type to them.

```cpp
auto a = 5;
a = 6; // fine
a = "Hello"; // doesn't compile
```

