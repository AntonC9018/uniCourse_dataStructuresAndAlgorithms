## Variables

A *variable* represents a memory location with a name.
The computer will allocate (provide) this memory location when our program is executed.

Each variable has a *type* associated with it. 
For now think of a type as a conceptual name that defines the number of bytes of memory
that will need to be allocated for the variable.
For example, the type `std::byte` means this size will be 1 byte of memory, 
and `int` is (typically) 4 bytes, 
and a `size_t` is (typically) 8 bytes.

To **declare** a variable (make the computer allocate memory for it, and name that memory in the source code),
we need to type in the type and a the variable name (of what it's supposed to represent).
For example:

```cpp
// Declare an int, aka allocate 4 bytes of memory and name it "i"
int i;
// Declare a byte, aka allocate 1 byte of memory and name it "myByte"
std::byte myByte;
```

You also need to initialize the variable, which means write a value into the memory of that variable.
By default any variable's memory is "unititialized", which means it will contain whatever was in that memory previously, which in practice can be anything
(this is often called "garbage" or "garbage data").
Typically what you do is you should immediately "zero out" the value, if you're going to use it later.
Zeroing the value means writing a zero into each byte of the memory of the variable.
The way you do this in C++ is you assign `{ }` (you can use 0 as well if it's a number type, like int).

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