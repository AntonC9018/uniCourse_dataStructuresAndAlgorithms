# Algorithm Practice

- [Video on algorithms](https://www.youtube.com/watch?v=C6plSGSYuyc&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=8)

## CONVINCE ME THAT I NEED THIS!

Programming projects of any complexity always involve analyzing and solving problems.
Solving problems requires identifying an algorithmic solution and implementing it in a program.
To do this effectively, you need to train
a particular way of thinking called **algorithmic thinking**.

Even though simple problems may seem unrealistic
("who would sum an array of numbers in the real world?
There is already a built-in function for that!")
solving them **trains exactly that algorithmic thinking**.

Analyzing and solving simple problems will help you develop **high-level thinking**,
which means **understanding abstractions
without having to recall their basic components**.
This is an essential skill both for solving more complex problems
and for effectively understanding and using existing solutions.

## Goals

The goal of this work is to learn how to:
- analyze and understand a problem;
- break a problem down into subproblems and each subproblem into even smaller subproblems;
- develop an algorithm by logically deriving and explaining
  every step based on the problem conditions;
- represent the problem conditions in a program and
  correctly determine the data structures and interface;
- represent the algorithm steps as program instructions.

You need to learn to do all this quickly enough when solving simple problems.

Ideally, you should see elementary operations and code instructions as intuitively equivalent:
you should immediately understand an operation by looking at the programming language syntax,
without thinking about it or searching for syntax examples,
and, conversely, you should be able to turn a verbal description of an operation into code.

## Practical task with explanations

- Write a function that multiplies the corresponding elements of 2 arrays, storing the results in the 1st array.

<details>
<summary>What will the interface be?</summary>

The first and second arrays must be passed to the function as parameters.
We will also write the result to the first one.

The return type is `void`, because the result is written to the array
passed as the first parameter.
The function does not return a value.

```cpp
void product(std::span<int> inputOutput, std::span<int> coefficients)
{
}
```

You can also make the second parameter read-only,
because its array elements will not be overwritten.

```cpp
void product(std::span<int> inputOutput, std::span<const int> coefficients)
{
}
```
</details>

- Use `assert` to make sure that the spans have the same length.

<details>
<summary>How?</summary>

```cpp
assert(inputOutput.size() == coefficients.size());
```
</details>

- Implement a version using an infinite loop, then exit it manually with `break`.

- Implement a version with a conditional `while` loop.

- Implement a version with a `for` loop.

## More practice

If you do not feel confident enough yet, practice with different algorithms, for example:
- Count how many numbers in an array are greater than 5;
- Find the maximum value in an array;
- Find the two largest values in an array;
- Generate the first `n` prime numbers;
- Calculate Fibonacci numbers;
- and so on.

You can practice simple problems on [LeetCode](https://leetcode.com/).
