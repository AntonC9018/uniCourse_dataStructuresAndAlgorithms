# Strings

*Strings* are arrays of characters.

## ASCII

Now, how do you represent a character in memory (aka as a number)?
For this purpose, people have invented *encodings*.
The simplest encoding is the 7-bit encoding called ASCII.
The symbols and their values are available e.g. [here](https://www.asciitable.com/).

Note that any symbol from ASCII can be represented using 7-bits,
so you can store at most one symbol in a byte.
Sure, the highest bit is then always 0, to make the value of the byte equivalent
to that from the ASCII table. 

The type that represents an ASCII character is `char`.
`char` is an 8-bit type, which can be either signed or unsigned depending on the compiler.

```cpp
#include <iostream>

int main()
{
    char character = 65; // 65 is the code for A in the ASCII table
    std::cout << character; // prints A
}
```

You can also use *character literals*, to make the compiler look up the
number in the ASCII table for you.

```cpp
char character = 'A';
// Equivalent to:
char character = 65;
```

You can do arithmetic on a character, aka increment it, or add some offset to it.
Now look closely at the capital latin letters in the ASCII table.
They are consecutive in the table.
This means we can print the whole alphabet by using a loop.

```cpp
char startCharacter = 'A';
char endCharacter = 'Z';
for (char ch = startCharacter; ch <= endCharacter; ch++)
    std::cout << ch;
```

Same applies to the lowercase alphabet.
For example, you can calculate the offset between the start of the 
capital letters and the start of the lowercase letters to be added
to transform letters from uppercase to lowercase.

> I urge you to try debugging this code to better understand the idea.

```cpp
char offset = 'a' - 'A';
for (char ch = 'A'; ch <= 'Z'; ch++)
{
    char result = ch + offset;
    std::cout << result;
}

// or the other way

char offset = 'A' - 'a';
for (char ch = 'a'; ch <= 'z'; ch++)
{
    char result = ch + offset;
    std::cout << result;
}
```

## Unicode

Unicode refers to a standardized set of encodings that can be used to encode any character.
The most popular one is UTF-8.

All of the regular ASCII characters are represented in UTF-8 without change.
The issue is that we do not have any more space in a byte to represent the other characters,
besides the one extra bit that is unused by ASCII.
The idea is to use that bit to mean that the character is encoded in multiple bytes.

For example, the character `ș` can be written in two bytes like `C8 99` in hex.
What UTF-8 does, is it uses the higher bits to indicate the number of bytes that the character 
is encoded in.

- The first bit being `1` means that *the current character is contained in multiple bytes*.
- The second bit after `1` being `0` means that *the current byte is not the first byte
  of the character*; otherwise, it is.
- The number of `1` before a `0`, following the first `1`, including the first `1`,
  indicates *the number of bytes of the character*.

The idea is that any byte by itself has the context of whether it's a self-contained
ASCII byte (the first bit is 0), the first byte of a sequence (pattern 11),
or one of the other bytes in the sequence (pattern 10).

The table below illustrates the pattern:

| Number of bytes | Byte 1   | Byte 2   | Byte 3   | Byte 4   |
|-----------------|----------|----------|----------|----------|
| 1 (just ASCII)  | 0....... | N/A      | N/A      | N/A      |
| 2               | 110..... | 10...... | N/A      | N/A      |
| 3               | 1110.... | 10...... | 10...... | N/A      |
| 4               | 11110... | 10...... | 10...... | 10...... |

4 bytes is the max.
If the character is more than 4 bytes (this is the case for most emojis),
it's called a grapheme cluster.
It is then represented with multiple UTF-8 characters.

> The different terminology can cause confusion, so the term "character" is
> basically meaningless when talking about UTF-8.
> It's better to refer to a character (a single thing that appears in text)
> as a *text element*, for example, to prevent confusion.
> Different sources / implementations choose different terminology for this.

> A character that fits into 4 bytes is sometimes called a *rune*.

There are also UTF-16 and UTF-32, which have the minimum number of bytes for
a character increased to 2 and 4 respectively, and use similar ideas for encoding it.

## C strings

A *C string* refers to a sequence of characters that ends with a *null terminator*, 
aka the number 0.
In C (not C++!), strings are typically stored in an array, or as a pointer, 
without storing the length of the string (the number of bytes).
The program is assumed to trust that wherever the string ends, it will have a 0 byte,
which is how it can find the end of the string.

```cpp
#include <iostream>
#include <array>

int main()
{
    std::array<char, 6> arr{ 
        'H',
        'e',
        'l',
        'l',
        'o',
        '\0', // same as just 0
    }; 

    // `std::cout` treats `char*` in a special way.
    // It assumes that it's a C string, and prints it as such.
    std::cout << &arr[0]; // Hello
    return 0;
}
```

And if you wrote a 0 byte in the middle of the string,
it will only print it until it finds that.

```cpp
std::array<char, 6> arr{ 
    'H',
    '\0',
    'l',
    'l',
    'o',
    '\0',
}; 
std::cout << &arr[0]; // H
```

You can use a string literal instead of listing each byte:

```cpp
std::array<char, 6> arr = "Hello";
```

String literals can also be assigned to a pointer variable.
This would place them into static memory, 
on some platforms the memory will be immutable 
(writing to it will crash your program).
You shouldn't write to the memory pointed to by such pointers.

```cpp
const char* str = "Hello";
```

## `std::string_view`

We very often need to know the length of the string,
or want to refer to only a part of the whole string,
which is why storing the length along with the pointer is useful.

In this regard, `std::string_view` works just like a `const std::span<char>`.
It stores the pointer to the string, along with the length.
The only difference is that it has some methods that are useful for strings,
and output streams (e.g. `std::cout`) print it as a string.

> For reference, the `<<` operator is not overloaded for `std::span` for streams,
> meaning you can't do `std::cout << span;`, it just won't compile.

There's also some difference in constructors, in that `std::string_view`
can't be implicitly constructed from an `std::array`.
It can still be constructed from a `const char*` though,
which will make it scan the string until it finds the null termination byte
to determine the length.

```cpp
#include <iostream>
#include <array>
#include <string>

int main()
{
    std::array<char, 6> arr = "Hello";
    std::string_view str{&arr[0]};
    std::cout << str.size(); // 5
    std::cout << str; // Hello
    return 0;
}
```

Just like with `std::span`, you can pass it the length in the constructor:

```cpp
std::array<char, 6> arr = "Hello";
std::string_view str{&arr[0], 2};
std::cout << str; // He
```

## `std::string`

`std::string` is an RAII type that allows you to allocate a string on the heap.

```cpp
#include <string>
#include <iostream>

int main()
{ 
    // Construct from a literal.
    // Note that the string is copied into a heap allocated buffer
    // from the static memory where the literal is stored.
    // The local variable stores the pointer to the buffer and the length.
    std::string string1{"Hello world!!"};

    // pointer + length constructor
    // note that it copies the string into a new heap-allocated buffer.
    std::string string2{&string1[0], 10};

    // This does NOT create a new buffer.
    // It points to the buffer of string2.
    std::string_view view{string2};

    std::cout << string1; // Hello world!!
    std::cout << string2; // Hello worl
    std::cout << view; // Hello worl

    return 0;

    // Implicitly added:
    // string2.~string()
    // string1.~string()
}
```

### `std::string` is mutable

```cpp
std::string string1{"Hello world!!"};
string1[0] = 'L';
std::cout << string1; // Lello world!!
```

It also supports convenient concatenation operators:

```cpp
std::string string1{"Hello"};
string1 += " world"; // May reallocate the buffer.
std::cout << string1; // Hello world
```

Also, for short strings, it doesn't actually allocate memory on the heap.
If the string is short enough, it will store it inside the object itself 
(typically up to 23 bytes doesn't allocate).
This is called *small string optimization*.


### `std::string` in C++ is a dynamic array

`std::string` is basically an `std::vector<char>`, because its buffer's capacity and
length are separate, which allows you to potentially be adding characters at the end
without reallocating it on every add.

In C#, for example, strings are immutable, which means that every time you try to append
a character to it, it will create a new string, copy the old string into it, and
then append the new character at the end.
This is really wasteful, but C#'s strings win in the sense that they are immutable,
which has its benefits.


### `const std::string&` as a parameter is dumb

**Do not use `const std::string&` for the type of a parameter.**

If `const` means that you won't be able to modify it, then why do you require the string
to be an actual `std::string`?
There are plenty of other ways to have a string around, it can be stored in any 
linear block of memory.

The best option is to replace that with `std::string_view` which is designed
to be used for that purpose. 
It's way more flexible, because you can create it without allocating dynamic memory
from any pointer + length pair.


### `std::string` is null terminated

The character buffer of any `std::string` 
is guaranteed to be null terminated by the C++ standard.
To get a pointer to the buffer, you can use the `c_str()` method.

