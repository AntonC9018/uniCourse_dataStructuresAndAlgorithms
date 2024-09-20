 Namespaces

We have already met with type scopes, which have the namespace concept built into them.
However, if you want a language primitive which just provides the namespace concept,
you can use `namespace`.

## Basic usage

A namespace basically means a scope that can house functions, variables, types and other namespaces,
and can be used to avoid name collisions among these.

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


## Namespaces allow you to use things from the namespace without qualification

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

## Shortcutting with the `::` operator

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

## The global scope

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


## `using namespace`

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


## Resolving name collisions

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


## `using` for name aliasing

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

