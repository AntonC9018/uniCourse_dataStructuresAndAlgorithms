This topic is an extension of the previous topic of programming fundamentals, focusing
on RAII, move semantics, some OOP elements and other C++ features.
It is only required for those who want to use standard containers
(`std::vector`, `std::unordered_map`) and `std::string`, and those who have been
explicitly told to study this or just want to learn more.

Concepts covered:
- References (`&`)
- Methods, `this`
- `static` class members
- Scopes, destructors
- Ownership of memory -- the idea of RAII
- Custom `std::vector` implementation with RAII
- `const` parameters and `const` methods
- Constructors, copy constructors
- lvalues and rvalues
- Move semantics (rvalue references `&&`, `std::move`, move constructors)
- Basic templating
- Strings: C strings, `std::string`, `std::string_view`
- Function pointers, `typedef`, `auto`, `decltype`
- Storing data together with functions to implement delegates, `std::function`