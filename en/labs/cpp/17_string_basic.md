# Strings

- Accompanying [video](https://www.youtube.com/watch?v=3aXFuiHxb9k&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=11&t=639)
- [Video about memory types](https://www.youtube.com/watch?v=jAr_jicQv4Y&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=22)

## Concepts

- Encodings, character codes, ASCII
- C strings, null termination
- Memory layout of string literals
- `std::string_view`

## Examples to analyze

### 1. Size of `char`
```cpp
std::cout << sizeof(char) << std::endl;
```

### 2. Printing a character
```cpp
char a { '1' };
std::cout << a << std::endl;
```

### 3. A character as a number
```cpp
char a { '1' };
std::cout << static_cast<int>(a) << std::endl;
```

### 4. A number as a character
```cpp
char a { 98 };
std::cout << a << std::endl;
```

### 5. Printing a null-terminated character array
```cpp
std::array<char, 2> s{ 'a', 0 };
char* p{ s.data() };
std::cout << p << std::endl;
```

### 6. Printing a character array with 0 in the middle
```cpp
std::array<char, 5> s{ 'a', 'b', 0, 'c', 'd' };
std::cout << s.data() << std::endl;
```

### 7. Printing an array after modification
```cpp
std::array<char, 5> s{ 'a', 'b', 'c', 'd', 0 };
std::cout << s.data() << std::endl;
s[1] = 'e';
std::cout << s.data() << std::endl;
s[2] = 0;
std::cout << s.data() << std::endl;
```

<!-- ab, a, ab0cd, cd, address of s, UB -->
### 8. Character code of `\0`
```cpp
char z{ '\0' };
std::cout << static_cast<int>(z) << std::endl;
```

### 9. `\0` in an array
```cpp
std::array<char, 5> s{ 'a', 'b', '\0', 'c', 'd' };
std::cout << s.data() << std::endl;
```

### 10. Silencing warnings about unused variables

Compile this program with the `-Wunused` flag and interpret the result.

```cpp
int main()
{
    [[maybe_unused]] int a{ 1 };

    int b{ 2 };
    (void) b;

    int c{ 3 };
}
```

<details>
<summary>Compilation result</summary>

Although `a` and `c` are unused, the attribute suppresses the warning for `a`,
and the cast to `void` counts as a use of `b`.
Therefore, the compiler issues a warning only for `c`.
```
❯ g++ -std=c++20 -Wall -Wconversion -Wextra -Wunused -pedantic test.cpp
test.cpp: In function ‘int main()’:
test.cpp:7:5: warning: unused variable ‘c’ [-Wunused-variable]
    7 | int c{ 3 };
      |     ^
```
</details>

### 11. Printing a character array without a trailing 0
```cpp
std::array<char, 2> s{ 'a', 'b' };
std::array<char, 2> s1{ '1', '\0' };
(void) s1;
std::cout << s.data() << std::endl;
```

<details>
<summary>Answer</summary>

This is UB, but the compiler does not detect it during compilation
and does not issue any warnings.

The variables will likely be placed next to each other in memory:

<table>
    <tr>
        <th><b>Variable</b></th>
        <th colspan="2">s</th>
        <th colspan="2">s1</th>
    </tr>
    <tr>
        <th><b>Character</b></th>
        <th>a</th>
        <th>b</th>
        <th>1</th>
        <th>'\0'</th>
    </tr>
    <tr>
        <th><b>Code</b></th>
        <th>97</th>
        <th>98</th>
        <th>49</th>
        <th>0</th>
    </tr>
</table>

Since printing this pointer treats it as a null-terminated character sequence beginning at the first element of `s`,
it may also print `1` from the `s1` array before reaching its `\0`.
If `s1` did not end in `\0`, printing might continue
until it encountered the first zero byte after the memory occupied by `s1`,
printing data left there from a previous use of that memory.
</details>

### 12. A string as an array
```cpp
char s[]{ "12" };
size_t count{ sizeof(s) }; // sizeof(char) == 1
std::cout << count << std::endl;
std::cout << s << std::endl;
std::cout << static_cast<int>(s[count - 1]) << std::endl;
```

<details>
<summary>Answer</summary>

`s` contains 3 characters, not 2.
When a string literal is used to initialize an array,
it automatically includes a trailing `\0`.
</details>

### 13. A string literal containing `\0`
```cpp
char s[]{ "12\0" };
std::cout << sizeof(s) << std::endl;
```

<details>
<summary>Answer</summary>

`s` contains 4 characters.
Even though `s` already has a zero byte at the end, the compiler will add another one.
</details>

### 14. `\0` pitfalls
```cpp
char arr[]{ "1\023" };
std::cout << sizeof(arr) << std::endl;
```

<details>
<summary>Explanation</summary>

Here, `\0` is interpreted together with `23` as a single escape sequence,
representing a character code written in octal.

To insert `\0` in the second position here,
you can use string literal concatenation:
```cpp
char arr[]{ "1\0" "23" };
```
</details>

### 15. `std::to_array` (1)
```cpp
auto s{ std::to_array("abc") };
std::cout << s.size() << std::endl;
```

### 16. `std::to_array` (2)
```cpp
auto s{ std::to_array("a\0bc") };
std::cout << s.size() << std::endl;
```

### 17. `const char*`

- Where are the string characters stored?
- Why is `const` necessary?
- How can you get the string length?

```cpp
const char* s{ "123" };
std::cout << s << std::endl;
```

<details>
<summary>Where the characters are stored</summary>

The characters are stored in static memory.
The variable `s` stores a pointer to the first character in that sequence.
</details>

<details>
<summary>Why <code>const</code>?</summary>

String literal data is often placed in read-only memory,
which the program is not allowed to modify.
This is intentional because string literals are immutable and may be **shared**.
Protecting them from modification ensures that all uses of a shared literal
observe the same contents.

In the following example, the addresses in `a` and `b` may be the same:
```cpp
const char* a{ "123" };
const char* b{ "123" };
std::cout << static_cast<void*>(a) << std::endl;
std::cout << static_cast<void*>(b) << std::endl;
```
</details>

<details>
<summary>String length</summary>

`sizeof(s)` here gives the size of the `s` object based on its type, `const char*`.
Here, the pointer occupies 8 bytes.

`sizeof(s)` here **will not give the string length**,
because `s` is only a pointer: its type does not encode the size
of the character buffer it points to.

To obtain the C-string length, you must traverse its bytes
until you find the end of the string (the null character),
counting as you go.
However, if there is a null character in the middle of the buffer,
this will not give the actual number of characters stored in it.
Therefore, in C++ **it is impossible to determine the actual buffer length from `const char*` alone**.

You can get the literal's length by creating a reference to it
before decay to `const char*` occurs:
```cpp
// Размер есть в типе, можно использовать как указатель.
const char(&s)[4]{"123"};

// Сам определяет тип const char(&)[4] из строки.
auto& s{"123"};
```
</details>

### 18. String comparison (1)

```cpp
const char* a{ "123" };
auto b{ std::to_array("123") };
const char* bp{ b.data() };
if (a == bp)
{
    std::cout << "Equal" << std::endl;
}
else
{
    std::cout << "Not Equal" << std::endl;
}
```

### 19. String comparison (2)
```cpp
#include <iostream>
#include <array>
#include <cstring>

int main()
{
    const char* a{ "123" };
    auto b{ std::to_array("123") };
    const char* bp{ b.data() };
    if (std::strcmp(a, b) == 0)
    {
        std::cout << "Equal" << std::endl;
    }
    else
    {
        std::cout << "Not Equal" << std::endl;
    }
}
```

### 20. `std::string_view` after modifying the source
```cpp
std::array<char, 4> arr{ "123" };
std::string_view v{ arr.data(), 3 };
arr[0] = 'a';
std::cout << v << std::endl;
```

### 21. `std::string_view` can refer to any contiguous character sequence

```cpp
#include <iostream>
#include <string_view>
#include <array>

void usage(std::string_view v)
{
    std::cout << v.size() << std::endl;
    std::cout << v << std::endl;
}

int main()
{
    {
        std::array<char, 3> s{ 'a', 'b', 'c' };
        usage({ s.data(), s.size() });
    }
    {
        auto s{ std::to_array("abc") };
        usage({ s.data() });
    }
    {
        char s[]{ "abc" };
        usage({ s });
    }
    {
        auto& s{ "abc" };
        usage({ s });
    }
    {
        const char* s{ "abc" };
        usage({ s });
    }
}
```

### 22. `std::string_view` determines the length when created

If the string length is not specified explicitly,
`std::string_view` determines it during construction by traversing the string
until it finds a zero byte, even if the passed argument's type contains this information.

The only exception is when a `std::string_view` is created from another `std::string_view`.

```cpp
#include <iostream>
#include <string_view>
#include <array>

void usage(std::string_view v)
{
    std::cout << v.size() << std::endl;
    std::cout << v << std::endl;
}

int main()
{
    {
        std::array<char, 3> s{ 'a', '\0', 'c' };
        usage({ s.data(), s.size() });
    }
    {
        auto s{ std::to_array("a\0c") };
        usage({ s.data() });
    }
    {
        char s[]{ "a\0c" };
        usage({ s });
    }
    {
        auto& s{ "a\0c" };
        usage({ s });
    }
    {
        const char* s{ "a\0c" };
        usage({ s });
    }
    {
        std::string_view s{ "a\0c", 3 };
        usage({ s }); // 3
    }
}
```

### 23. String comparison using `std::string_view`

```cpp
auto s1{ std::to_array("abc") };
auto& s2{ "abc" };

std::string_view v1{ s1.data(), s1.size() - 1 };
std::string_view v2{ s2, sizeof(s2) - 1 };

if (v1 == v2)
{
    std::cout << "Equal" << std::endl;
}
else
{
    std::cout << "Not Equal" << std::endl;
}
```

## Counting the character 1

Write a function that counts how many `1` characters are in a `std::string_view`.

Write several tests for each case (no 1s, several 1s, all 1s) using `assert`.

<details>
<summary>Example</summary>

```
void runTests()
{
    assert(countOnes("001100") == 2);
    // ...
}
```
</details>

## Getting a word

Write a function that finds the first ` ` in a string
and returns the portion of the string after it, up to the next ` `.
If there is no next ` `, return the rest of the string.

Write tests as in the previous task.

Examples: 
```
secondWord("Hello world") == "world"
secondWord("Hello my dear") == "my"
secondWord("Hello") == ""
secondWord("") == ""
secondWord(" ") == ""
secondWord(" a ") == "a"
secondWord("a  ") == ""
secondWord("a  b") == ""
secondWord("hello     world    dear") == ""
```
