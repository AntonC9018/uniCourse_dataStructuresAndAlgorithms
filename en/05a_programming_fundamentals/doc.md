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

> Do not worry about how `std::string` works yet, 
> just conceptually think of it as a string.

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

> *Member* means something that's declared in a `struct` or `class`.
> It can be either a method or a field.

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
};
```

You can separate definition from declaration the same way you did with static methods.

## Accessibility and `class`

By default, all members of a struct are `public`.
This means they can be accessed on an instance of the struct.
You can make them `private` explicitly, to disallow access.

This might seem completely useless at first. 
I mean, what's the point of disallowing access to some memory?
One of the ideas is to limit the ways in which the data can be accessed 
or modified to make it obvious which way is the correct way by using methods.

This isn't something unique to OOP, you can do this on a module level by making some functions `static`
(only visible internally within the compilation unit they were defined).
The *accessibility modifiers* specifically is an OOP exclusive thing though.

```cpp
struct Person
{
private:
    int age;
    std::string name;

public:
    void setAge(int age)
    {
        this->age = age;
    }

    void printAge()
    {
        std::cout << this->age;
    }

    void printName()
    {
        std::cout << this->name;
    }
};

int main()
{
    Person person;
    person.age = 15; // compile-time error: cannot access private field.
    person.name = "John"; // same error

    person.setAge(15); // compiles
    person.printAge(); // compiles
    person.printName(); // compiles

    return 0;
}
```

You can make some fields `private`, and others `public`.

```cpp
struct Person
{
private:
    int age;

public:
    std::string name;
}

int main()
{
    Person person;
    person.age = 10; // compile-time error: cannot access private field.
    person.name = "John"; // works
    return 0;
}
```


### `class`

`class` is equivalent to `struct`, the only difference 
being that it has an implicit `private:` at the top.
So all of the members are public by default in a `struct`, but private in `class`.

> `class` is the keywords that's usually used in the context of OOP.
> It is considered good tone to use `class` instead of `struct` if you declare any methods
> that encapsulate (provide well-defined access patterns to) the data (the fields).

```cpp
struct Person
{
private:
    int age;
    std::string name;
}

// is the same as

class Person
{
    int age;
    std::string name;
}

// and vice-versa ...

class Person
{
public:
    int age;
    std::string name;
}

// is the same as

struct Person
{
    int age;
    std::string name;
}
```

## Scopes

Scopes have two functions in C++:
- They serve to make variables not visible outside of them;
- They are used to clean up memory ("resources") of objects.
  This can be achieved by using destructors.

You can say that scopes allow you to control the lifetimes of objects.

### Scopes for limiting the visibility

You can create scopes by using `{ ... }`.

```cpp
int main()
{
    int a = 1;

    {
        int b = 2;
        a = 5; // allowed, `a` is visible in outer scope
        b = 10; // allowed, `b` is visible in the current scope
    }

    b = 10; // not allowed, `b` is not visible, because its scope has ended 
            // (the brace has been closed).

    a = 15; // still allowed, because it's visible in the current scope

    return 0;
}
```

Functions must define a scope for their body.


You can redeclare variables with the same name if they are in different scopes.
They are not guaranteed to end up pointing at the same memory.

```cpp
int main()
{
    int a = 5;

    // Redeclaring the variable in the same scope is not allowed.
    // int a;

    {
        // Redeclaring it here is also not allowed.
        // int a;

        int b = 10;
    }

    {
        // This is allowed, because the scopes don't interact.
        int b = 20;

        {
            // This would be disallowed.
            // int b = 30;
        }
    }

    return 0;
}
```

A scope within another scope is called a *nested scope*.
You can *nest* scopes indefinately.

> In general, putting things within other things of the same kind is called *nesting*.

There's also the concept of the global scope, 
which is the scope that's outside of any function.


### Scopes for cleaning up resources

Conceptually, a variable defined in a scope is destroyed at the end of the scope.
For simple types like int, it means literally nothing.
For a complex type, like `std::string`, this means 
returning the memory allocated for the character array to the C++ runtime.


### Destructor 

You can define your own logic to be called when your object is destroyed by using a *destructor*.
Destructor is a special `void` function that is called in this context automatically.
You can call it manually as well.


Let's just illustrate how it works.

```cpp
#include <iostream>

struct Demo
{
    int i;

    // This is a destructor
    ~Demo()
    {
        std::cout << "Destroying demo" << this->i << std::endl;
    }
};

int main()
{
    Demo demo1{1};
    Demo demo2{2};
    std::cout << "Demos created" << std::endl;

    return 0;

    // The compiler implicitly adds the following:
    // `demo2.~Demo();`
    // `demo1.~Demo();`
}
```

Which prints:

```
Demo created
Destroying demo
```

> You can split the destructor declaration and the definition 
> the same way you do with regular methods.

Note that the destructor will only be called in that context.
If you reassign the variable, it won't be called for the object already in that memory.

```cpp
int main()
{
    Demo demo1{1};
    Demo demo2{2};
    demo2 = demo1; // This copies the object, but doesn't call the destructor of `demo2`.

    return 0;

    // `demo2.~Demo()` runs, printing "Destroying demo 1"
    // `demo1.~Demo()` runs, printing "Destroying demo 1"
}
```

> To make sure the destructor of `demo2` is in fact called, 
> we'll have to overload the assignment operator.


## Constructors

Constructors are special `void` functions used to initialize objects.
Constructors cannot be called in any other context.

Constructors were created to allow initializing private data members (fields) in OOP.
Constructors can be more involved than that, but it's generally discouraged to make them complex.

> If they get out of hand, you can switch to using factory functions.

For example, let's define a parameterless constructor (a default constructor),
which prints to the console.

```cpp
#include <iostream>

class Demo
{
    int memory;

public:
    Demo()
    {
        // memory will be unitialized at this point (contain garbage).
        std::cout << "Created " << this->memory << std::endl;
        this->memory = 5;
    }

    ~Demo()
    {
        // memory is 5 here.
        std::cout << "Destroyed " << this->memory << std::endl;
    }
};

int main()
{
    {
        // This actually calls the parameterless constructor.
        // C++ designers decided that objects must never be unitialized.
        Demo demo;

        // Compiler implicitly added:
        // demo.~Demo();
    }

    {
        // Explicitly calls the parameterless constructor.
        Demo demo{};

        // Equivalent syntax:
        // Demo demo = Demo();

        // Compiler implicitly added:
        // demo.~Demo();
    }

    return 0;
}
```

A practical use case would be e.g. to allocate memory, and clean it up in the destructor.
We can do this by using the `new` and `delete` operators.


```cpp
#include <iostream>
#include <assert.h>

class Buffer
{
// private:
    size_t length;
    int* firstElement;

public:
    Buffer(size_t elementCount) 
        // Writes `elementCount` to length directly, before our code is run.
        // This is called a member initializer.
        : length(elementCount)//, anotherField(8)
    {
        // NOTE: firstElement contains garbage here.

        // We need to allocate memory, which won't be readable in the initializer.
        // This is why I decided to write it in the constructor body.
        this->firstElement = new int[elementCount];

        // The elements are initially uninitialized.
    }

    ~Buffer()
    {
        delete[] firstElement;
    }

    int& elementAt(size_t index)
    {
        assert(index < this->length);
        return firstElement[index];
    }
};

int main()
{
    Buffer buffer{5};

    // Prints garbage.
    std::cout << buffer.elementAt(0) << std::endl;

    // Do some stuff with the buffer.
    int& secondElement = buffer.elementAt(1);
    secondElement = 10;

    return 0;

    // The compiler inserted the following automatically.
    // buffer.~Buffer();
}
```

It is still extremely easy to break the code above and end up with a memory leaks or repeated memory deletes:

```cpp
int main()
{
    Buffer buffer1{10};
    Buffer buffer2{20};
    // This does a memberwise copy.
    buffer2 = buffer1;
    return 0;

    // the buffer with 20 length is never deallocated
    // the buffer with 10 length is deallocated twice (runtime error)
}
```