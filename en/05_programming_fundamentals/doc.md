## Variables

A *variable* represents a memory location with a name.
The computer will allocate (provide) this memory location when our program is executed.

### Types

Each variable has a *type* associated with it. 
For now think of a type as a conceptual name that defines the number of bytes of memory
that will need to be allocated for the variable.
For example, the type `std::byte` means this size will be 1 byte of memory, 
and `int` is (typically) 4 bytes, 
and a `size_t` is (typically) 8 bytes.

### Declaration

To **declare** a variable (make the computer allocate memory for it, and name that memory in the source code),
we need to type in the type and a the variable name (of what it's supposed to represent).
For example:

```cpp
// Declare an int, aka allocate 4 bytes of memory and name it "i"
int i;
// Declare a byte, aka allocate 1 byte of memory and name it "myByte"
std::byte myByte;
```

### Initialization

You also need to initialize the variable, which means write a value into the memory of that variable.
By default any variable's memory is "unititialized", which means it will contain whatever was in that memory previously, which in practice can be anything
(this is often called "garbage" or "garbage data").
Typically what you do is you should immediately "zero out" the value, if you're going to use it later.
Zeroing the value means writing a zero into each byte of the memory of the variable.
The way you do this in C++ is you assign `{ }` (you can use 0 as well if it's a number type, like int).

### Definition

Declaring and initializing a variable together is also named defining a variable.
But since variables are initialized by default (with garbage, but still in effect initialized), 
any variable declaration is also its definition.

```cpp
// Define an int, and fill all 4 bytes with zeros.
int i = 0;
// Same thing
int number = { };

// Define an int, and set the 4 bytes to contain 42.
// This will correctly set the bit pattern of the 4 bytes to represent 42 in base 2.
// Each byte's value in base 10: 0 0 0 42
// And now it in base 2: 00000000 00000000 00000000 00101010
int someNumber = 42;

// Declare an int, then initialize it separately.
// In between the declaration and the initialization, the variable will contain garbage data.
// ... Declaration
int g;
// ... Initialization
g = 10;
```

### Assignment

Initializing typically refers to the first time you write a value into a variable.
But in principle you can overwrite the value of a variable as many times as you want.
This is called **assignment** and the act of setting the value is called **assign**.

```cpp
// Define a few numbers
int a = 5;
int b = 10;
int c = 20;

// Define a variable to store the sum, initialized to 0.
int sum = 0;
// Add the value of each variable to the sum.
sum = sum + a; // 0 + 5 = 5
sum = sum + b; // 5 + 10 = 15
sum = sum + c; // 15 + 20 = 35
```

## Arrays

An arrays is a contiguous block of memory, where each element of the array has the same type
(aka occupies the same number of bytes).
You can think of arrays as a group of variables, where each variable is named by its index in the array.

To visually understand how it's laid out in memory, check out [memory_example_1](./memory_example_1).

```cpp
// Declares an array of 5 ints, aka 5 * 4 bytes = 20 bytes.
// This effectively means that we declare 5 variables of type int,
// and they have the names array[0], array[1], array[2], array[3], array[4].
int array[5];

std::byte array[2];
```

### Array indexing

Arrays are indexed starting from 0, so the first element is `array[0]` and not `array[1]`.
Think of the index as the offset, counted in the size of the type of each element,
from the start of the memory of the array.

In the ascii table below is represented the first 12 bytes of the memory of an `int` array.

```
address:          0 1 2 3   4 5 6 7   8 9 10 11 ... 
bytes graphic:  | _ _ _ _ | _ _ _ _ | _ _ _ _ | ...
offset (index): 0         1         2         3 ...
```

You can use the array element e.g. `array[0]` as any other regular variable:
you can assign to it, read from it, zero it out by assigning `{ }`.

But one of the more useful things with arrays is that you can use an non-constant index.
For example:

```cpp
int array[3] = { };

size_t index = 2;
// Sets array[2] to 69.
array[index] = 69;

size_t otherIndex = 1;
// Sets array[1] to 420.
array[otherIndex] = 420;
```

This can be useful when you get the index from somewhere else, 
like from user input, or just another function.


## Pointers

> [Video](https://www.youtube.com/watch?v=2ybLD6_2gKM)

If you understand memory addresses, you pretty much understand pointers.
A pointer is a variable that stores a memory address.
For an example of how a pointer is stored in memory, check out [memory_example_1](./memory_example_1).

```cpp
int someNumber = 1;
// Declare a pointer that has the memory address of `someNumber`.
// The & operator is called "address of" and it 
// returns the memory address of the variable it is used on.
int* pointerToSomeNumber = &someNumber;
```

### Sizes, addresses and `size_t`

The type of the pointer defines what type of variable the address points to,
however, this type does not affect the size of the address itself.
An address of a variable of any type is always the same size,
which is either 8 bytes (64 bit) on 64-bit architectures,
or 4 bytes (32 bit) on 32-bit architectures.

> Now technically it could be anything, but in 99.9% of cases it's one of those to.
> For the purposes of furthering the discussion, assume it's 8 bytes.

The special type `size_t` indicates the maximum length in bytes of a block of memory.
It is also the same as the address size, on most architectures.
It's usually used for indices or lengths of arrays.

The type that can store any pointer is `uintptr_t` and 
it will be the same size as `size_t` for all modern processors used in personal computers.

We can retrieve the numerical value of an address by converting it to a `uintptr_t`.
Converting from one type into another is called "casting".

```cpp
int someNumber = 1;
int* pointerToSomeNumber = &someNumber;
// Cast the pointer to a uintptr_t, by interpreting the memory address stored in there as a number.
uintptr_t addressOfSomeNumber = (uintptr_t) pointerToSomeNumber;
```

### Dereferencing

"Dereferencing" means getting the value from the address stored in a pointer.

In other words, it means:

1. Get the address stored in the memory of the pointer variable;
2. Go to that address in memory;
3. Read the value from that address.

```cpp
int value = 0;
int* pointerToValue = &value;

// Dereference the pointer, aka get the value from the address stored in the pointer.
// `valueFromPointer` will be equal to 0.
int valueFromPointer = *pointerToValue;

value = 10;

// Dereference the pointer again, aka get the value from the address stored in the pointer.
// `valueFromPointer` will remain equal to 0 
// (because it's a copy of the earlier value, stored in the memory of valueFromPointer)
// but `otherValueFromPointer` will be equal to 10 (as read from `value`).
int otherValueFromPointer = *pointerToValue;
```

### Writing to a memory address

This operation is different from dereferencing, even though it has the same syntax.
It means writing a value in the memory at the address that's stored in the pointer.

In other words:

1. Get the address stored in the memory of the pointer variable;
2. Write to that address in memory.

```cpp
int value = 0;
int* pointerToValue = &value;

// `value` becomes equal to 10.
*pointerToValue = 10;
```

### Pointer inception

Pointers can point to other pointers, indefinitely.
A pointer to a pointer means that the first pointer 
stores the memory address of where the other pointer's memory is,
that is, where it stores the address of the variable it points to.

These are occasionally useful, but are rarely used in their raw form.
Double or even triple indirection (dereferencing pointers multiple times in the program)
is very common, but it's usually hidden under a clearer abstraction.
Pointers to pointers are hard to think about in their raw form. 
If you feel that way, know that it's normal.

```cpp
int value = 0;
int otherValue = 5;
int* pointerToValue = &value;
int** pointerToPointerToValue = &pointerToValue;

// We can retrieve the `pointerToValue`'s value, so the address stored in its memory,
// by dereferencing `pointerToPointerToValue`.
int* anotherPointerToValue = *pointerToPointerToValue;

// Now we can write to `value` by writing to `*anotherPointerToValue`.
// So this will set `value` to 10.
*anotherPointerToValue = 10;

// Let's now point `pointerToValue` to `otherValue`.
pointerToValue = &otherValue;

// This gives 5.
int valueOfOtherValue = *pointerToValue;

// But this still has the old address of `value`, so it reads 10.
int valueOfValue = *anotherPointerToValue;

// But dereferencing the `pointerToPointerToValue` twice gives us the new address of `otherValue`.
int valueOfOtherValueAgain = **pointerToPointerToValue;
```

> Quiz time: how many bytes does the type int** occupy?
 
<details> 
<summary>Response</summary>
`uintptr_t` (typically 8 bytes), just like any other memory address.
</details>


### `void*`

The type `void*` is a special type of pointer that can point to any type of variable.

```cpp
int value = 0;
std::byte otherValue = 5;

// Store the address of `value` in a `void*`.
void* pointer = &value;

// This line won't compile (void* can't be dereferenced).
// int valueFromPointer = *pointer;

// But we can cast it to an int* first, and then dereference, which will work.
int* typedPointer = (int*) pointer;
int valueFromPointer = *typedPointer;
// or as a single operation
int valueFromPointer = * (int*) pointer;
```

### Pointers into arrays and pointer arithmetic

> [Video](https://youtu.be/q24-QTbKQS8). 
> It's in C, so the syntax is a tiny bit different with structs.

Just like with any other variable, you can point a pointer to an element in an array.

```cpp
int array[3] = { 1, 2, 3 };

// Point to the first element of the array.
int* pointerToArray = &array[0];
// Point to the second element of the array.
int* pointerToArray = &array[1];

int i = 2;
// Pointer to some i-th element of the array.
int* pointerToArray = &array[i];
```

You can also add and subtract numbers from pointers to navigate blocks of memory (like arrays),
in increments of the size of the type of the pointer.

```cpp
int array[3] = { 1, 2, 3 };

// Point to the first element of the array.
int* pointerToArray = &array[0];
int value1 = *pointerToArray; // 1

// Navigate to the second element.
// Note that +1 changes the address not by a single byte, but by 4 bytes in this case.
pointerToArray = pointerToArray + 1;
int value2 = *pointerToArray; // 2

// Go back to the first element
pointerToArray = pointerToArray - 1;
int value3 = *pointerToArray; // 1

// Navigate to the third element by skipping over the second one.
pointerToArray = pointerToArray + 2;
int value4 = *pointerToArray; // 3
```

A `void*` acts as an `std::byte*` when doing pointer arithmetic, that is to say,
it navigates memory in increments of 1 byte.

Another thing that needs to be mentioned is that you can subtract 
two pointers to get the number of items in between them.

> `ptrdiff_t` is a signed variant of `size_t`.

```cpp
int array[3] = { 1, 2, 3 };
int* pointerToArray0 = &array[0];
int* pointerToArray2 = &array[2];
ptrdiff_t numberOfItems = pointerToArray2 - pointerToArray0; // 2
ptrdiff_t negativeNumberOfItems = pointerToArray0 - pointerToArray2; // -2
```

If you want to find out the difference in bytes between two pointers,
you can cast them to `std::byte*` or `uintptr_t` or `ptrdiff_t` first.
Also, you cannot subtract two `void*`, or pointers of different types, unless you cast them first.

> The best way is probably `std::byte*`, because it won't cause any weirdness with signedness.
> When subtracting a `uintptr_t`, you have to be certain the left one is bigger,
> and casting to `ptrdiff_t` loses one bit of information (the sign bit).
> Subtracting types other than `std::byte*` for pointers very quickly gets into the territory of
> "is overflow or underflow defined for this type, or is it undefined behavior?",
> which it's better to just avoid.

```cpp
int array[3] = { 1, 2, 3 };
int* pointerToArray0 = &array[0];
int* pointerToArray2 = &array[2];

uintptr_t numberOfBytes = (uintptr_t) pointerToArray2 - (uintptr_t) pointerToArray0; // 8
// or
ptrdiff_t numberOfBytes = (ptrdiff_t) pointerToArray2 - (ptrdiff_t) pointerToArray0; // 8
// or
ptrdiff_t numberOfBytes = (std::byte*) pointerToArray2 - (std::byte*) pointerToArray0; // 8
```

Adding two pointers is not allowed either 
(it doesn't really make a whole lot sense why you'd do that, if you think about it).

> Note that subtracting pointers is only allowed by the C++ standard 
> if they point to elements in the same array / block of memory.
> Otherwise it's undefined behavior (anything can happen, don't rely on it).

## Functions

Functions are blocks of code that can be executed from other places in the program.
In instruction terminology, a function is a sequence of instructions, 
which have an address at which they start in the executable file.
To be clear, each instruction in executable files has an address, which is,
just like the memory, the position of the instruction in the file, with some base offset (say, 100).
This offset can vary on distinct runs of the program, but the relative positions of the instructions
in the file will always be the same.

> TODO: someone should fact check this, I'm just relaying my understanding of it,
> I might be somewhat wrong in the details.

When you call a function in code, the processor "jumps" to the address of the first instruction
of the function, and starts executing instructions from there.
When the function is done executing, the processor "jumps"
back to the instruction after the one that called the function.

Executing a function is called "calling" or "invoking" a function,
and coming back from a function after it's finished executing, is called "returning" from a function.
It is said that the function that you had called "returns".

### The `main` function

The function named `main` is a special function that is called automatically when the program starts.
It's called the entry point of the program.

> Don't worry about the `include`, the `int`, or the `return 0;` for now.

```cpp
#include <iostream>
int main()
{
    // Prints "Hello" to the console when executed.
    std::cout << "Hello";
    return 0;
}
```

> `return 0` indicates success, while returning any other value indicates a failure.

### Prototypes

A **prototype**, also called a signature in other languages, is a description of the interface of a function.
It describes what "parameters", or inputs, the function takes, and what it "returns", or outputs.

You can think of a function at a high level as a factory:

- It takes in something (parameters), like steel and plastic;
- It does some operations with it;
- Out comes something else (return value), like a car.

You're probably familiar with the math notation $` f(x, y, z) \rightarrow \mathbb{Z} `$, which says:

- The function is named `f`;
- It takes parameters `x`, `y`, and `z`;
- It returns some value, that is a whole number (`Z`).

Note that in this math notation the types (which values they may have)
of the parameters are often implied by the context,
but they can also be specified explicitly separately,
like right here: $` f(x, y) \rightarrow \mathbb{Z}, x \in \mathbb{Z}, y \in \mathbb{Z} `$.

The same thing happens in C++.
Any function has a return type, a name and a list of parameter, where each one has a name and a type.

For example, if we approximate $` \mathbb{Z} `$ with `int`, we can declare this function in C++ like this:

```cpp
int f(int x, int y);
```

This is called a function prototype, or a function signature.

Here we declare a function that returns some pointer, and takes in a pointer to an int, and an int.

```cpp
void* getSomePointer(int* pointer, int someInt);
```


### Procedures

A procedure means a function that doesn't have a return type,
or doesn't return anything, in the usual sense of the word.
It may still affect the memory of the caller via its parameters,
like changing the value by using a pointer passed as a parameter.
It may also produce a visible side effect, like printing to the console.

You mark the return type of a procedure as `void` to mean "no return type".

```cpp
// Here's a procedure that just prints hello to the console.
// (produces a side effect)
void printHello()
{
    std::cout << "Hello";
}

// Here's a procedure that takes in a pointer to an int,
// and writes a value to it.
// (affects memory of the caller)
void writeValue(int* pointer)
{
    *pointer = 10;
}
```


### Function declaration

Functions are analogous to variables, in that they have a declaration and a definition.
However, unlike variables, functions are not initialized with garbage by default like variables,
they are simply unusable as just a declaration, unless a definition is also provided somewhere in the program.

For example, the following program will fail to compile with a linker error,
due to `add` missing its definition.

```cpp
int add(int a, int b);

int main()
{
    int c = add(1, 2);
    return 0;
}
```


### Function definition

A function definition is the actual implementation of the function.
It is also called the body of the function.

In the above example, if we defined the body of `add` (what instructions it should do),
the program would compile and run correctly.

```cpp
// declaration
int add(int a, int b);

// definition
int add(int a, int b)
{
    return a + b;
}

int main()
{
    int c = add(1, 2);
    return 0;
}
```

We can put the definition anywhere in the program.

> As long as there's only one definition.
> It may happen that you have multiple definitions of the same function,
> in cases where you define the same function in multiple source files,
> and then try to link them together into a single executable.
> It will fail with a linker error, saying there's more than one definition.

```cpp
// declaration
int add(int a, int b);

int main()
{
    int c = add(1, 2);
    return 0;
}

// definition
// In this case, it's put after it's called in the file.
int add(int a, int b)
{
    return a + b;
}
```

The restriction is that the declaration must come before the function is called.
The following will *fail to compile*:

```cpp
int main()
{
    int c = add(1, 2);
    return 0;
}

// declaration
int add(int a, int b);
```

You can also combine the declaration with the definition, 
analogous to the way you do it with variables:

```cpp
// declaration + definition
int add(int a, int b)
{
    return a + b;
}

int main()
{
    int c = add(1, 2);
    return 0;
}
```


### The locals go on the stack

*insert explanation here*, sigh.

The [example 3](./memory_example_3) shows how the different kinds of memory work.


### Recursion (function inception)

*insert explanation here*, sigh.

The [example 4](./memory_example_4) shows how recursion works.


## Structs

Check out [memory_example_2](./memory_example_2) for an example of how structs are laid out in memory.

A struct is a means to group together multiple variables.
Formally, a struct is a custom datatype that a programmer can define.
Variables declared in a struct are called fields.

Below, we declare a struct that groups together two int variables, named `a` and `b`.

```cpp
struct TwoInts
{
    int a;
    int b;
};
```

And below we declare a struct "Car" to hold data about a car.

```cpp
struct Car
{
    Color color; // another custom struct, defined elsewhere
    int numberOfDoors; // an int
    int wheelLastChangedYear[4]; // an array of 4 ints
};
```

### Usage and the field access operator

To use a struct, you need to declare a variable of that type.
You can then access the fields of the struct by using the `.` operator.

```cpp
struct Point
{
    int x;
    int y;
};

int main()
{
    Point point;
    point.x = 10;
    point.y = 20;
    
    // 10 + 20 = 30
    int a = point.x + point.y;
    
    return 0;
}
```

The struct as a whole has the name `point`, and the variables within 
have the names `point.x` and `point.y` (their name in the declaration, prefixed with `point.`).
Think of the operator `.` as reaching into the memory of the whole point,
and grabbing the variable you want.


### Copying structs

The same way that you can have multiple variables of the same primitive type,
you can have multiple variables of the same complex type, e.g. `Point`.

```cpp
struct Point
{
    int x;
    int y;
};

int main()
{
    Point point1;
    point1.x = 10;
    point1.y = 20;
    
    Point point2;
    point2.x = 30;
    point2.y = 40;
    
    // 10 + 20 = 30
    int a = point1.x + point1.y;
    // 30 + 40 = 70
    int b = point2.x + point2.y;
    
    return 0;
}
```

You can also copy the points fully, one to the other.
This means copying all bytes, which will 
set the variables within one to their values within the other.

```cpp
struct Point
{
    int x;
    int y;
};

int main()
{
    Point point1;
    point1.x = 10;
    point1.y = 20;
    
    Point point2;
    point2.x = 30;
    point2.y = 40;
    
    // Copy point1 into point2.
    // sets point2.x to 10
    // sets point2.y to 20
    point2 = point1;
    
    // 10 + 20 = 30
    int a = point1.x + point1.y;
    // 10 + 20 = 30
    int b = point2.x + point2.y;
    
    return 0;
}
```


### Pointers to structs, and the `->` operator

You can also have pointers to structs, 
just like you can have pointers to any other type.

You can use the `->` operator to dereference a pointer to a struct,
and then access one of the fields.
You can think of `->x` as "go to the address of the pointer, then grab the local `x` variable".

```cpp
struct Point
{
    int x;
    int y;
};

int main()
{
    Point point;
    point.x = 10;
    point.y = 20;
    
    Point* pointerToPoint = &point;
    pointerToPoint->x = 30;
    // Equivalent to (*pointerToPoint).x = 30;
    
    // 30 + 20 = 50
    int a = point.x + point.y;
    
    return 0;
}
```

### Arrays of structs

You can also have arrays of structs.

```cpp
struct Point
{
    int x;
    int y;
};

int main()
{
    Point points[3] = { };
    points[0].x = 10;
    points[1].x = 20;
    points[2].y = 30;
    
    // 10 + 20 + 30 = 60
    int a = points[0].x + points[1].x + points[2].y;
    
    return 0;
}
```


### `sizeof`

The [`sizeof`](https://en.cppreference.com/w/cpp/language/sizeof) operator returns the size of a type in bytes.
It's useful for example when allocating memory with malloc.


## Linker and more on functions

### Compiler phases in short

Compiler is the program that can read the source code and produce an executable file with
machine instructions, which can be executed directly by the processor.

The process of compilation is split up into a few phases:

- Preprocessing, where the directives are expanded. 
  For examples, `#include "some_file.h"` is replaced with the contents 
  of `some_file.h` at this initial phase.

- Reading the source files by the compiler and the output of object files.
  Object files are the result of compiling a single `.cpp` source file after preprocessing 
  (also called a compilation unit).
  Object files contain the instructions for function *defined* in that file, information about
  which functions and global variables are defined, and which are only declared but not defined.
  
- The last phase is the linking phase. 
  Either a separate program or a subprogram included in the compiler, called the **linker**,
  takes all the object files and links them together into a single executable file.

### The function of the linker

The function of the linker is to *resolve references to functions and variables in between different compilation units*.
For example if we have a file `main.cpp` which declares and function and calls it:

```cpp
// main.cpp
int f(int a);

int main()
{
    int b = f(10);
    return 0;
}
```

And another file which provides the definition (the body) for `f`:
```cpp
// f.cpp
int f(int a)
{
    return a + 1;
}
```

It is the job of the linker to:
- Identify that `main.cpp` wants to call a function named `f`, which it doesn't have the definition for;
- Identify that `f.cpp` provides the definition for a function named `f`;
- Realize that it needs to *link* the definition from `f.cpp` to the declaration in `main.cpp`;
- Link the function definition from `f.cpp` to the function call in `main.cpp`;
- Produce an executable file that contains the instructions for `main.cpp` and `f.cpp` together.

> For a visual diagram of what's happening here, see the first example in [linker_examples](./linker_examples). 
> Be sure to read the readme in that folder as well.

Consider a broader picture of what happens when you compile a program: suppose you run the command
`zig c++ main.cpp f.cpp`, which will:
- Compile `main.cpp` separately getting the object file for it;
- Compile `f.cpp` separately getting the object file for it;
- Execute the linker on the two object files, producing an executable output file.

Also, if you want to view the intermediate object files, you can force zig to only compile them,
and then link them into an executable manually as a separate command:
```
# Compile main.cpp into main.o
zig c++ -c main.cpp -o main.o

# Compile f.cpp into f.o
zig c++ -c f.cpp -o f.o

# Link main.o and f.o into an executable
zig c++ main.o f.o -o main.exe

# Run the executable
.\main.exe
```

### `extern`

Variable declarations, as opposed to functions, are also definitions.
`extern` forces a variable declaration to stop being a definition.

In the context of the linker, being a global/non-static definition means 
that the function or the variable can be linked to from other files.
So `extern` basically makes the variable be "imported" from somewhere in the other file,
rather than defined in the current file.

Since function declarations are already not definitions, `extern` for these is redundant,
which is to say, it does nothing.

> See the 2nd example in [linker_examples](./linker_examples).

### `static` functions

`static` means that the function does not participate in linking.
This effectively means it can only be used in the compilation unit where it was defined.

> See the 4th example in [linker_examples](./linker_examples).

Two different static functions with the same name and parameters may be defined in multiple compilation units,
in which case all of them will end up in the executable, and they will all be treated
independently.


### `inline` functions

`inline` means that the instructions of the functions are going to be *inlined*.
Inlining means they are going to be expanded in place, instead of being called as a function.

This is similar to a macro, the difference being that macros are resolved by the preprocessor at textual level,
which inline functions are just regular functions that are expanded at instruction level.
So in case of macros, the text of a macro will be placed directly where it was used,
but with inline functions, it will be the instructions of the function instead.

Inline functions don't participate in linking either. 
Their difference from static functions is that they don't end up in the executable as regular functions.

> `inline` is technically a hint to the compiler, so it may or may not inline the function.
> This means, technically, it may still end up in the executable.

> See the 3rd example in [linker_examples](./linker_examples).


### Functions have addresses

You can think of the executable file as a sequence of instructions,
where each instruction has an address, so just like regular memory you already understand.
The only difference being that the memory slots cannot be changed (are read only) and
serve a different purpose (store the instructions, letting the processor execute them).

Functions, just like variables, are just names for certain addresses in the executable file.
For example, a function like this:
```cpp
void f()
{
    int a;
    a = 5;
    a = a + 10;
    return;
}
```
will literally look like each individual line as machine instructions written one after the other
in the executable file, with the first instructions (allocating some space for the local variable)
as the first instruction, and `return;` as the last instruction.

There is a couple of special instructions when it comes to functions:
- *Jumping* to an address to continue execution. This is in essence equivalent to calling a function:
  the processor sees this jump instruction, and realizes that it should continue executing the
  instructions starting at the address it's jumping to, which can be the first address of the function.
- Storing the address of the next instruction on the stack (local memory, explained later).
- *Returning* from a function, which is in essence equivalent to jumping 
  to the address stored on the stack to continue executing from there.

An example won't hurt:
```cpp
void f()
{
    int a;
    a = 5;
    a = a + 10;
    return;
}

void g()
{
    f();
    return;
}
```

Which will compile to something like:

| Address | Instruction                                                                                    |
|---------|------------------------------------------------------------------------------------------------|
| 690     | Allocate space for `a` on the stack                                                            |
| 691     | Store 5 in `a`                                                                                 |
| 692     | Add 10 to `a`                                                                                  |
| 693     | Return: read the address stored below `a`, jump to it                                          |
| 694     | Store the address 696 on the stack                                                             |
| 695     | Jump to address 690                                                                            |
| 696     | Return: read the address on the stack (saved by the function that could call this), jump to it |

The addresses 690-693 correspond to `f`, and 694-696 correspond to `g`.

> See the example in [function example](./function_example_1).


### The stack

As mentioned, the stack is used by functions to store local variables and the return addresses
(among other things, like the arguments).
The stack is a relatively large piece of memory that's available to the program,
which has a fixed size and is allocated to the program when it starts.

The stack is used to allocate temporary space for things like local variables.

```cpp
void f()
{
    int a = 5;
    int b = 10;
    // return;
}

void g()
{
    int a = 15;
    f();
    // return;
}
```

The stack will look something like this, when we call `f` from `g` (69420 is an example address):

| Address | Variable                  | Value |
|---------|---------------------------|-------|
| 100     | a (from g)                | 15    |
| 104     | address of `return;` of g | 69420 |
| 112     | a (from f)                | 5     |
| 114     | b (from f)                | 10    |

Note that when `f` returns, continuing the execution of `g`, the stack will look the same,
except for the fact that the local variables of `f` will be effectively forgotten,
even though their values will still remain in memory.
So to `g` the stack will look like this:

| Address | Variable   | Value |
|---------|------------|-------|
| 100     | a (from g) | 15    |
| 104     | ?????????? | 69420 |
| 112     | ?????????? | 5     |
| 114     | ?????????? | 10    |

Meaning that the old values are still there, they just became meaningless without the 
variable names, so we might as well call them just garbage data.

Now supposed we had a program like this:

```cpp
void f1()
{
    int a = 5;
    int b = 10;
    // return;
}

void f2()
{
    int a = 8;
    int b = 9;
    // return;
}

void g()
{
    int a = 15;
    f1();
    f2();
    // return;
}
```

Let me show you how the stack will look at each point in time:

1. When we call `g`, before calling `f1`:

| Address | Variable   | Value |
|---------|------------|-------|
| 100     | a (from g) | 15    |
| 104     |            | ???   |
| 108     |            | ???   |
| ...     | ...        | ...   |

2. When we're at `return;` of `f1`:

| Address | Variable                      | Value |
|---------|-------------------------------|-------|
| 100     | a (from g)                    | 15    |
| 104     | the address of `f2();` in `g` | 69420 |
| 112     | a (from f1)                   | 5     |
| 116     | a (from f2)                   | 10    |
| ...     | ...                           | ...   |

3. Back in `g`, after `f1` returned, before calling `f2`:

| Address | Variable   | Value |
|---------|------------|-------|
| 100     | a (from g) | 15    |
| 104     | ???????    | 69420 |
| 112     | ???????    | 5     |
| 116     | ???????    | 10    |
| ...     | ...        | ...   |

4. When we're at `return;` of `f2`. Note that it got the same memory for the local variables,
   overwriting the memory that `f1` had used:

| Address | Variable                        | Value |
|---------|---------------------------------|-------|
| 100     | a (from g)                      | 15    |
| 104     | the address of `return;` in `g` | 69423 |
| 112     | a (from f2)                     | 8     |
| 116     | a (from f1)                     | 9     |
| ...     | ...                             | ...   |

5. Back in `g`, after `f2` returned:

| Address | Variable   | Value |
|---------|------------|-------|
| 100     | a (from g) | 15    |
| 104     | ???????    | 69423 |
| 112     | ???????    | 8     |
| 116     | ???????    | 9     |
| ...     | ...        | ...   |

> This demonstration is conceptual and should not be relied on: the compiler has the full freedom
> to choose how it should lay out your locals and if it needs to do that at all. 

> See the [stack example 2](./memory_example_3/stack_2.cpp) for a more involved example

### Recursion

Recursion is when a function calls itself, either directly or indirectly.
If you understand the stack and how functions get called, this should be easy to understand.

```cpp
void f(int depth)
{
    if (depth == 2)
        return;

    f(depth + 1);
}

int main()
{
    f(0);
    return 0;
}
```

The function `f` has no local, but it has the parameter `depth`, which
may get space on the stack in place of locals (let's assume it works like a local for the
sake of this demonstration).

The function `f` will return prematurely when `depth` is 2.
Each time `f` calls itself, we pass it larger `depth` values.

If we write out the instructions, it would like kind of like this:

| Address      | Operation      | Instruction                                                                     |
|--------------|----------------|---------------------------------------------------------------------------------|
| 69420 (f)    | `_(int depth)` | Read the local `depth`                                                          |
| 69421        | `depth < 2`    | Compare `depth` to 2                                                            |
| 69422        | `if (_)`       | If `depth` was not equal in the previous comparison, jump to address 104        |
| 69423        | `return;`      | Return: read the address stored below `depth`, jump to it                       |
| 69424        |                | Put the address 69427 on the stack                                              |
| 69425        | `_(depth + 1)` | Put the value of `depth + 1` on the stack (local variable `depth` of next call) |
| 69426        | `f(_)`         | Jump to address 69420                                                           |
| 69427        | `return;`      | Return: read the address stored below `depth`, jump to it                       |
| 69428 (main) |                | Put the address 69431 on the stack                                              |
| 69429        | `_(0)`         | Put the value 0 on the stack (local variable `depth` of first call)             |
| 69430        | `f(_)`         | Jump to address 69420                                                           |
| 69431        | `return 0;`    | Return: read the address, jump to it                                            |

And the stack would look like this (I show the final state rather than the whole progression here):

| Address | Variable            | Value |
|---------|---------------------|-------|
| 100     | address (in `main`) | 69431 |
| 108     | `depth` of `f(0)`   | 0     |
| 112     | address (in `f(0)`) | 69427 |
| 120     | `depth` of `f(1)`   | 1     |
| 124     | address (in `f(1)`) | 69427 |
| 132     | `depth` of `f(2)`   | 2     |

So each function call *gets its own copy of the local variables*.
This is absolutely crucial to realize.

> See [memory example 4](./memory_example_4) for a similar example (that one ignores the return addresses though).


### Function pointers

Just like you can have pointers to variables, you can have pointers to functions.
This can allow you to call functions indirectly, just like you can write to memory indirectly with pointers.

```cpp
// Declare a function pointer type called SumFunctionType
// that takes two ints and returns an int.
// The syntax is the ugliest thing in the world,
// which is why we do a typedef and just forget about it.
typedef int (*SumFunctionType)(int, int);

// Define the function.
// Doesn't have to be a definition, can just as well be a declaration.
int sum(int a, int b)
{
    return a + b;
}

int subtract(int a, int b)
{
    return a - b;
}

int main()
{
    // Take the address of `sum` and store it in a variable.
    // The syntax is the same as with variables.
    SumFunctionType funcPointer = &sum; 

    // Call the function indirectly.
    int s = funcPointer(5, 10); // 15

    // Change the function pointer to point to a different function.
    funcPointer = &subtract;

    // Call the function indirectly.
    int d = funcPointer(5, 10); // -5

    return 0;
}
```
