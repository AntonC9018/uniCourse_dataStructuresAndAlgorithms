# Operator overloading

## Assignment operator overloading

We still have a major elephant in the room, 
who makes itself known in a dangerous way when we copy into an existing variable.
See the example [here](#Breaking-the-code-above).

We can fix that issue by redefining what assignment does for our type.
This is called *assigment operator overloading*, "assignment operator" meaning the `=` in the assignment operation, 
and "overloading" meaning defining a function which will substitute the default behavior for our type.

```cpp
class Example
{
    int* memory;

public:
    Example(int value)
    {
        this->memory = new int{value};
    }

    ~Example()
    {
        delete this->memory;
    }

    void operator=(const Example& other)
    {
        // This is the default behavior.
        // Like illustrated in a previous example, 
        // the default behavior can easily cause memory leaks and repetitive frees.
        // this->memory = other.memory;

        // This is the behavior we want.
        *this->memory = *other.memory;
    }
};

int main()
{
    Example example1{1};
    Example example2{2};

    // This calls the assignment operator.
    example2 = example1;

    // `operator=` is just the name of that method,
    // you can call it like a regular method as well:
    example2.operator=(example1);

    return 0;
}
```

## Another solution: prohibiting copying

You can make an operator that is allowed to be used implicitly, unusable,
by *deleting* the method responsible for the operator.
You do that by assigning the `delete` keyword to the method, instead of providing a body.

```cpp
class Example
{
    // ...

    // This makes the operator = unusable.
    void operator=(const Example& other) = delete;
}

int main()
{
    Example example1{1};
    Example example2{2};

    example1 = example2; // compile-time error
    return 0;
}
```

There's also a way to explicitly state that we want the `default` behavior for some function.
This can be useful if you wanted to bring back the parameterless constructor, for example,
without having to type out a method body that does the equivalent thing.
You can also use it for the copy constructor.

To do this, you have to assign the `default` keyword to the method.

> The example will break at runtime and is given for demo purposes.

```cpp
class Example
{
    // ...

    // Allow the default behavior for the parameterless constructor.
    Example() = default;

    // Allow the default behavior for the copy constructor.
    Example(const Example& other) = default;

    // For good measure, let's explicitly state that we want 
    // the assignment to do the default thing as well.
    // The return type has to be `Example&` for this to work (I explain why a bit later).
    Example& operator=(const Example& other) = default;
}

int main()
{
    // Our custom constructor.
    Example example1{1};

    // Parameterless constructor
    Example example2{};

    // Copy constructor
    Example example3{example1};

    // Assignment operator
    example2 = example1;

    return 0;
}
```


## Overloading math operators: `Vector` use-case

I have implemented a Vector struct with operations for addition, 
subtraction and scaling.

One implementation is procedural, the other one is with operator overloading.
See the example code [here](./vector/procedural.cpp) and [here](./vector/operator.cpp).


## Returning values or references from mutating operators

> By "mutating operators" I mean stuff like `=`, `+=`, `-=` etc.

We can go one step further and implement the `+=` and `-=` operators as well.
You can choose any return type that you find logical, but usually it's either `void` or `Vector` or `Vector&`.
See [an example](./vector/mutation.cpp).
We return a reference for stuff like this to be allowed (but it's not required):

```cpp
int main()
{
    Vector a{6, 9};
    Vector b{2, 3};
    Vector c{5, 6};

    // We can do it in multiple steps
    a = a + b;
    Vector result = a;
    result = result + c;

    // Or in a single step
    Vector result = (a += b) + c;
    // The idea is that `a += b` return either the value of `a`, 
    // or a reference to `a`, which will be the result of `a + b`, 
    // aka the new value of `a` after the addition.

    return 0;
}
```

## Another use case: printing to the console

You may remember that C++ uses the `<<` (bitwise left shift) 
operator for interacting with the output stream.
This is achieved by using `friend` functions, 
which allows it to access the private fields of `Vector`.

> `friend` functions are implicitly static, aka they don't have a hidden `this` parameter.

```cpp
#include <iostream>

struct Vector
{
    int x;
    int y;

    // The second parameter can be either `Vector`, `Vector&` or `const Vector&`.
    // (You can technically make it anything you want, but it's pointless).
    friend std::ostream& operator<<(std::ostream& outputStream, Vector vector)
    {
        outputStream << "(" << vector.x << ", " << vector.y << ")" << std::endl;
        return outputStream;
    }
};

int main()
{
    Vector v{1, 2};
    std::cout << v; // (1, 2)
    return 0;
}
```

Notice how the overloaded operator returns a reference to the output stream object.
This allows you to use the `<<` operator again right after the first one.
This is called a *fluent* interface; you can learn more on your own.

For example, code like this works without an issue 
due to the fact that we return the stream object reference:

```cpp
int main()
{
    Vector v1{1, 2};
    Vector v2{5, 6};

    // This:
    (std::cout << v1) << v2;

    // Is equivalent to this (evaluated left to right):
    std::cout << v1 << v2;

    // Does the same thing as this, in effect.
    std::cout << v1;
    std::cout << v2;

    return 0;
}
```


`friend` functions are a bit weird when it comes to separating declaration from definition:

```cpp
struct Vector
{
    // ...
    // Declaration
    friend std::ostream& operator<<(std::ostream& outputStream, Vector vector);
};

// Definition.
// You don't need the scope resolution operator `::`.
// In fact, using it here is invalid.
std::ostream& operator<<(std::ostream& outputStream, Vector vector)
{
    // ...
}
```

`friend` functions allow you to put the logic that comes to printing your object
in the your class, rather than in the `std::ostream` class.
This is useful when you can't or have a reason not to 
modify the type that is used as the first parameter,
meaning you can't or don't want to add that operator 
as a regular operator in the source code of the class of the first parameter.

In this case, of course, since `std::ostream` is from the standard library,
you cannot modify its source code.
But even if it weren't, you may only want it to have general functionality for printing text,
and not have to burden it with the specifics of printing your concrete type.
This can let your other type define the printing logic, 
based on the fundamental operations provided by `std::ostream`,
such as string or `int` output.

This idea is closely related to encapsulation and is typically called *separation of concerns*.

To be noted that `std::ostream` overloads the `<<` operator for some of the fundamental types,
like `const char[N]`, `int`, `float`, etc, which is how you're able to use `<<` for printing.
And you're able to use it fluently (chain operators) 
because it returns a reference to the same stream object.
