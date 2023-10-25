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

You can make an operator that is allowed to be used implicitly unusable,
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
See the examples code [here](./vector/procedural.cpp) and [here](./vector/operator.cpp).


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

To be noted, that `std::ostream` overloads the `<<` operator for some of the fundamental types,
like `const char[N]`, `int`, `float`, etc, which is how you're able to use `<<` for printing.
And you're able to use it fluently (chain operators) 
because it returns a reference to the same stream object.