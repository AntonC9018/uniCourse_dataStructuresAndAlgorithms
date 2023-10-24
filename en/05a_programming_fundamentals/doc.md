## References (\&)

A reference is basically a pointer whose address 
it points to cannot be changed, and with simplified syntax.

You can also think of it as an alias for a variable (a memory location).

```cpp
int main()
{
    int a = 5;
    
    int* pointer = &a;
    int& reference = a;
    
    *pointer = 10; // a = 10
    reference = 15; // a = 15
    
    int b = 20;
    // You can't do this to make `reference` refer to `b`.
    // The following will write the value of `b` (20) into `a`.
    reference = b; // a = 20
    reference = 10; // a = 10
    
    return 0;
}
```

You can pass references to functions.
Under the hood, they are passed as pointers.

```cpp
void foo(int& a)
{
    a = 10;
    a = a + 5;
}

int main()
{
    int a = 5;
    foo(a); // a = 15
    return 0;
}
```

The same program, but using a pointer instead:

```cpp
void foo(int* a)
{
    *a = 10;
    *a = *a + 5;
}

int main()
{
    int a = 5;
    foo(&a); // a = 15
    return 0;
}
```

It's a more constrained version of a pointer, perfect for function arguments.
It is considered good practice to use references instead of 
pointers when passing arguments to functions.


## Methods

Consider a function that takes in a struct variable.

```cpp
#include <iostream>

struct Person
{
    int age;
    std::string name;
};

void printAge(Person* person)
{
    std::cout << person->age;
}

int main()
{
    Person person;
    person.age = 20;
    person.name = "John";
    
    printAge(&person);
    
    return 0;
}
```

### `static` method

We can convert this function into a member function, also called a method.
Let's first make it a static member function, to see how the concept of *namespaces* works.

> Note that methods only exist in C++ and not in C.

```cpp
#include <iostream>

struct Person
{
    int age;
    std::string name;
    
    // The `static` keyword doesn't actually make it static,
    // it just requires you to call this function using the scope resolution operator (::).
    static void printAge(Person* person)
    {
        std::cout << person->age;
    }
};

int main()
{
    Person person;
    person.age = 20;
    person.name = "John";
    
    // This is how you call a static member function.
    // `Person` is the namespace here, and `printAge` is the method.
    // The idea is that we're able to associate the operations 
    // that operate on a `Person` in the `Person` namespace of this struct.
    Person::printAge(&person);
    
    return 0;
}
```

You can separate the declaration from the definition, just like with regular functions.
Note that there's no other syntax for doing this, 
you have to write the struct name in the definition.

```cpp
struct Person
{
    int age;
    std::string name;
    
    static void printAge(Person* person);
};

// Think of `Person::printAge` as the name of this function.
static void Person::printAge(Person* person)
{
    std::cout << person->age;
}
```

### Instances and Objects

*Instance* stands for the memory of a variable of some type.
So in the following code:

```cpp
Person person;
```

we can say that `person` is an instance of the `Person` type.


*Object* means the value of an instance of some type.
So we can say that `person` contains a `Person` object.


### Non-static (instance) methods

Now let's make it a non-static member function.
A non-static member function has simpler call syntax, 
and automatically passes the pointer to the instance as the first hidden parameter named `this`.

```cpp
struct Person
{
    int age;
    std::string name;
    
    // Instance method.
    void printAge()
    {
        // `this` is a pointer to the instance (`Person*`).
        std::cout << this->age;
    }
};

int main()
{
    Person person;
    person.age = 20;
    person.name = "John";
    
    // This is how you call an instance method.
    // The compiler automatically passes the pointer to the instance as the first parameter.
    person.printAge();
    
    return 0;
}
```

This allows us to marry functionality to the data type, 
and get the "object.verb" semantics.


`this->` is optional to write out.

```cpp
struct Person
{
    // ...
    void printAge()
    {
        // `age` refers to `this->age`.
        std::cout << age;
    }
}
```