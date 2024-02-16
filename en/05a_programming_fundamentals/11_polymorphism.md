# Polymorphism

*Polymorphism* means that a single function name can refer to different functions,
depending on some context.
It is one of the most important programming concepts, 
which enables some really powerful techniques.

## Static polymorphism (function overloading)

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


## Function pointers

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
include "math_functions.h"
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

## Passing private state to the function

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


## `void*` as the context type (type erasure)

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


## Templated state and function in one (functors)

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


## Lambdas

Lambdas allow us to define functions without naming them (anonymous functions),
potentially inside the scope of another function,
and creating the functor type automatically, which is done by the compiler.

### Without context

To define a lambda function without context,
which would be equivalent to a regular free function 
(a regular function in the global scope), 
you use [the following syntax](./polymorphism/lambda_1_void.cpp).
You can pass it directly as a parameter to other functions 
that accept a function pointer as well.

### Private context

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

### Sharing the context

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

### Passing lambdas to templates

For example, in [this example](./polymorphism/functor.cpp), 
you can pass lambdas to the function:
```cpp
// `a` is a reference here.
forEachItem(values, [&a = values[0]](float& value){ value *= a; });

// or store the address (`a` is a pointer here)
forEachItem(values, [a = &values[0]](float& value){ value *= *a; });
```

### Dangling references

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

### Capturing everything

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


## A little foreword: function types

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


## `std::function`

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


## Passing multiple functions (vtable, fat pointers)

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


## Multiple virtual tables

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


## Pure abstract base classes and virtual functions

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
