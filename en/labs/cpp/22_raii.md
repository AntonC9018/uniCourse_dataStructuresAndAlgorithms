# Constructors, Destructors, RAII

- [Video about OOP, RAII](https://www.youtube.com/watch?v=Lc2VUm09-6s&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=16).
- [Video about memory types](https://www.youtube.com/watch?v=jAr_jicQv4Y&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=14).
- [Information about RAII](../../../en/05a_programming_fundamentals/02_RAII.md)

## Example

```cpp
// Файл HeapInt.h
#pragma once // 1
#include <cassert>

class HeapInt
{
private:
    int* heapValue; // 2

public:
    // 3
    inline HeapInt(int val) 
        // 4
        : heapValue(new int{ val })
    {
    }

    inline ~HeapInt()
    {
        // Заметка: delete проверяет на nullptr сам.
        delete heapValue; // 5
    }

    inline int& asRef()
    {
        assert(heapValue != nullptr); // 6
        return *heapValue;
    }

    HeapInt(const HeapInt& hello); // 7
    HeapInt(HeapInt&& hello);
    void operator=(const HeapInt& hello);
    void operator=(HeapInt&& hello);
};

// Файл main.cpp
#include "HeapInt.h"
#include <utility>

void constructors()
{
    HeapInt a{5}; // 8
    HeapInt b{a}; // 9
    HeapInt c{std::move(a)}; // 10
    HeapInt d = b; // 11
    HeapInt e = std::move(b); // 12
    d = std::move(c); // 13
    d = e; // 14
}

// Файл HeapInt.cpp
#include "HeapInt.h"

// ... 15
```

The `HeapInt` class above is a wrapper around a dynamically allocated int.
Unlike a regular `int*`, this type does not allow `nullptr` as a normal value.

The exception is a moved-from object. A move constructor or move-assignment
operator can leave such an object with `heapValue == nullptr`, preventing the same memory from being freed twice.
A moved-from object must still be valid for destruction and reassignment, but its value cannot be read
before it is assigned a new value.

The class follows RAII: it allocates memory in its constructor and deletes it in its destructor.

1. Why is the `heapValue` field (2) private?

   <details>
   <summary>Hint</summary>

   Data encapsulation.
   </details>

   <details>
   <summary>Answer</summary>

   So that code outside the class cannot overwrite the pointer directly.
   Only the value it points to can be overwritten from outside the class.
   </details>

2. What does the syntax at (4) mean? How can it be written in the constructor body?

   <details>
   <summary>Answer</summary>

   ```cpp
   inline HeapInt(int value)
   {
       // : heapValue(new int{value})

       // Выделение памяти
       // new int
       int* t = new int;

       // Инициализация объекта в динамической памяти
       // {value}
       *t = value;

       // Присваивание поля
       // : heapValue(...)
       this->heapValue = t;
   }
   ```
   </details>

3. How can this be compiled with GCC?

   <details>
   <summary>Answer</summary>

   > You can also add `-W` flags.

   ```
   g++ -c main.cpp -o main.o
   g++ -c HeapInt.cpp -o HeapInt.o
   g++ main.o HeapInt.o -o program
   ```

   Or with one command:

   ```
   g++ main.cpp HeapInt.cpp -o program
   ```
   </details>

4. Why is (1) needed? What situation does it prevent?

   <details>
   <summary>Answer</summary>

   To ensure that the header is included only once.

   If another header, `demo.h`, contained an `#include "HeapInt.h"` directive,
   and both headers were included in `main.cpp`, then without `#pragma once`, `HeapInt.h` would be included
   2 times, causing the type and functions to be defined 2 times, which is not allowed.
   Therefore, the program would not compile.

   To prevent such bugs, which are often hard to spot,
   `#pragma once` is always used in headers.
   </details>
   

5. Why is (3) defined as `inline`?

   <details>
   <summary>Answer</summary>

   It is *defined* in the header.
   If it is not made `inline`, the linker will report an error if the header is included
   in more than one `compilation unit` (the function is defined more than once).
   </details>

6. How can the requirement for a constructor or function to be `inline` be avoided?

   <details>
   <summary>Answer</summary>

   Leave only the declaration in the header.
   Define it in a cpp file.
   </details>


7. Why is the check at (6) necessary if `heapValue` is normally not `nullptr`?

   <details>
   <summary>Hint</summary>

   When an object is passed to an rvalue-reference parameter (`HeapInt&&`),
   its allocated memory can be taken from it.
   Code that takes ownership of this memory must also set the passed object's pointer to `nullptr`.
   </details>

   <details>
   <summary>Detail</summary>

   One might conclude that, since every `HeapInt` object has a non-null `heapValue`, there is no need
   to take memory from an object passed as `HeapInt&&`; instead, the value could simply be copied, because the memory will be deleted
   in the source object's destructor. However, for the `swap` task to work correctly,
   it is important to transfer ownership of the memory itself—at least when the destination object's `heapValue == nullptr`.
   Moving another object into one that was previously moved from is a valid operation.

   This check remains necessary because a move constructor exists.
   </details>


9. Explain which constructors or overloaded operators are called at (8-14).
   Which of them are equivalent?

10. How can the syntax in (11-12) be disallowed?

   <details>
   <summary>Hint</summary>

   `explicit`.
   </details>

11. Define the constructors and operators declared in (7) at (15).

    <details>
    <summary>How can a constructor or overloaded operator be defined outside the class?</summary>

    ```cpp
    class Hello
    {
        Hello(AnyParam p);
    }

    Hello::Hello(AnyParam p)
    {
        // ...
    }
    ```

    For an operator, the same syntax is used as for methods (the method name is `operator=`).
    </details>


    <details>
    <summary>What should they do?</summary>

    Remember that all these operations must comply with the rules of RAII:
    each block of allocated memory must have only one owner.
    They must work correctly in any sequence.

    The copy constructor must allocate fresh memory and copy the numeric value from the source object
    (you can simply call the constructor that takes an `int` parameter with the source object's value).

    The move constructor must take the pointer from the source object and set the source object's pointer to `nullptr`.
    This prevents the same pointer from being deleted a second time in the destructor.

    The assignment operator must copy the value pointed to by the other object's `heapValue`
    into the existing `heapValue`.

    The assignment operator that takes an rvalue-reference parameter must take ownership of the pointer from the source object.
    </details>

12. In what other situation is the rvalue-reference overload of a constructor or assignment operator called?

    <details>
    <summary>Overload?</summary>

    An *overload* is a function with the same name but different parameters.
    </details>

    <details>
    <summary>Answer</summary>

    It is called with temporary objects—that is, values of the required object type that are not stored in a variable
    but are passed directly to a function.
    </details>

13. How many times is the `HeapInt` destructor called after (14)?

    <details>
    <summary>Answer</summary>

    As many times as there are variables of this type.

    For example, `a` was moved from using `std::move`,
    but its destructor is still called.
    </details>

14. Explain what you think motivated the decision not to define a default constructor for this type.

    <details>
    <summary>Definition</summary>

    A *class contract* is a set of rules that always hold while an object exists,
    regardless of the operations that have been performed on it.

    For this class, the contract is that `heapValue` cannot be equal to `nullptr`,
    except for the explicitly specified state of an object after it has been moved from.

    More broadly,
    a contract describes requirements for input data (preconditions)
    and guarantees about output data (postconditions);
    it may be stated in a function's interface.
    A *class contract* is essentially a set of conditions associated with the implicit `this` parameter
    that *every* method of the class must uphold.
    </details>

    <details>
    <summary>Answer</summary>

    To uphold the class contract.

    There were several options:
    - make a default constructor that would put `nullptr` in `heapValue`,
      which would violate the class contract;

    - allocate memory in the default constructor,
      which I usually do not recommend (default constructors should be cheap);

    - not provide a default constructor at all.

    </details>

15. Explain why reading an object's value after moving from it using `std::move` is an invalid operation.

    <details>
    <summary>Answer</summary>

    The object may have entered a state in which its value cannot be read.

    For example, `heapValue` may become equal to `nullptr`; this is the only situation in which that can happen.
    </details>
    
16. Create a function `void swap(HeapInt& a, HeapInt& b)` that swaps the values
    without allocating new dynamic memory.

    <details>
    <summary>Hint 1</summary>

    An implementation for a regular type that does not use RAII would be:
    ```cpp
    void swap(Whatever& a, Whatever& b)
    {
        Whatever temp = a;
        a = b;
        b = temp;
    }
    ```
    </details>

    <details>
    <summary>Hint 2</summary>

    Move operations allow a value to be transferred from one object to another.
    </details>

    <details>
    <summary>Hint 3</summary>

    Think about which operations are used in Hint 1 (the copy constructor and assignment operator).
    Replace them with move operations.
    </details>
