# Flow control

## Concepts

- `if`
- `else`
- `else if`
- `while (true)`
- `continue`
- `break`
- `do ... while`

## Understanding examples

### 1. `true` in a condition
```cpp
if (true)
{
   std::cout << "Hello" << std::endl;
}
```

<details>
<summary>Answer</summary>

`true` in a condition causes the body of the `if` statement to always execute.
</details>

### 2. `false` in a condition
```cpp
if (false)
{
   std::cout << "Hello" << std::endl;
}
```

<details>
<summary>Answer</summary>

The body of the `if` statement is guaranteed not to execute.
</details>

### 3. A `bool` variable in a condition
```cpp
bool execute = true;
if (execute)
{
   std::cout << "Hello" << std::endl;
}

bool notExecute = !execute;
if (notExecute)
{
   std::cout << "Not executed" << std::endl;
}
```

<details>
<summary>Answer</summary>

When run, only Hello will be printed.
</details>

### 4. Numbers in a condition
```cpp
if (1)
{
   std::cout << "1" << std::endl;
}
if (123)
{
   std::cout << "123" << std::endl;
}
if (0)
{
   std::cout << "0" << std::endl;
}
```

<details>
<summary>Answer</summary>

In C++, `if` accepts any expression that can be converted to `bool`.
This code will compile and print `1` and `123`.
</details>

### 5. A pointer in a condition
```cpp
int* a { nullptr };
if (a)
{
   std::cout << "a is true" << std::endl;
}

int b {};
int* pb { &b };
if (pb)
{
   std::cout << "pb is true" << std::endl;
}
if (b)
{
   std::cout << "b is true" << std::endl;
}

bool c { false };
bool* pc { &c };
if (pc)
{
   std::cout << "pc is true" << std::endl;
}
```

<details>
<summary>Answer</summary>

When the condition is a pointer, `if` checks whether it is non-null (not `nullptr`).
`a is true` will not be printed here, while `pb is true` and `pc is true` will be printed.

`if (b)` is equivalent to `if (0)`, which is equivalent to `if (false)`.
`b is true` will not be printed.
</details>

### 6. Multiple statements in the body
```cpp
if (false)
{
   std::cout << "A" << std::endl;
   std::cout << "B" << std::endl;
}
```

<details>
<summary>Answer</summary>

Nothing will be printed.
</details>

### 7. Without braces
```cpp
if (false)
   std::cout << "A" << std::endl;
   std::cout << "B" << std::endl;
```

<details>
<summary>Answer</summary>

Only `B` will be printed because only the first statement is attached to the `if`.

Equivalent code:
```cpp
if (false)
{
   std::cout << "A" << std::endl;
}
std::cout << "B" << std::endl;
```
</details>

### 8. `else`
```cpp
if (false)
{
   std::cout << "A" << std::endl;
}
else
{
   std::cout << "B" << std::endl;
}
```

<details>
<summary>Answer</summary>

This code will print `B`, since the `else` block executes when the condition is not satisfied.
</details>

### 9. Reassigning a condition variable inside the `if` body
```cpp
bool a = true;
if (a)
{
   a = false;
}
else
{
   std::cout << "B" << std::endl;
}
```

<details>
<summary>Answer</summary>

`B` will not be printed because whether `else` executes is determined when `a` is checked in the `if`,
which happens before it is changed.
</details>

### 10. `return` in an `if`
```cpp
void F()
{
   if (true)
   {
       return;
   }
   else
   {
       std::cout << "Else" << std::endl;
   }
   std::cout << "After Else" << std::endl;
}
```

<details>
<summary>Answer</summary>

`Else` will not be printed here.
Whether the `else` block executes depends only on the condition in the `if`.

`return` exits the function immediately, so `After Else` will not be printed either.
</details>

### 11. Code after `else`
```cpp
if (true)
   std::cout << "A" << std::endl;
else
   std::cout << "B" << std::endl;
std::cout << "C" << std::endl;
```

<details>
<summary>Answer</summary>

`B` will not be printed. `A` and `C` will be printed.
</details>

### 12. `if` without braces, `else` with braces
```cpp
if (true)
   std::cout << "A" << std::endl;
else
{
   std::cout << "B" << std::endl;
}
```

<details>
<summary>Answer</summary>

It is valid to use an unbraced statement after `if` and an explicit block after `else`.
</details>

### 13. An `if`-`else` chain

How would this code usually be written using an `if`-`else` chain?
```cpp
if (a)
{
   std::cout << "A" << std::endl;
}
else
{
   if (b)
   {
       std::cout << "B" << std::endl;
   }
   else
   {
       if (c)
       {
           std::cout << "C" << std::endl;
       }
   }
}
```

<details>
<summary>Answer</summary>

An `if` statement is usually placed directly after `else`:

```cpp
if (a)
{
   std::cout << "A" << std::endl;
}
else if (b)
{
   std::cout << "B" << std::endl;
}
else if (c)
{
   std::cout << "C" << std::endl;
}
```
</details>

### 14. Early return

Try to represent this code as an equivalent `if`-`else` chain.
How can this code be written using an early return / guard clause?

```cpp
if (a)
{
   std::cout << "A" << std::endl;
}
else
{
   std::cout << "After A" << std::endl;

   if (b)
   {
       std::cout << "B" << std::endl;
   }
   else
   {
       std::cout << "After B" << std::endl;

       if (c)
       {
           std::cout << "C" << std::endl;
       }
       else
       {
           std::cout << "After C" << std::endl;
       }
   }
}
```

<details>
<summary>Answer (chain)</summary>

This code cannot be represented as an `if`-`else` chain without duplicating code.
There is nowhere to put `After B` and `After C` so that they execute according to the same rules without duplicating them.
You could duplicate them, as shown below, but that would make the code harder to maintain:

```cpp
if (a)
{
   std::cout << "A" << std::endl;
}
else if (b)
{
   std::cout << "After A" << std::endl;
   std::cout << "B" << std::endl;
}
else if (c)
{
   std::cout << "After A" << std::endl;
   std::cout << "After B" << std::endl;
   std::cout << "C" << std::endl;
}
else
{
   std::cout << "After A" << std::endl;
   std::cout << "After B" << std::endl;
   std::cout << "After C" << std::endl;
}
```
</details>

<details>
<summary>Answer (guard clause / early return)</summary>

1. Put this code in a function.
2. Add a `return` statement to each `if` block.
3. Then the `else` statements and blocks can be removed.

```cpp
#include <iostream>

void f(bool a, bool b, bool c)
{
   if (a)
   {
       std::cout << "A" << std::endl;
       return;
   }
   std::cout << "After A" << std::endl;

   if (b)
   {
       std::cout << "B" << std::endl;
       return;
   }
   std::cout << "After B" << std::endl;

   if (c)
   {
       std::cout << "C" << std::endl;
       return;
   }
   std::cout << "After C" << std::endl;
}

int main()
{
   // Assumes that a, b, and c were declared earlier ...
   f(a, b, c);
}
```
</details>

<details>
<summary>Why use this guard clause / early return?</summary>

- To move error handling to the top of the function and the main logic below it.
  This makes it clear that the main logic depends on the conditions checked
  during error handling (the contract).
- It removes unnecessary nesting of conditions;
- It promotes locality between error checks and their handling.

Example code without using a guard clause / early return:
```cpp
void sendWelcomeEmail(User* user)
{
   // The conditions are nested one inside another.
   if (user != nullptr)
   {
       if (user->IsActive)
       {
           if (user->EmailConfirmed)
           {
               // The code that performs the action is hidden in the middle of the function.
               std::cout << "Sending email to " << user->email << std::endl;
           }
           else
           {
               std::cout << "Email not confirmed." << std::endl;
           }
       }
       else
       {
           std::cout << "User is not active." << std::endl;
       }
   }
   // Locality is not preserved:
   // the handling is separated in the source code from the associated check.
   else
   {
       std::cout << "User not found." << std::endl;
   }
}
```

The same code using a guard clause / early return:
```cpp
void sendWelcomeEmail(User* user)
{
   // A block can be used to delimit the contract
   // (the conditions required to perform the main action),
   // or it can be moved to its own function.
   {
       // Locality is preserved: conditions are next to their handling.
       if (user == nullptr)
       {
           std::cout << "User not found." << std::endl;
           return;
       }
   
       if (!user->isActive)
       {
           std::cout << "User is not active." << std::endl;
           return;
       }
   
       if (!user->emailConfirmed)
       {
           std::cout << "Email not confirmed." << std::endl;
           return;
       }
   }

   // The main code comes after all checks rather than in the middle.
   std::cout << "Sending email to " << user->email << std::endl;
}
```
</details>

### 15. A complex example
```cpp
int i = 0;
while (true)
{
   if (i == 4)
   {
       std::cout << "ERROR: Should not happen" << std::endl;
       break;
   }
   if (i == 3)
   {
       std::cout << "Exit" << std::endl;
       break;
   }
   if (i == 0)
   {
       std::cout << "Increase by 2 on first iter" << std::endl;
       i += 2;
       continue;
   }

   std::cout << "Increase by 1 normally" << std::endl;
   i++;
}
```

<details>
<summary>What do <code>break</code> and <code>continue</code> do?</summary>

`break` stops the loop; execution continues with the first statement after it.

`continue` starts the next iteration of the loop (the remaining statements in the loop body are not executed for that iteration).
</details>

<details>
<summary>Answer</summary>

"Increase by 2 on first iter" will be printed in the first loop iteration; `i++` will not execute because `continue` skips it.

"Increase by 1 normally" will be printed in the second loop iteration, 
after all `if` checks have failed.

"Exit" will be printed in the third iteration, while the `i == 0` check and the `i++` statement will not execute,
because `break` stops the loop.

```
Increase by 2 on first iter
Increase by 1 normally
Exit
```
</details>

### 16. `return` from inside `while`
```cpp
int F()
{
   while (true)
   {
       if (true)
       {
           return 0;
       }
       break;
   }
   return 1;
}
```

<details>
<summary>Answer</summary>

The function will return `0`. `break` and `return 1` will not execute.
</details>

### 17. An example of using `if`
```cpp
#include <iostream>
#include <cassert>

struct Result
{
   bool isDenominatorZero;
   // Should only be read if there is no error.
   int result;
};

Result ceilingDivide(int numerator, int denominator)
{
   if (denominator == 0)
   {
       return {
           .isDenominatorZero = true,
           .result = 0,
       };
   }

   int value = (numerator + denominator - 1) / denominator;
   return {
       .isDenominatorZero = false,
       .result = value,
   };
}

int main()
{
   {
       int totalStudents { 25 };
       int studentsPerTable { 2 };
       Result result { ceilingDivide(totalStudents, studentsPerTable) };
       if (!result.isDenominatorZero)
       {
           int numTablesNeeded = result.result;
           std::cout << "Number of tables needed is " << numTablesNeeded << std::endl;
       }
       else
       {
           std::cout << "Can't seat any students if no students are seated per table" << std::endl;
           assert(studentsPerTable == 0);
       }
   }
   {
       Result result { ceilingDivide(30, 0) };
       if (result.isDenominatorZero)
       {
           std::cout << "Could not divide" << std::endl;
       }
       else
       {
           std::cout << "The result is " << result.result << std::endl;
       }
   }
}
```

## Refactoring

Refactor this code using a guard clause / early return.

```cpp
#include <iostream>

int main()
{
    int number = 10;

    if (number == 5)
    {
        std::cout << "The number is 5" << std::endl;
    }
    else
    {
        std::cout << "The number is not 5" << std::endl;

        if (number % 2 == 1)
        {
            std::cout << "The number is not divisible by 2" << std::endl;
        }
        else
        {
            std::cout << "The number is divisible by 2" << std::endl;

            if (number == 6)
            {
                std::cout << "The number is 6" << std::endl;
            }
        }
    }
}
```

## Complex logical expression

Here is the starter code:

```cpp
#include <iostream>

int main()
{
    int apples;
    int pears;
    int oranges;

    std::cout << "Apples:";
    std::cin >> apples;

    std::cout << "Pears:";
    std::cin >> pears;

    std::cout << "Oranges:";
    std::cin >> oranges;

    // ...

    return 0;
}
```

- If the number of apples is greater than 5, the number of pears is less than 8,
  and the number of oranges is exactly 2 times the number of apples,
  print "Hello".

- Create a temporary variable containing the result of the expression.
  Check it in an `if` statement.

- Create a temporary variable for each subcondition.
  Calculate the overall condition using these subconditions.

- Declare the temporary subcondition variables in a block
  so that they are not visible outside the block.
  Use the outer condition outside the block (the block exists to initialize the overall condition).

  You may also turn this block into a function.

- Refactor the 3 variables holding fruit quantities into a single structure (`FruitCounts`)
  with 3 fields, one for each fruit type.
  Rewrite the code so this structure is used everywhere.
