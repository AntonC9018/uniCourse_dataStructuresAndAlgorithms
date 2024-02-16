# `enum` and `enum class`

`enum` allows you do define named compile-time constants in a straightforward way.

## The concept of an enumeration

`enum` stands for *enumeration*, which means an exhaustive list of possible things.
Imagine you wanted to represent the colors of a traffic light, how would you do that?
Well, the most straightforward way would be to define a constant for each possible color:
one for red, one for yellow, and one for green.

```cpp
static inline const int RED = 0;
static inline const int YELLOW = 1;
static inline const int GREEN = 2;
```

The `static inline` are there in order to make the linker not consider them when linking files,
and so that they don't end up in the final executable.
Each file that wants to use these constants, can just import the file that defines them,
without caring about duplicate definitions.

And you could use it [like this](./enums/global_const_list.cpp).

That's precisely what `enum` does.
It just allows you to define these constants easier.

```cpp
enum TrafficLightColors
{
    RED = 0,
    YELLOW = 1,
    GREEN = 2,
};
```

Moreover, specifying the values becomes optional.
They are autoincremented by the compiler if omitted.
So if you don't write them, like this:

```cpp
enum TrafficLightColors
{
    RED,
    YELLOW,
    GREEN,
};
```

It's basically equivalent to this:

```cpp
enum TrafficLightColors
{
    RED = 0,
    YELLOW = RED + 1,
    GREEN = YELLOW + 1,
};
```

And if you were to do:

```cpp
enum TrafficLightColors
{
    RED,
    YELLOW = 55,
    GREEN,
};
```

It would be equivalent to:

```cpp
enum TrafficLightColors
{
    RED = 0,
    YELLOW = 55,
    GREEN = YELLOW + 1, // 56
};
```

## `enum class`

It would be a good idea to have a way to enforce that the type of the
integer passed into some function is one of the listed values.
You can do this by means of a `struct`. See the [example](./enums/namespaced_enum.cpp).

And that's basically what `enum class` allows you to achieve, just with a
way simpler syntax. See the [example](./enums/enum_class.cpp).

> The only important difference is that in our `struct` implementation, 
> you don't necessarily have to define the constants within the namespace,
> but with `enum class` they are always defined in the namespace.
> Which means that you can pull all of the constants into the current scope with `using`,
> but you can't do the same with `enum class`.


## The base type

Enums are not limited to ints -- you can use any other type to represent the values.
For example, you could use a byte, if the max value is less than 256.
You do that by specifying the base type after the name of the enum.

```cpp
#include <stdint.h>

enum TrafficLightColor
    : uint8_t // base type, 8-bit unsigned int
{
    RED = 0,
    YELLOW = 1,
    GREEN = 2,
};
```

Also, you can actually write an invalid value to a variable of an enum type,
aka write a value that is not one of the constants.
You typically don't expect that in the code, so when you stumble upon a value like that,
it's generally reasonable to `assert(false)` to crash the program.

```cpp
enum class TrafficLightColor
    // : int // implicitly int
{
    RED = 0,
    YELLOW = 1,
    GREEN = 2,
};

int main()
{
    // Creating an invalid color is allowed.
    TrafficLightColor color = static_cast<TrafficLightColor>(5);
    return 0;
}
```
