- Variables
- Functions
- `std::cin` and `std::cout`
- Pointers, pointer arithmetic, `void*`, `&`
- C arrays
- `for` and `while` loops
- `struct`, `.` and `->`
- `auto`??
- C++ references


For the C++ OOP part (I think I need to teach this to the 2nd year students):
- Accessibility modifiers
- Methods, `this`
- Function pointers
- The concept and motivation of a vtable (polymorphism, virtual methods)
- Linear search of implemented vtable vs adjusting the pointer
- Interfaces (abstract classes without fields) for polymorphism
- Constructors and destructors, including creation syntax; RAII
- Single inheritance of fields (no pointer adjustment)
- Virtual inheritance (pointer adjustment)
- Useless diamond inheritance, how solved at a low level (see link in resources), syntax
- `std::static_cast`, `std::dynamic_cast`, `std::reinterpret_cast`
- `static` fields and methods
- `const` fields and methods (this is probably outside the scope)
- `std::unique_ptr` (and maybe `std::shared_ptr`)