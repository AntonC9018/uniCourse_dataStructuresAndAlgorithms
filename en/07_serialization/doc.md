
## Domain data models

Domain data model is a struct that represents some thing from the real world.
In the following simple example, the struct `Car` represents a car object.

```cpp
struct Car
{
    std::string companyName;
    std::string modelName;
    std::string numberplateText;
    int producedYear;
    int numberOfDoors;
};
```

One of the key idea is that you can have multiple variables of this type 
to represent data about different cars.

```cpp
int main()
{
    Car myCar{
        "Audi", // companyName
        "A4", // modelName
        "MD1515", // numberplateText
        2000, // producedYear
        4, // numberOfDoors
    };

    Car neighborsCar{
        "Toyota",
        "Camry",
        "JK1516",
        2002,
        6,
    };

    return 0;
}
```

### Validation

What you very often want to do, 
is you want to validate if the data in your object is valid.
For example, we may want to make sure the `companyName` has been specified,
the number of doors is not negative,
and the year produced is no more than the current year.

#### Bool

There are multiple ways in C++ that you can represent errors.
The very basic but nonetheless useful way is to output `true` if it's valid,
and `false` otherwise.

The problem with this approach is that it does not give you enough information
to diagnose the problem when it occurs.

> [`time_t`](https://en.cppreference.com/w/cpp/chrono/c/time_t)

> [See example](validation/bool_example.cpp)

#### String error

You could mitigate this problem by logging the error that happened,
or returning a string to be logged.
This is a valid solution, unless you want the code to be
used in other places to determine and deal with errors programmatically:
you will have the ability to help the user using the program to diagnose the problem
by looking at the logs, but your other functions won't be able to
easily determine what went wrong, because they'd have to be able to
analyze the string. 

> [See example](validation/string_example.cpp)

This approach also allows you to record multiple errors, outputting each,
separated by a newline character, for example.

> [See example](validation/string_multiline_example.cpp)


##### Enum and flags

This can be useful when you want to record just the specific kind of error.
The idea is to give each error a unique number, and return that number.

> [See example](validation/enum_example.cpp)
