# Practice Modeling a Simple Problem

- [Video](https://www.youtube.com/watch?v=6JtlzvwhHr0&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=29)

## Task

The menu contains 3 items: a drink, a first course, and a second course.
Each of them has a different price (for example: 10, 20, 30).

A customer can order any quantity of each of these items.
There are 2 customers, and each orders a different combination of items.

1. Represent this situation in a program.
   Display the cost of each customer's order.

   <details>
   <summary>I am having trouble understanding how to represent this</summary>

   You have 2 customers. 
   Each has a quantity for every type of item. 
   That makes 6 variables.
   Set the values of the variables according to the customer's order.
   For example:
   
   ```csharp
   int client1_drink = 100; // 100г напитка
   int client1_first = 0; // нет первого
   int client1_second = 250; // 250г второго
   
   int client2_drink = 0; // 0 напитка
   int client2_first = 300; // 300г первого
   int client2_second = 0; // 0 второго
   ```
   </details>

   <details>
   <summary>Calculating the cost</summary>

   ```csharp
   int client1_total = client1_drink * 10 + client_first * 20 + client_second * 30;
   ```
   </details>

2. Put the code for each individual customer into separate blocks.
   Within the blocks, use variables with the same names.

3. Create a structure to hold the prices.
   Use a variable of this type to refer to item prices instead of referring to each price directly.
   This way, all prices will be logically grouped in one variable.

4. Create a structure to represent a customer's choice.

5. Write a function that calculates a customer's total and takes prices and a customer's choice as parameters.

   <details>
   <summary>Why?</summary>
   
   To eliminate repeated code.
   </details>

   <details>
   <summary>How?</summary>
   
   Look at the code that calculates a customer's total to determine what it depends on.
   It depends on prices, so prices will be the first parameter.
   
   Next, what changes each time this code is repeated?
   The customer's choice changes, so it will be the next parameter.
   
   Finally, what should this piece of code return?
   It should return the total cost.
   Therefore, the return type will be `int`.
   
   ```cpp
   int customerTotal(Prices prices, Choices choices)
   {
       // ...
   }
   ```
   </details>
