# Abstraction and Encapsulation

## Implementation files (cpp)

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
include "f.cpp"

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


## Sharing declarations

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


## The interface

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


## Avoiding duplicate declarations

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


## Circular includes

These are not allowed, because files are only ever included sequentially.


## `private` fields

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


## `private` members in the header file

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

