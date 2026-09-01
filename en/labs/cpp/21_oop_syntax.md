# Basic OOP

- [Video](https://www.youtube.com/watch?v=Lc2VUm09-6s&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=16) up to `NumberWrapper`.
- [Information](../../../en/05_programming_fundamentals/linker_examples)

## Basic Concepts

1. What is a method?

   <details>
   <summary>Answer</summary>
   A method is a function defined within a structure or class.
   </details>

2. What is a "member function"?

   <details>
   <summary>Answer</summary>
   It is a synonym for a method.
   </details>

3. What is a class member?

   <details>
   <summary>Answer</summary>
   A class member can be a method or field, as well as a constructor or destructor (which come later).
   </details>

4. How does an instance function differ from a static one?

   <details>
   <summary>Linker</summary>
 
   `static` for methods is unrelated to `static` used for internal linkage. Do not confuse them.
   </details>
   
   <details>
   <summary>Answer</summary>
 
   Instance functions receive a hidden `this` parameter — a pointer to the object.
   </details>

5. What is the syntax for calling methods?

   <details>
   <summary>Answer</summary>
 
   Instance methods can only be called
   using member-access syntax: `obj.action(parameter)`,
   which passes `&obj` as the hidden `this` parameter
   (if `obj` is a pointer, use `obj->action(parameter)` instead).
 
   Static methods can be called via `obj.action(parameter)`
   or as `Object::action(parameter)` (where `Object` is the type of `obj`).
   No hidden `this` exists for them, so it is not passed.
   
   </details>

6. How can a method be declared and defined separately?

   <details>
   <summary>Answer</summary>
   
   A method can be declared just like an ordinary function.
   ```cpp
   class Hello
   {
       static void world();
   }
   ```
 
   It can be defined either directly in the class or outside it as `void Hello::world()`.
 
   ```cpp
   class Hello
   {
       static void world();
   }
   
   // ...
   
   void Hello::world()
   {
       std::cout << "Hello" << std::endl;
   }
   ```
   
   The same syntax applies to instance methods.
   </details>

7. Can a method inside a class have internal linkage
    (so that it is defined only in the current compilation unit)?

   <details>
   <summary>Answer</summary>
   
   You cannot give just one method internal linkage. Giving the class internal linkage gives all of its methods internal linkage. A nested class can be used as a workaround.
   [See the documentation](../../../en/05a_programming_fundamentals/05_module.md#private-members-in-the-header-file).
   </details>

8. Is the `new` operator required to create an object of a class (a structure with methods)?

   <details>
   <summary>Answer</summary>
   No. Objects of class types can be allocated on the stack, just like ordinary structures without methods.
   </details>

9. Does the number of methods in a class affect how many bytes an object of that class type occupies?

   <details>
   <summary>Answer</summary>
   No. Methods belong to the type itself, not to a particular object.
   The instructions in the methods themselves take up memory, but separately from each object's memory.
   </details>

10. Does an object with one method take more memory than an object without methods?

    <details>
    <summary>Answer</summary>
 
    No, if the methods are not virtual.
   Virtual methods will be covered later, in the topic on polymorphism.
 
    You can check how much memory any object occupies using `sizeof`.
    </details>

11. What is the functional advantage of using methods instead of ordinary functions
     that explicitly take a parameter similar to `this` as their first parameter?

    <details>
    <summary>Answer</summary>
    Functionally—that is, in terms of what happens when the program runs—there is no difference.
    Therefore, the correct answer is that methods have no functional advantage.
 
    Methods have an advantage in organizing code:
    if all operations on data of a particular type are defined within the type definition,
   they are easier to find.
 
    OOP also makes it possible to encapsulate data,
   which is harder to achieve using typical procedural programming.
    </details>
