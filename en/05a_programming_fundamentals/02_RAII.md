# Scopes

Scopes have two functions in C++:
- They serve to make variables not visible outside of them;
- They are used to clean up memory ("resources") of objects.
  This can be achieved by using destructors.

You can say that scopes allow you to control the lifetimes of objects.

## Scopes for limiting the visibility

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


## Scopes for cleaning up resources

Conceptually, a variable defined in a scope is destroyed at the end of the scope.
For simple types like int, it means literally nothing.
For a complex type, like `std::string`, this means 
returning the memory allocated for the character array to the C++ runtime.


## Destructor 

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


## Implicit destructors

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

# Constructors

Constructors are special `void` functions used to initialize objects.
Constructors cannot be called in any other context.

Constructors were created to allow initializing private data members (fields) in OOP.
Constructors can be more involved than that, but it's generally discouraged to make them complex.

## Constructors used to initialize new objects

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

## Breaking the code above

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


## Copy constructors

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


## Moving an object

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


## Move constructors

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

## Return value optimization (RVO)

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

## lvalue and rvalue

*lvalue* means a value that appears on the left hand side of an assignment.
This is equivalent to saying that *an lvalue is a value that has storage*, meaning it is stored in some memory.

An *rvalue* may not have any storage, but be a temporary value.
rvalues appear on the right hand side of an assigment.


```cpp
int a;

// a is an lvalue, 5 is an rvalue
a = 5;

int b;

// b is lvalue, a is rvalue
b = a;

std::vector<int> vec;
// vec is lvalue, {} is rvalue
vec = {};
```

*rvalue references* are denoted as `T&&`, which means that it's a temporary object, whose value won't be used later.
You can force an object to be treated like an rvalue reference by using `std::move`.

```cpp
std::vector<int> a{};
a.push_back(5);

{
    // This makes a copy of a in t
    std::vector<int> t{ a };
    a[0] = 6;
    assert(t[0] == 5);
    assert(a[0] == 6);
}
{
    // a becomes empty, now t posesses the memory that was previously pointed at by a
    std::vector<int> t{ std::move(a) };
    assert(a.size() == 0);
    assert(t[0] == 5);
}
```

It can be used to avoid making copies.
In the example below, only one copy of the strings *Test* and *Magic* will be created.

> Note that you shouldn't see a difference in the memory usage due to small string optimization,
> but if the strings are large enough, it will be copied into dynamically allocated memory more times than required.

```cpp
void addBook(Book&& book)
{
    *someMemory = std::move(book);
}

// ...

Book temp;
temp.author = "Test";
temp.title = "Magic";
addBook(std::move(book));
assert(temp.author == "");
```
