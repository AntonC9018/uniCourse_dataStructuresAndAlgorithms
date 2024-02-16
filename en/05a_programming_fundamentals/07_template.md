# `template`

`template` is a C++ language primitive, which, 
together with the overload mechanism, enables *static polymorphism*.

## Basic `template` usage

`template` at a basic level allows you to automate copy pasting of function overloads.

> See [a basic example](./template/example_1)

Consider the following example:

```cpp
int sum(std::span<int> arr)
{
    int result = 0;
    for (size_t i = 0; i < arr.size(); i++)
        result += arr[i];
    return result;
}

// Overload the function, which means define another function with
// different parameter types (or count thereof).
float sum(std::span<float> arr)
{
    float result = 0;
    for (size_t i = 0; i < arr.size(); i++)
        result += arr[i];
    return result;
}

int main()
{
    std::array<int, 3> arrInt = { 1, 2, 3 };
    // Calls `sum` with an `std::span<int>` parameter.
    // Implicitly convert to `std::span<int>`
    int resultInt = sum(arrInt);

    std::array<float, 3> arrFloat = { 1.0f, 2.0f, 3.0f };
    // Calls `sum` with an `std::span<float>` parameter.
    float resultFloat = sum(arrFloat);

    return 0;
}
```

`template` allows you to write out the function only once, for any type.
The following templated function will work not only for `float` and `int`,
but also for any other type that has a default constructor, and overloads the `+=` operator.

```cpp
template<typename T>
T sum(std::span<T> arr)
{
    T result{};
    for (size_t i = 0; i < arr.size(); i++)
        result += arr[i];
    return result;
}

int main()
{
    std::array<int, 3> arrInt = { 1, 2, 3 };
    // We have to convert to `std::span<int>` manually.
    std::span<int> spanInt = arrInt;
    int resultInt = sum(spanInt);
    // It understands that `T` should be `int` from the type of the variable
    // that is passed in. It's equivalent to:
    // resultInt = sum<int>(spanInt);

    std::array<float, 3> arrFloat = { 1.0f, 2.0f, 3.0f };
    std::span<float> spanFloat = arrFloat;
    float resultFloat = sum(spanFloat);
    // equivalent to
    // resultFloat = sum<float>(spanFloat);

    return 0;
}
```

Templated function definitions are a bit magical when put in a header file.
Even if they are used from multiple compilation units, the linker is smart enough
to automatically remove duplicate definitions derived from these functions.
Aka if you called `sum<int>` from two different compilation units,
there will (typically) only be a single definition of `sum` for the `int` type parameter,
even though both the compilation units had had their own copy created.
So basically templated functions typically work like `static` functions,
where the duplicates are automatically trimmed (removed).

> Technically, they aren't guaranteed to be trimmed.

> TODO: source. I vaguely remember reading about this somewhere.

> See [an example of this](./template/example_2).


## `template` for types 

In the same way, you can use `template` for types (structs/classes).
There are no additional issues with this approach if you only have fields in the type.

> See [example_3](./template/example_3).

It appears to work, which I honestly did not expect, even if you have methods
defined in-place in your type.

> See [example_4](./template/example_4).


## Explicit template instantiation

The problems with templates begin when you want to only 
*declare* the method / function in the header file,
but define it in a separate implementation file.
In this case a definition is never created.
You have to make sure an explicit definition is created.
You can do this in the file that defines the template by *explicitly instantiating the template*.

You can also import the file with the templated definition (`f.cpp`),
and instantiate it explicitly in another file.

> See [example_5](./template/example_5).

For types, it works in a similar way.
Methods that are only declared, but not defined, 
in a templated class definition will require 
an explicit instantiation of the templated definition in order to be defined.

> See [example_6](./template/example_6)


## Templated methods within templated classes

In this situation you just have to apply the `template` thing multiple times.
The rest works just like in the previous examples.


## Passing things other than types as template parameters

You can pass e.g. numbers as template parameters.
You have already used this previously with `std::array<Type, Size>`.
Here's an example:

```cpp
template<size_t N> // you write the type instead of `typename`
std::array<int, N> createArray()
{
    return {};
}

int main()
{
    std:array result = createArray<10>();
    return 0;
}
```

These can be implied automatically as well:

```cpp
template<size_t N>
void doStuff(std::array<int, N>& arr)
{
    // ...
}

int main()
{
    std::array arr = { 1, 2, 3 };
    doStuff(arr); // calls `doStuff<3>`
}
```

