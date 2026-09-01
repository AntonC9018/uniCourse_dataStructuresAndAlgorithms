# Assessment 1 Template

## 1. Algorithms (48 points)

- [Video](https://www.youtube.com/watch?v=C6plSGSYuyc&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=9)

Write out the steps of an algorithm for solving a problem, explaining the logic behind every decision as fully as possible.

Example problems:
- Calculating the sum of the elements in a list;
- Finding the maximum;
- Finding the number of values divisible by 5;
- Pairwise operations on 2 lists;
- Finding an element's position according to a rule;
- A similar simple problem.


**Solution steps:**

1. (2 points) Identify the interface. 
   From this point on, assume that all input data is *already available* 
   (you do not need to request it from the user).

2. (30 points) Analyze the problem.
   Break the problem down into subproblems.
   Break each one down further into subproblems or sub-ideas 
   until you reach *primitive operations* (listed below).

   Describe all sub-ideas and subproblems, as well as their logical connections, in as much detail as possible.  
   **An intuitive leap that skips a level of logic is considered an error —
   the intuition must later be justified by logic for it to count.**

3. (10 points) Put the primitive operations in the correct order,
   possibly adding intermediate primitive operations,
   to obtain the final algorithm.

4. (4 points) Execute the resulting algorithm on several given examples.
   At each step, indicate the current state of the allocated
   memory cells (you do not have to write out lists; record them only when their contents change).

5. (2 points) Write the algorithm as a C++ function using a `while` loop.


**Primitive operations:**

1. Create a memory cell (variable) with a name.
2. Read from a memory cell by name.
3. Read from a list by index. (It can be written as `A[i]`.)
4. Read a parameter (for example, the length of a list).
5. Write a value into a memory cell.

6. Evaluate an expression in order to write its result into a memory cell or use it in a condition.
   For example: "the value in `a` + 1 is written into the memory cell `a`" or
   "the value in `a` + the value in `c` is written into the memory cell `b`."

   You may write this as `a = a + 1` and `b = a + c`, or as
   `a + 1  -->  a` and `a + c  -->  b`.

7. Check a condition and perform actions only when it is true.
   If there are several actions, create a sublist of steps for them.

   For example:

   ```
   5. If а > b
        1. a = 5
        2. b = 6
   6. Next step.
   ```

   You may use the notation `if (a > b)`.

8. End the algorithm and output the result (can be written as `return result`).
9. Go to a specific algorithm step.
10. Signal an error and terminate the algorithm prematurely.

Operations can be combined; for example, "If a > b, read from a, and write into b" 
includes 3 primitive operations, but this is allowed (within reason).


## 2. Syntax (24 points)

- A randomly selected basic comprehension question from [lab 1](01_instruction.md)
  on the following subtopics: variables, pointers, and pointer arithmetic.

  Grading (18 points):
  - 1 point for each correct answer;
  - 5 points for the reasoning behind each one.

- A randomly selected basic comprehension question from the [structures lab](06_struct.md).
  (It will not be about functions.)

  Grading (6 points):
  - 1 point for a correct answer;
  - 5 points for the reasoning.
