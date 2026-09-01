# Operator Overloading

- [Video](https://www.youtube.com/watch?v=UoMKfmyYEiw&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=18)
- [Information](../../../en/05a_programming_fundamentals/03_operators.md)

## Practice

Implement a `Vector2` type with 2 `float` fields in a separate module (`Vector2.h` and, if needed, `Vector2.cpp`).
`Vector2` must be a plain struct with public fields.

Overload the following operators, where `v` and `w` are vectors and `a` is a `float`:
- `v * a`
- `a * v` (the same as `v * a`)
- `v *= a`
- `v / a`
- `v /= a`
- `v + w`
- `v - w`
- `v += w` (with support for the syntax `(v += w) += w`)
- `v -= w`
- Make `std::cout << v` print the components of `v` in parentheses, separated by a comma
- `v[i]` to obtain a reference to a component (`i` is 0 or 1).

1. Overload them as free `inline` functions inside `Vector2.h`;
2. Leave only the declarations of the overloaded operators in `Vector2.h`, and put the definitions in a `cpp` file;
3. Instead of free functions, use methods declared in the struct and defined in a `cpp` file (where possible).
   Try to modify the function prototypes and bodies using textual replacement in your text editor (search-and-replace).

In `main.cpp`, test the functionality with `assert`s.


## Key ideas

-   Why is the `v * w` operator a bad idea?

    <details>
    <summary>Answer</summary>

    It could mean either the dot product or component-wise multiplication (the Hadamard product).
    It is not obvious which operation `v * w` would perform.
    </details>

-   How can you call a particular operator as a function?

-   What is a "fluent interface"? How can support for it be added to the `<<`, `+=`, `-=`, and similar operators?
    <details>
    <summary>Note</summary>

    A fluent interface can be created without overloading operators.
    Methods can be used as well.

    For example, with your own `Vector2` type, you could do this:
    ```cpp
    struct Vector2
    {
        // ...

    public:
        Vector2& add(Vector2 v)
        {
            *this = *this + v;
            return *this;
        }

        Vector2& sub(Vector2 v)
        {
            *this = *this - v;
            return *this;
        }
        
        Vector2& scale(float a)
        {
            *this = *this * a;
            return *this;
        }

        Vector2& printInto(std::ostream& out)
        {
            // ...
            return *this;
        }
    };

    void usage()
    {
        Vector2 val{1, 2};
        val.add({ 1, 2 })
            .sub({ 2, 3 })
            .printInto(std::cout) // (0, 1)
            .scale(5)
            .add({ 1, 2 })
            .printInto(std::cout); // (1, 7)

        val.printInto(std::cout); // (1, 7)
    }
    ```

    For example, for printing, the language designers could have made an interface like this instead of `<<`:
    ```cpp
    std::cout
        .print(v)
        .print(std::endl)
        .print(w)
        .print(std::endl);
    ```
    The only drawback is that it would not be possible to overload `print` for your own type
    without an additional overloading mechanism, such as requiring `Vector2` to have a method with a specific name
    or a `print` method with a particular signature
    (`print` would need to invoke the overloaded logic, for example through static polymorphism using a `template`).

    </details>
