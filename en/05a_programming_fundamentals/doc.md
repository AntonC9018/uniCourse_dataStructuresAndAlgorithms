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

You can apply `&` to a reference to get a pointer to the variable.

A reference a more constrained version of a pointer, perfect for function arguments.
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
void Person::printAge(Person* person)
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

> `class` is the keyword that's usually used in the context of OOP.
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
Destroying demo2
Destroying demo1
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
    demo2 = demo1; // This copies the object's bytes, but doesn't call the destructor of `demo2`.

    return 0;

    // `demo2.~Demo()` runs, printing "Destroying demo 1"
    // `demo1.~Demo()` runs, printing "Destroying demo 1"
}
```

> To make sure that the same object isn't deleted more than once
> in this situation, we'll have to overload the assigment operator.


### Implicit destructors

Say you had a struct with a field whose type has a destructor.

```cpp
#include <iostream>

struct Test
{
    ~Test()
    {
        std::cout << "Destroying test" << std::endl;
    }
};

struct Person
{
    Test test;
};

int main()
{
    Person person;
    person.test = {};
    return 0;

    // The compiler automatically calls the destructor of each field.
    // `person.test.~Test();`

    // It will also delete the temporary object used for the assignment,
    // but that's explained in more detail later.
}
```

## Constructors

Constructors are special `void` functions used to initialize objects.
Constructors cannot be called in any other context.

Constructors were created to allow initializing private data members (fields) in OOP.
Constructors can be more involved than that, but it's generally discouraged to make them complex.

### Constructors used to initialize new objects

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
        : length(elementCount) //, anotherField(8)
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

### Breaking the code above

It is still extremely easy to break the code above and end up with memory leaks or repeated memory deletes:

```cpp
int main()
{
    Buffer buffer1{10};
    Buffer buffer2{20};
    // This does a memberwise copy.
    buffer2 = buffer1;
    return 0;

    // the buffer with length 20 is never deallocated
    // the buffer with length 10 is deallocated twice (runtime error)
}
```


### Copy constructors

You can define a constructor that takes in an object reference,
which is going to be called on copy initialization.
This includes regular definitions with `{ }`, or definitions with an immediate assignment.


```cpp
#include <iostream>

class Demo
{
    int id;

public:
    // We need a constructor with parameters to be able to create an object in the first place.
    Demo(int idParameter) : id(idParameter) { }

    // Demo(const Demo& other)
    Demo(Demo& other) : id(other.id)
    {
        std::cout << "Copying " << other.id << std::endl;
    }
};

int main()
{
    Demo a{1};

    // Calls the copy constructor.
    Demo b{a};

    // Also calls the copy constructor.
    Demo c = a;

    // This does NOT call the copy constructor. 
    // It just does a memberwise copy.
    b = c; 
}
```


### Moving an object

Moving an object into another object makes one steal the resources of the other.
This is often used when constructing objects, 
or writing values into fields to avoid calling the copy constructor.

Consider the following example, which creates 2 copies of `std::string`:

```cpp
struct Person
{
    std::string name;
};

int main()
{
    // Calls the constructor of `std::string`, 
    // which copies the characters into a dynamically-allocated buffer.
    std::string name = "John Brown";

    Person person;

    // Makes a copy of `name` by allocating another buffer and copying the characters.
    // It then writes this copy into `person.name`.
    person.name = name;

    return 0;

    // The compiler implicitly adds the following:
    // `person.name.~string();` (from the implicit destructor of Person which deletes all fields)
    // `name.~string();`
}
```

So what we do is we move `name` into `person.name`, instead of copying it.
In this case, this means, in essence, copying the string object into `person.name`,
and then clearing it from the `name` variable, so that it no longer refers to the buffer.
So it becomes unusable after the call.

```cpp
#include <iostream>

struct Person
{
    std::string name;
};

int main()
{
    std::string name = "John Brown";
    Person person;

    std::cout << name << std::endl; // // prints "John Brown"
    std::cout << person.name << std::endl; // prints nothing

    person.name = std::move(name);

    std::cout << name << std::endl; // prints nothing
    std::cout << person.name << std::endl; // prints "John Brown"

    return 0;
}
```


### Move constructors

In general, you can define constructors that take in *rvalue references* (\&\&).
This basically means a reference from which you're supposed to steal resources.

> Don't get hung up on the details here, I will explain what rvalues are later.

> You can use rvalue references as regular parameters as well.

```cpp
#include <iostream>

class Demo
{
    int* memoryPointer;

    int getValue()
    {
        if (memoryPointer == nullptr)
            return 0;
        return *memoryPointer;
    }

public:
    Demo(int value)
    {
        // Allocate an int on the heap (just as a demo, I know this is pointless),
        // and store the pointer to it in `memoryPointer`.
        this->memoryPointer = new int{value};
    }

    ~Demo()
    {
        std::cout << "Destructor called for " << this->getValue() << std::endl;
        // Deallocate (deleting a nullptr is allowed).
        delete this->memoryPointer;
    }

    // Move constructor
    Demo(Demo&& other)
    {
        std::cout 
            << "Move constructor called for "
            << other.getValue()
            << std::endl;

        // Steal the pointer from the other object.
        this->memoryPointer = other.memoryPointer;

        // Clear the pointer from the other object.
        // `nullptr` is the same as `0`, it just zeros it out.
        other.memoryPointer = nullptr;
    }
};

int main()
{
    Demo demo1{1};
    Demo demo2{2};

    // This calls the move constructor.
    Demo demo3 = std::move(demo1);

    return 0;

    // The compiler implicitly adds the following:
    // demo3.~Demo(); (clears memory with 1)
    // demo2.~Demo(); (clears memory with 2)
    // demo1.~Demo(); (doesn't do anything)
}
```

### Return value optimization (RVO)

If you return an object from a function, its destructor will not be called.
In fact, the move constructor won't be called either.
It will just write the result directly into the memory of the variable declared for the result.

> I have not described how returning objects from functions actually works,
> but that's because I don't know the actual mechanics myself.
>
> It may be returned in one or more of the registers, and then copied into the variable on the stack, 
> or the function might take a hidden "output" address, where it will write the result.
> I don't know in which situation which implementation is used by the compiler,
> and whether there are more clever ways to do this.
>
> If you do know or want to learn more, I'd appreciate it if you made a PR with a brief explanation,
> or linked some resources.

```cpp
Demo test()
{
    Demo demo1{1};
    Demo demo2{2};
    return demo1;

    // `demo2.~Demo();` inserted by the compiler, as usual.
    // Destructor call for `demo1` NOT inserted here.
}

int main()
{
    // Compiler might implement this by passing `test` a hidden pointer to the local `demo`,
    // and giving that memory to the local `demo1` in `test`,
    // such that the memory of `demo1` isn't actually stored on the stack frame of `test`.
    // You can think of `demo1` as being a reference to `demo`.
    // Do note that this isn't what the compiler will necessarily do,
    // it's just one way it could implement this behavior.
    Demo demo = test();
    return 0;

    // `demo.~Demo();` inserted by the compiler, as usual.
}
```

RVO is the reason you *should not be moving objects out of functions*.

```cpp
Demo test()
{
    Demo demo{1};
    // DO NOT do this, this will make an extra copy.
    // This will call the move constructor into the output memory,
    // as well as trigger the destructor of the local `demo` at the end of the function.
    return std::move(demo);
}
```


## Operator overloading

### Assignment operator overloading

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

### Another solution: prohibiting copying

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


### Overloading math operators: `Vector` use-case

I have implemented a Vector struct with operations for addition, 
subtraction and scaling.

One implementation is procedural, the other one is with operator overloading.
See the example code [here](./vector/procedural.cpp) and [here](./vector/operator.cpp).


### Returning values or references from mutating operators

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

### Another use case: printing to the console

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


## Abstraction and Encapsulation

### Implementation files (cpp)

Let me clarify some points related to implementation files (`cpp` files).
`cpp` files typically contain *definitions of functions and/or global variables*.
They may expose said functions to be used in other compilation units (in other cpp files),
but they may also define `static` functions and global variables,
which can be used as helpers in the exposed functions, that is, 
help implementing the logic of the exposed functions.

What do you think would happen if a `cpp` file were to be included in the compilation twice?
Assume we compiled the two files `main.cpp` and `f.cpp` with the command `zig c++ main.cpp f.cpp`,
where the files have the following contents:

`main.cpp`:

```cpp
#include "f.cpp"

int main()
{
    f(1);
    return 0;
}
```

`f.cpp`:

```cpp
void f(int a)
{
}
```

The answer is that it will produce a linker error,
because the function `f` has been defined twice:
once in `main.cpp` (due to us including the contents of `f.cpp`)
and a second time in `f.cpp` (because we compile this file too).

This basically implies that *it is only valid to compile each implementation file at most once*.


### Sharing declarations

What do we do if we wanted to use the same function `f` in multiple different files?
Well, we just have to declare it in all of those files, and then link them to the implementation.
> See [example 1](./headers/example_1)

The problem is that now if we wanted to change e.g. the parameter type of `f`
from `int` to `float`, we'd have to:
- Modify the implementation file,
- Modify the `f` declaration in `main.cpp`,
- Modify the `f` declaration in `other_file.cpp`.

And if we had more files, we'd have to go through all of them.

What people usually do to only have to modify the declaration in a single file,
is that they put the declaration in a separate file, and paste the declaration
in the files that need it using `#include`.
The files that contain such declarations are called header files.
Of course, the definition will still have to be modified separately.
> See [example 2](./headers/example_2)

If the function definition is obvious and small, like returning some constant, it is
common to put the *definition* directly in the header file.
Now, if we just went ahead and did that, we'd have
the same problem as in [the paragraph above](#Implementation-files-(cpp)).
Recall the `inline` modifier, which makes it so that the function does not participate
in linking, and won't appear in the final executable.
This use case is perfect for `inline`.
In fact, we don't even need an implementation file if all functions can be made inline.
> See [example 3](./headers/example_3)

The other way to avoid linker errors here is to make all functions `static`.
This is typically discouraged, because the executable file will include their definitions
as many times as the header is imported.


### The interface

A *module* can be defined as a header-implementation file pair.
You can see how the header file, having the declarations, effectively specifies the 
*public interface* of the *module*, while the implementation file specifies the
*implementation* of the interface. 

*Abstraction* means that you interact with a module only via its public interface.
*Encapsulation* means that you can interact with the module as a whole,
without having to understand how it's implemented and what data exactly it uses under the hood. 

Contrary to common opinion, OOP did not invent either of these.
You can use these principles without using classes.
OOP just adds finer-grained encapsulation at *class level*, 
in the form of the accessibility system (public - private members),
and finer-grained abstraction at class level via virtual methods (maybe described later?).

So OOP allows these two concepts both *at module level and at class level*,
while regular procedural programming only allows this *at module level*.


### Avoiding duplicate declarations

> TODO: this example is kinda jack, because I assume multiple declarations aren't allowed.

Assume we had code like this:

```cpp
void f(int a);
void f(int a);
void f(int a)
{
    std::cout << a;
}
```

It might be undesirable to have multiple declarations of the same function.
Now assume a situation where `main.cpp` includes `a.h` and `b.h`,
and `b.h` includes `a.h` too.
This would mean `a.h` has been included twice.
If `a.h` declared any functions, our program will include the declarations multiple times.

This can be avoided by using `#pragma once`, which instructs the preprocessor
to only include this file once.
If added in `a.h`, it will make it only be included in `main.cpp`,
with `b.h` skipping importing it.
Now, `b.h` will still see the declarations from `a.h`,
because it is put after `a.h` had been included in `main.cpp`.

We have a very similar situation in [the `inline` example](./headers/example_3).
If you removed `#pragma once` from `f.h`, it will fail to compile.


### Circular includes

These are not allowed, because files are only ever included sequentially.


### `private` fields

Like I have mentioned before, typical procedural programming does not allow
class-level (struct-level) encapsulation, but only module-level encapsulation.
This means *the data in the structs that the interface expects the users to pass in can be changed by the user*.

An example: assume we had a type that represents a dynamically allocated fixed-size buffer.
The code could be something like this:

```cpp
struct DynamicBuffer
{
    int* firstItemPointer;
    size_t length;
}

DynamicBuffer createBuffer(size_t length)
{
    int* pointer = new int[length];
    return {pointer, length};
}

void setItem(DynamicBuffer* buffer, size_t index, int value)
{
    assert(index < buffer->length);
    buffer->firstItemPointer[index] = value;
}

void destroyBuffer(DynamicBuffer* buffer)
{
    delete[] buffer->firstItemPointer;
};
```

Because there's no encapsulation of data at class (struct) level,
the following code will compile, but will break at runtime.

```cpp
int main()
{
    DynamicBuffer buffer = createBuffer(10);
    buffer.firstItemPointer = 0; // there's nothing stopping us from doing this.
    setItem(&buffer, 0, 5); // runtime error: access violation
    return 0;
}
```

Now of course here it is obvious that doing that is wrong,
because it violently breaks the internal state of the buffer,
but it is still allowed without an issue by the compiler.
The idea with accessibility is to be able to explicitly disallow that.

```cpp
class DynamicBuffer
{
    // Private data
    int* _firstElementPointer;
    size_t _length;

public:
    // We still want to be able to *read* that data,
    // but not *write* to it directly.
    // So we can define *properties* for this.
    // Properties are methods that return or set the values of fields.
    // Note that I've named the fields with an underscore so that we don't
    // have name collisions with the properties.
    int* firstElementPointer()
    {
        return this->_firstElementPointer;
    }

    size_t length()
    {
        return this->_length;
    }

    DynamicBuffer(size_t length) : _length(length)
    {
        this->_firstElementPointer = new int[length];
    }

    ~DynamicBuffer()
    {
        delete[] this->_firstElementPointer;
    }

    void setItem(size_t index, int value)
    {
        assert(index < this->_length);
        this->_firstElementPointer[index] = value;
    }
};
```

```cpp
int main()
{
    DynamicBuffer buffer{10};
    buffer._firstElementPointer = 0; // does not compile
    int* firstElement = buffer.firstElementPointer(); // can still *read* the value
    return 0;
}
```

But it also disallows you to define any additional operations 
that are not included in the `DynamicBuffer` class that need to operate with its private state.
So the following will not work in the OOP version:

```cpp
int resize(DynamicBuffer& buffer, size_t newSize)
{
    if (buffer.length() < newSize)
    {
        buffer._length = newSize;
    }
    else
    {
        int* newBufferPointer = new int[newSize];
        for (size_t i = 0; i < buffer.length(); i++)
            newBufferPointer[i] = buffer.firstElementPointer()[i];
        delete[] buffer.firstElementPointer();
        buffer._firstElementPointer = newBufferPointer;
    }
}
```

But the equivalent procedural version will work without an issue.

> I think you can work around this with `friend` functions, but you're typically not expected to.


### `private` members in the header file

It should be pretty clear why fields are required to be in the header file.
This is because the knowledge of these is required to know the size of the class,
and you have to know the size of the class, because you 
*control the memory where the object will be stored.*

However, private *methods* are put into the header file only to be able to work around
the encapsulation issue: you cannot define static functions in the implementation file,
while being able to access the private fields of the class, so you are forced to make
them known to the user in the declaration (the header file).

`buffer.h` contains the class declaration (constructors and such omitted):

```cpp
class DynamicArray
{
    int* pointer;
    size_t count;
    size_t capacity;

public:
    void addItem(int item);

private:
    void ensureCapacity(size_t newMinimumSize);
};
```

`buffer.cpp` contains the definitions:

```cpp
void DynamicArray::addItem(int item)
{
    this->ensureCapacity(this->count + 1);
    this->pointer[this->count] = item;
    this->count++;
}

void DynamicArray::ensureCapacity(size_t newMinimumSize)
{
    if (this->capacity >= newMinimumSize)
        return;

    int* oldMemory = this->pointer;
    size_t newSize = std::max(newMinimumSize, this->capacity * 2);
    int* newMemory = new int[newSize];
    for (size_t i = 0; i < this->count; i++)
        newMemory[i] = oldMemory[i];
    this->pointer = newMemory;
    delete[] oldMemory;
}
```

This, however, goes against the idea that the header file
*must only contain the public interface, providing encapsulation at the module level*.
Ideally, we'd want the private function *not to exist in the header file*,
because it is only used internally within the module, being an implementation detail.
There's no reason why it should stay in the header.

If we tried to just make it `static` and use it in the implementation file, so:

`buffer.h`:

```cpp
class DynamicArray
{
    int* pointer;
    size_t count;
    size_t capacity;

public:
    void addItem(int item);

    // No private methods here...
};
```

`buffer.cpp`:

```cpp
void DynamicArray::addItem(int item)
{
    ensureCapacity(this, this->count + 1);
}

// static, so only visible and usable within this compilation unit.
static void ensureCapacity(DynamicArray* self, size_t newMinimumSize)
{
    // Cannot access self->capacity, because it's private.
    if (self->capacity >= newMinimumSize)
        return;

    // ...
}
```

It of course won't work because of accessibility rules.

You can work around this by using the fact that
*types that you don't allocate memory for, or find the size of, don't have to declare their fields*,
combined with the fact that *types can be used as namespaces* 
and *have access to the private members of the containing type*.
See a more detailed explanation [here](https://stackoverflow.com/questions/28334485/do-c-private-functions-really-need-to-be-in-the-header-file).

So you can achieve the above static function behavior like this:

```cpp
class DynamicArray
{
    // ... fields
public:
    void addItem(int item);

private:
    // This is called a *forward declaration*.
    struct Impl;
};
```

```cpp
// Making the struct static makes all of the methods static (internal linkage).
static struct DynamicArray::Impl
{
    // We don't require an instance.
    // `static` here doesn't mean internal linkage,
    // it means no implicit `this` parameter.
    static void ensureCapacity(DynamicArray* self, size_t newMaximumSize)
    {
        // This now works, because we're technically inside of DynamicArray.
        if (self->capacity >= newMaximumSize)
            return;
        
        // ...
    }
}

void DynamicArray::addItem(int item)
{
    DynamicArray::Impl::ensureCapacity(this, this->count + 1);
    // or like this
    // Impl::ensureCapacity(this, this->count + 1);
    // because we're technically inside DynamicArray's scope already.

    this->pointer[this->count] = item;
    this->count++;
}
```

## `template`

`template` is a C++ language primitive, which, 
together with the overload mechanism, enables *static polymorphism*.

### Basic `template` usage

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


### `template` for types 

In the same way, you can use `template` for types (structs/classes).
There are no additional issues with this approach if you only have fields in the type.

> See [example_3](./template/example_3).

It appears to work, which I honestly did not expect, even if you have methods
defined in-place in your type.

> See [example_4](./template/example_4).


### Explicit template instantiation

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


### Templated methods within templated classes

In this situation you just have to apply the `template` thing multiple times.
The rest works just like in the previous examples.


### Passing things other than types as template parameters

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

## Iterators

An *iterator* is a powerful programming pattern that allows you to abstract the logic
of iterating over a collection of items.

### Iterator pattern example

Imagine you had a tree graph, and you wanted to do a 
[depth-first traversal of it](./iterator/graph_1.cpp), 
printing all of the values.

Now that's simple enough, but what if you also wanted 
to compute the sum of all values in the nodes?
You'll have to duplicate the traversal function, 
and just change the logic that you do:

```cpp
int sumDFS(const Node* node)
{
    int result = node->value;
    for (size_t i = 0; i < node->children.size(); i++)
        result += sumDFS(node->children[i]);
    return result;
}
```

You can see how this might become problematic if the traversal logic was more involved
than just recursively looping through the children.

Now, one of the ways to solve this would be to use the strategy pattern,
aka passing in a function to be executed when visiting a node.
How you do that will be described later.

Here, we will discuss the iterator pattern instead, 
which is another solution to this problem,
and to that a more flexible one.
It will allow you to pause the traversal, and resume it later, as well as do 
any operation with the elements, and accessing any of your variables you want.

The idea is to store the current state of iteration in an object,
effectively representing how the stack will look in the recursive traversal,
and then define functions to advance the iterator to the next element
(and possibly more functions to e.g. go to the previous one).
We will also need a way to signal that the iteration has ended.
See [the code](./iterator/graph_manual_iterator.cpp).

> I recommend you take some time with the debugger 
> to understand how the program works.

Sure, it is more complicated, especially the fact that in this case you have 
to imitate the stack manually (you don't always have to),
and it will generally turn out more complicated than straightforward iteration,
but the added flexibility + removing code duplication may be really valuable.

### C++ iterators

C++ has a "standard way" of doing iterators, which is required for some
templated functions in the standard library to work:

- The iterator type overloads the `++` operator, to mean the `advance` method from my example.
  It also optionally overloads the `--` operators, to go back to the previous element.

- The iterator type overloads the `*` operator, to mean the `value` method from my example. 
  `*` as in pointer dereference. It should return a reference if possible.

- The iterator has a special state that means the end of iteration.
  In my case, I defined an `empty` method, but we could represent this "empty" state
  with both vectors being empty.
  Emptiness is then checked by comparing the iterator against this special state.

- Types that define a single way of iterating may define a `begin` and `end` method,
  which return the iterator state of the first element, 
  and the special "empty" state respectively.

See [the same example as before, but using the standard iterator pattern](./iterator/graph_standard.cpp)

The motivation for a design like this is to mimic the interface that you have with pointers.
`++p` moves the pointer by one element, `*p` reads the value at the address,
and `p == start+count` checks if we've reached the end of an array, for example.

### Benefits of the stardard way

If you do your iterator the C++ way, you get some nice syntax for range iteration.
If your type has `begin` and `end` methods, you can use it in a range-based for loop.
See [an example](./iterator/graph_range_for.cpp).

This syntax is enabled for most container types, because they follow this pattern,
defining `begin` and `end` methods, as well as an iterator type with the operations
described above.

You don't have to define another type. 
If it only makes sense to do one kind of iteration for your data structure,
or some sort of way of iterating should obviously be the default,
you can define a `begin` and an `end` method for your container type directly.
That would make sense for e.g. a `DynamicArray`, but it probably won't for a graph.


## `static_cast`, `reinterpret_cast`, `bit_cast`

`static_cast` for basic types is equivalent to a regular C cast.
It's different only in the context of class inheritance.
It can cast, with potentially modifying the pointer,
to a less derived type, but not the other way.

`reinterpret_cast` is a cast that just changes the type of a pointer,
without changing the address, skipping checks if the conversion is valid.

`bit_cast` can be used to reinterpret the bits of a type as another type.
For example:
```cpp
float a = 5.0f; // 40 a0 00 00 = 5.0
int b = std::bit_cast<int>(a); // 40 a0 00 00 = 1084227584
int c = static_cast<int>(a); // 5
```


## Namespaces

We have already met with type scopes, which have the namespace concept built into them.
However, if you want a language primitive which just provides the namespace concept,
you can use `namespace`.

### Basic usage

A namespace basically means a scope that can house functions, variables, types and other namespaces,
and can be used to avoid name collisions within these.

I've been using the `std` namespace in my examples extensively.
`std` is a namespace that comes from the standard library, but we can easily create our own.

```cpp
#include <iostream>

// We define a namespace called Demo.
namespace Demo
{
    // Put a function within Demo.
    void f()
    {
        std::cout << "Hello from Demo::f" << std::endl;
    }
}

int main()
{
    // We can use the scope resolution operator to access the function.
    // This is analogous to using `.` for accessing struct fields.
    Demo::f();
    return 0;
}
```

Notice how it's practically the same as a static function in a type declaration.
This is because type declarations can function as namespaces.

```cpp
#include <iostream>

struct Demo
{
    static void f()
    {
        std::cout << "Hello from Demo::f" << std::endl;
    }
};

int main()
{
    Demo::f();
    return 0;
}
```

You can nest namespaces within namespaces.

```cpp
namespace Demo
{
    namespace Demo1
    {
        void f()
        {
        }
    }
}

int main()
{
    Demo::Demo1::f();
    return 0;
}
```

Namespaces can be used when you have different function implementations
of a function with the same name, which you want to be able to differentiate:

```cpp
namespace Impl1
{
    void f()
    {
        std::cout << "Hello";
    }
}
namespace Impl2
{
    // Even though it has the same name, it won't cause a linker error.
    void f()
    {
        std::cout << "World";
    }
}
int main()
{
    Impl1::f(); // Hello
    Impl2::f(); // World
    return 0;
}
```

You can define namespaces multiple times, in multiple places,
and they will refer to the same bag of stuff.

```cpp
namespace Demo
{
    void f()
    {
    }
}

namespace Dima
{
    void g()
    {
    }
}

// Refers to the same namespace as the Demo above.
namespace Demo
{
    // This namespace is not the same as Dima above.
    // This namespace is really called Demo::Dima.
    namespace Dima
    {
        // Totally allowed, no compile-time error
        void g()
        {
        }
    }

    // Also allowed, no compile-time error.
    void g()
    {
    }

    // Duplicate definition, compile-time error.
    // We've got an `f()` above already.
    void f()
    {
    }
}
```

Which means that defining the `std` namespace in your code is totally allowed.
It's even required for some things, like defining a hash function for a type.

```cpp
namespace std
{
    void f(){}
}

int main()
{
    std::f();
    return 0;
}
```

Note that `main` must not be in any namespace to play the special role of the entry point.


### Namespaces allow you to use things from the namespace without qualification

```cpp
namespace Demo
{
    void f()
    {
    }

    void g()
    {
        // We can use `f` without qualification.
        f();
        // We could use `Demo::f` if we wanted to.
        Demo::f();
    }
}
```

This is analogous to the idea that you don't have to type `this->` when accessing
fields or methods while inside the body of a method.

By the way, the same thing applies with name scopes created by `struct` or `class`.

Another thing is that the nested namespaces can see the things defined in the outer namespaces.
This is analogous to scopes in functions, the difference being that you *are* allowed
to define functions with the same prototype in the different scopes.

```cpp
namespace Outer
{
    void f()
    {
    }

    void g()
    {
    }

    namespace Inner
    {
        // Redefining `g` in a nested namespace is allowed.
        void g()
        {
            // Calls `Outer::f()`
            f();
        }
    }
}
```

### Shortcutting with the `::` operator

You don't have to nest every single namespace individually.
You can use `::` in the namespace definition.
The following code:

```cpp
namespace Outer
{
    namespace Inner
    {
        void f()
        {
        }
    }
}
```

Is equivalent to:

```cpp
namespace Outer::Inner
{
    void f()
    {
    }
}
```

### The global scope

The global scope is the scope that is outside of any namespace.
It doesn't have a name.
It can be used to disambiguate things in some niche situations.

```cpp
namespace Demo
{
    void f()
    {
        std::cout << "Outer";
    }

    namespace Dima
    {
        namespace Demo
        {
            void f()
            {
                std::cout << "Inner";
            }
        }

        void g()
        {
            // We want to call the `Demo::f` from the global scope.
            // However, just calling `Demo::f` will call the `f` from the inner `Demo`.
            Demo::f(); // Inner

            // To be able to call the outer `Demo::f`, we have to use the global scope.
            ::Demo::f(); // Outer

            // The inner call can be written like this:
            ::Demo::Dima::Demo::f(); // Inner
        }
    }
}
```


### `using namespace`

`using namespace` is pretty cool. 
It can be used to bring everything from a namespace into the current scope.
By bring, I mean make all members of the namespace visible, aka
available without qualification.
The coolest thing is that it can be used in *any* scope, be it separate function scopes,
nested regular scopes, namespaces or type scopes.

```cpp
#include <iostream>

int main()
{
    {
        // Make all of std members visible here without qualification.
        using namespace std;

        cout << "Hello" << endl;
    }

    {
        // But not here.
        cout << "World" << endl; // compile-time error
    }
}
```

`using namespace` is pretty dangerous, because it may lead to a function
other than yours to be selected for overload resolution,
that is, the compiler might call a standard function with the same name as yours,
which better matched by its parameters.

I'm going to show you this with a more tame example, so that you get the idea.

```cpp
#include <iostream>

namespace Demo
{
    void f(int a)
    {
        std::cout << "Demo::f -- " << a << std::endl;
    }
}

// We happily define a second function, which takes a float instead,
// and we expect that to be called, because we don't know about the one in Demo.
void f(float a)
{
    std::cout << "Happy life" << std::endl;
}

int main()
{
    using namespace Demo;
    // Guess which function will be called here?
    f(5); 
    return 0;
}
```

`using namespace std` is extremely dangerous because of this,
because `std::` has **a lot** of crap inside of it 
that will *very likely* have the same names as some of your stuff.
You might spent countless miserable hours trying 
to figure out why your function doesn't do what it supposed to,
only to later realize that you haven't even been testing your own function all along.

You *cannot* apply `using namespace` to types.

```cpp
#include <iostream>

struct T
{
    int value;
    static void f()
    {
        std::cout << "T::f" << std::endl;
    }
};

int main()
{
    // Doesn't compile
    using namespace T;
    f();
    return 0;
}
```


### Resolving name collisions

If you've included two namespaces that have the same function declaration,
you won't be able to call the function without qualifying it.

```cpp
namespace A
{
    void f()
    {
        std::cout << "A";
    }
}
namespace B
{
    void f()
    {
        std::cout << "B";
    }
}

int main()
{
    using namespace A;
    using namespace B;

    // Which one do I call, bro? A::f or B::f?
    f();

    // You have to disambiguate by qualifying the name.
    A::f(); // A
    B::f(); // B
}
```

A similar situation where a name collision takes place between a function from the global scope
and a function from a used namespace can be resolved analogously:

```cpp
namespace A
{
    void f()
    {
        std::cout << "Hello";
    }
}
void f()
{
    std::cout << "World";
}

int main()
{
    using namespace A;

    f(); // nonsense!
    A::f(); // Hello
    ::f(); // World

    return 0;
}
```


### `using` for name aliasing

Another very useful use for `using` is to give a type another name.
It is largely equivalent to `typedef`, but `using` is a bit more intuitive, 
so it is recommended to use `using` over `typedef`.

> `typedef` doesn't work with templates, `using` does.


```cpp
namespace Long::Namespace::Name
{
    struct Outer
    {
        struct Inner
        {
            struct Target
            {
                int x;
            }
        }
    }
}
int main()
{
    using T = Long::Namespace::Name::Outer::Inner::Target;
    // same as
    // typedef Long::Namespace::Name::Outer::Inner::Target T;

    T t{15};
    std::cout << t.x; // 15

    return 0;
}
```

```cpp
enum class Color
{
    Red = 'r',
    Green = 'g',
    Blue = 'b',
};

int main()
{
    using C = Color;
    C color = C::Red;

    switch (color)
    {
        case C::Red:
            std::cout << "Red";
            break;
        case C::Green:
            std::cout << "Green";
            break;
        case C::Blue:
            std::cout << "Blue";
            break;
    }

    return 0;
}
```

You can use `namespace X =` syntax for the same thing with namespaces.

```cpp
namespace Hello::World::Long::Namespace::Very::Long
{
    void func()
    {
    }
}

int main()
{
    namespace NS = Hello::World::Long::Namespace::Very::Long;
    NS::func();
}
```

## `enum` and `enum class`

`enum` allows you do define named compile-time constants in a straightforward way.

### The concept of an enumeration

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

### `enum class`

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


### The base type

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

## Polymorphism

*Polymorphism* means that a single function name can refer to different functions,
depending on some context.
It is one of the most important programming concepts, 
which enables some really powerful techniques.

### Static polymorphism (function overloading)

I've already kind of glossed over this idea in the `template` section.
It refers to declaring multiple functions with the same name, but a different
number of parameters / parameter types.

```cpp
void f(int a)
{
    std::cout << "int";
}

void f(float a)
{
    std::cout << "float";
}

int main()
{
    f(5); // int
    f(5.0f); // float
    return 0;
}
```

There really isn't much beyond this.
The key idea to understand is that the same name `f` refers to multiple functions,
and which function exactly is called is decided based on the context -- the type of the argument. 

Note that C, in contrast to C++, does not have function overloading.
In C, in order to implement the same functionality, 
you would have to give the functions different names.
Usually, the names are prefixed with the type of the argument (in some way).

```cpp
void f_int(int a)
{
    std::cout << "int";
}

void f_float(float a)
{
    std::cout << "float";
}

int main()
{
    f_int(5); // int
    f_float(5.0f); // float
    return 0;
}
```

It turns out more explicit on the caller site, 
which function overloading strives to eliminate.
If the program already has the type information,
based on which it can decide which function to call,
why would you want to repeat it again every time you want to call the function?
That's basically the idea.


### Function pointers

The idea here is to call the function by its address,
stored in a pointer variable.

You can use it to implement a rudimentary form of the strategy pattern.
It's not as powerful as the iterator pattern when it comes to collections,
but it can still be used in this context.
You can also compound the two together to create an abstraction over loops.

See [the example](./polymorphism/strategy_func_pointer.cpp).

You can use this idea to assign behavior to things.
Imagine wiring up a certain function to be called when a button is pressed.  
See [an example](./polymorphism/button_func_pointer_example.cpp).

Sure, you could achieve that with a `switch`. 
But what if the main function doesn't or shouldn't know about 
all of the possible functions?
Like in the [following example](./polymorphism/button_func_pointer_decentralized.cpp).
This can easily happen, if you want to keep the actual functions in some other module
as static, and only expose a function that would add these internal functions to the list.
You could never achieve something like this with a switch,
without exposing the internal functions.

```cpp
// main.cpp
#include "math_functions.h"
// ...
addMathFuncs(functionList);
```

```cpp
// math_functions.h
void addMathFuncs(std::vector<ButtonFunc>& functionList);
```

```cpp
// math_functions.c
static void add()
{
    // ...
}

static void subtract()
{
    // ...
}

void addMathFuncs(std::vector<ButtonFunc>& functionList)
{
    functionList.push_back(add);
    functionList.push_back(subtract);
}
```

### Passing private state to the function

When using function pointers,
the one issue that you'll have is that you can't pass data to it.
If you want a function that adds 5 to each number of the array, you're fine,
but if you want one that adds N to each number of the array,
you simply can't do this by passing a parameter.

```cpp
void add5(int& a)
{
    a += 5;
}

void addN(int& a, int n)
{
    a += n;
}

// ...

// Totally fine
forEachItem(list, add5);

// Not possible
int increment = 5;
forEachItem(list, addN(???, increment));
```

Sure, you can kind of solve this by using global variables,
but don't, because that's a bad idea.
It makes for an inflexible and messy program.
Sure, if `forEachItem` only accepted function pointers, you'd have no choice,
but if you can change `forEachItem`, you can do better.

What we want is to allow the user to pass *custom context* to the function,
meaning some additional data that the function needs to do its thing. 
A simple enough solution would be to add a template parameter for the context type,
and pass it together with the function pointer.

See [the example](./polymorphism/func_with_context.cpp).
It has a few issues, like not being able to easily make a `const` overload,
without duplicating all of the code, but don't worry about that too much.
The other issue is that different functions might require different context types,
so the polymorphism is basically back to being static here,
but by the context type, rather than the function. 


### `void*` as the context type (type erasure)

The special thing about `void*` is that it can be used to store a pointer to anything,
which means you can pass any context type with it.
The only issue is that you'll have to make sure you pass the right thing,
and cast it back in the function on the receiving end, so it's pretty fragile.
See [the example](./polymorphism/func_void_pointer_context.cpp).

Also, since some context might be smaller than a pointer, 
we could store it directly, instead of the pointer.
We can do this by passing in a `uintptr_t` instead
and then casting it to the expected type, which will either be a pointer, 
or the value type. 
See [an example](./polymorphism/pointer_value_union_small_example.cpp).


### Templated state and function in one (functors)

This is another approach to static polymorphism, with context passing.
The idea is that you can unify the context and the function into a single type,
by making the function you want to call into a member function of that type.
See [the example](./polymorphism/functor_custom_name.cpp).

In order to be able to reliably call the method from the templated
definition, you have to decide on the name that the function should have.
C++ selected the *invocation operator `operator()`* for this,
because with that you are now able to pass function pointers as functors.
See [the example](./polymorphism/functor.cpp).

Note that for each new type that you pass into `forEachItem`,
a new copy of the function will be created in the final executable
(unless trimmed / merged into an existing definition / optimized away).
This most of the time isn't something you should be concerned about,
but especially large function could bloat your executable (aka make it way too large),
because of which using a more dynamic approach could be more reasonable.

Functors is an idea that is very often used by functions in 
e.g. the `algorithm` module of the standard library,
which works with iterators as well.


### Lambdas

Lambdas allow us to define functions without naming them (anonymous functions),
potentially inside the scope of another function,
and creating the functor type automatically, which is done by the compiler.

#### Without context

To define a lambda function without context,
which would be equivalent to a regular free function 
(a regular function in the global scope), 
you use [the following syntax](./polymorphism/lambda_1_void.cpp).
You can pass it directly as a parameter to other functions 
that accept a function pointer as well.

#### Private context

To define the private context of the function,
you put the parameters of the lambda in the square brackets (called the *capture group*).
*Copies* of whatever variables you put in the square brackets 
will be accessible in the function.
Under the hood, the compiler creates a functor type,
and those variables become private fields in that type.
See [the example](./polymorphism/lambda_2_context_copy.cpp).

> Note that `mutable` is required if the function wants 
> to change the value of its context.
> It adds `const` to the generated `operator()` method,
> so it follows the regular `const` rules of references vs values.

The act of copying the variables is called *capturing*.

#### Sharing the context

You can also capture by reference, 
by prepending `&` to the variable name in the capture group.
This way you can share context between multiple lambdas.
See [the example](./polymorphism/lambda_3_shared_context.cpp).

You can mix the capture types.
```cpp
int a = 1;
float b = 8;
auto func = [&a, b]() mutable {
    a += 5;
    b *= 10;
};

func();

assert(a == 6);
assert(b == 8); // `b` was copied by value
```

And have multiple captures of the same type:
```cpp
int a;
float b;
auto func = [&a, &b]() mutable {
    a += 5;
    b *= 10;
};
```

#### Passing lambdas to templates

For example, in [this example](./polymorphism/functor.cpp), 
you can pass lambdas to the function:
```cpp
// `a` is a reference here.
forEachItem(values, [&a = values[0]](float& value){ value *= a; });

// or store the address (`a` is a pointer here)
forEachItem(values, [a = &values[0]](float& value){ value *= *a; });
```

#### Dangling references

Be careful with capturing by reference,
because you can easily end up with dangling references,
if you try to return the functor having by-reference 
captures to local variables from a function.

```cpp
auto createBadFunctor()
{
    int localVariable{5};
    return [&localVariable](){ return localVariable; };
}

int main()
{
    auto func = createBadFunctor();
    func(); // references deleted memory -- undefined behavior
    return 0;
}
```

#### Capturing everything

You can capture everything visible in the current scope
by value with `[=]` or by reference with `[&]`.

```cpp
int a = 1;
int b = 2;
{
    auto func = [=]() mutable {
        a += 5;
        b *= 10;
    };
    func(); // a = 1, b = 2
}
{
    auto func = [&]() {
        a += 5;
        b *= 10;
    };
    func(); // a = 6, b = 20
}
```

You can also use `&` or `=` to set the default,
and then overwrite it for specific variables:

```cpp
int a = 1;
int b = 2;
// The default is &, but `a` is to be copied.
auto func = [&, a]() mutable {
    a += 5;
    b *= 10;
};
func(); // a = 1, b = 20
```

The variables will only be captured if they are used in the lambda.
That is illustrated [here](./polymorphism/lambda_4_functor_sizes.cpp).


### A little foreword: function types

It's kind of mind-bending, but function declarations have types in this language.
The syntax is like with the function pointer types, but without the `(*)`:

```cpp
using FuncType = void(int, int);
FuncType f; // declaration
void f(int a, int b); // an equivalent declaration
void f(int a, int b) { } // definition
```

Similar to variables, you can have function references:

```cpp
using FuncRefType = void(&)(int, int);
void f(int a, int b) { }
FuncRefType g = f;
```

Or, with `decltype`:

```cpp
void f(int a, int b) {}
decltype(f)& g = f;
```


### `std::function`

`std::function` is introduced by the documentation 
as a *general-purpose polymorphic function wrapper*.
The idea of `std::function` is to be able to assign any function, or functor
to it, potentially capturing its context, and then be able to call it later.

It's a really powerful type, which effectively allows you 
to implement dynamic polymorphism in a very flexible way,
which means you can pass it to functions without it having 
a template parameter for the functor.

To be noted that `std::function` is an RAII type and may allocate dynamic memory.

`std::function` truly implements dynamic polymorphism,
which implies that it won't lead to code bloat, mentioned previously,
but it will lead to a runtime overhead when calling the function
(just as it's slower to call a function via a function pointer rather than directly,
it is slower to call a functor via an `std::function` rather than directly).

See [an example](./polymorphism/std_function.cpp),
which illustrates working with `std::function` 
with up to two levels of indirection, using both lambdas and functors,
and provides an example of how to move things into lambdas.


### Passing multiple functions (vtable, fat pointers)

If your function has to call more than one function,
passed as an argument, you can use your existing knowledge to
figure out how to do that.
A potential implementation would be:

```cpp
using IntroductionFunc = void(*)();
using SumFunc = int(*)(int a, int b);

struct Behavior
{
    PrintFunc introduceOneself;
    SumFunc answer;
};

void test(Behavior& behavior)
{
    behavior.introduceOneself();
    int answer = behavior.answer(5, 6);
    std::cout << answer << std::endl;
}

int main()
{
    Behavior dumbCat{
        [](){ std::cout << "Meow" << std::endl; },
        [](int a, int b){ return 0; },
    };
    Behavior smartDog{
        [](){ std::cout << "Woof" << std::endl; },
        [](int a, int b){ return a + b; },
    };
    test(dumbCat); // Meow, 0
    test(smartDog); // Woof, 11

    return 0;
}
```

You can imagine a similar implementation with `std::function`, 
which will allow you to capture some context in each function as well.

Now, what do would we do if we wanted both the functions to share the same context,
and we also wanted dynamic polymorphism (we need functions to be either function pointers
or `std::function`)?
Sure, you could share the context in the `std::function`s, but that's kind of wasteful.
We would end up storing the context's memory somewhere, and then we'd have to store 
a reference to it in each of the functions.
We could avoid storing the pointers by just passing the context manually.

A solution which does what we want is to use `void*` for the context.
Sure, it is clunky, and dangerous, but it does what we want.
What we do, is we would pass the context pointer together with 
a pointer to the struct with the functions, 
which is also called a *virtual table* or a *vtable*.
The reason why we use a pointer to the vtable, rather than the vtable itself,
is simply because we want to use the same vtable for multiple contexts.
See [the example](./polymorphism/fat_pointer.cpp).

> This is basically how Rust does dynamic polymorphism.


### Multiple virtual tables

Assume we wanted to have multiple vtables.
Let's say we want to use a vtable for greetings
(methods like `introduceSelf` when greeting and `excuseSelf` when leaving),
and another vtable for computing answers to questions
(like `computeSum` and `writeCppProgram`).

Sure, we could do this by using fat pointers, 
but *virtual inheritance* in C++ takes a different approach.
Instead, they *modify the pointer*, 
adjusting it to be looking at the method table, 
rather than the start of the object,
and *store the offset to the start of the object data in the vtable*,
to be able to get at the context.

See [the example](./polymorphism/multiple_vtables_cpp_approach.cpp).

I'm not going to force you to understand the code thoroughly,
but if you do want to understand the topic, be sure to learn it.
Here's [a video](https://youtu.be/QzJL-8WbpuU) I've been suggested too.


### Pure abstract base classes and virtual functions

The method table idea that I have described and implemented previously
is available as a primitive in C++.

> It may not be exactly the same my implementation, but it uses some very similar ideas.

To define the layout of a vtable, you can define a *pure abstract base class*
with *virtual* methods, set to `0`, meaning "unimplemented".
Another name for this is an *interface*.

```cpp
class GreetingAbstractBase
{
public:
    virtual void introduceSelf() = 0;
    virtual void excuseSelf() = 0;
};
```

You can then *inherit* these in a class with your context,
and *override* the methods.
This will initialize the vtables, and add an implicit pointer field
to each of them in your *derived* class (the one that inherits).

```cpp
class Person : 
    public GreetingAbstractBase,
    public QuestionAbstractBase
{
    // ...

    void introduceSelf() override
    {
        // ...
    }

    // ...
}
```

The conversion syntax and the call syntax are then way simpler,
it is a language primitive after all.

```cpp
Person person;

Person* personPtr = &person;
GreetingAbstractBase* greetingPtr = personPtr;
QuestionAbstractBase* questionPtr = personPtr;

// The pointers look at different memory.
assert(static_cast<uint8_t*>(greetingsPtr) - static_cast<uint8_t*>(questionPtr) != 0);

// The context is adjusted and passed implicitly.
greetingPtr->introduceSelf();
```

It is less flexible than fat pointers,
because it marries the data (the context) to the methods, 
but it is convenient due to the simpler syntax,
so you might find yourself using it anyway.

In general, prefer using `std::function` 
instead of interfaces when you only need a single method.
Otherwise, interfaces are a good choice.
But, of course, before you do, consider if you really want dynamic polymorphism at all.

See [an example](./polymorphism/abstract_base_class.cpp)
