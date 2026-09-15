---
title: "Practice with Simple Problems"
---
# Practice with Simple Problems

## What you will develop in this assignment

This document contains problems that I recommend solving manually to reinforce basic skills:
- Modelling real-world situations and problem conditions in a program;
- Analysing problems and planning the steps of a solution algorithm;
- Defining an algorithm interface for solving a problem;
- Implementing a function interface based on the algorithm interface, 
  choosing types for parameters and the return value;
- Implementing the algorithm steps as program instructions;
- Separating data definition in `main` from the use of that data in a separate algorithm function;
- Creating abstractions for grouping data.

## Example of completing a practice assignment

### Problem

There are X eggs and Y ml of kefir in the fridge.
To make 8 pancakes, you need 1 egg and 250 ml of kefir.
Determine *how many pancakes can be made from the current ingredients*
using only whole quantities of ingredients (you cannot use half an egg).
Afterwards, *remove* the used ingredients from the fridge.

### 1. Thinking through the algorithm

For example, if there are *3 eggs and 500 ml of kefir*, you can take 1 egg and 250 ml of kefir twice,
leaving 1 egg unused.

In other words, we use 1 egg and 250 ml of kefir as many times as possible,
because those are the quantities required for one portion.
Any remaining ingredients stay in the fridge.

With 3 eggs and 500 ml of kefir, we can make 2 portions,
even though the eggs would be enough for 3 portions.

What if we have *2 eggs and 750 ml of kefir*?
Then all the eggs can be used, but an extra 250 ml of kefir will remain.
Although there is enough kefir for 1 more portion, there are not enough eggs,
so we leave it in the fridge.

What if we have *1 egg and 300 ml of kefir*?
There is enough of both ingredients for 1 portion, after which 50 ml of kefir remains in the fridge.
That is not enough for another portion, but it does not matter,
because we cannot make another portion anyway.

What if there are no eggs or no kefir?
Then we can make 0 portions.

<details>
<summary>
So, the key insight of the problem
</summary>

We make the maximum number of portions allowed by the ingredient that is in the shortest supply.

In other words, we choose the smaller of the two possible numbers of portions.
Choosing the larger number would require more of the other ingredient than we have.
</details>

### 2. Formal definition of the algorithm steps

Find the number of portions for which there are enough eggs: $`a = X`$.

Find the number of portions for which there is enough kefir: $`b = floor(\frac{Y}{250})`$, where $`250`$ is the amount of kefir required for 1 portion.
$`floor`$ discards the fractional part because we count only complete portions.
This is represented by the integer part of the result.
For example, when $`Y = 300`$, the integer part is $`1`$,
because $`250`$ fits into $`300`$ once, 
leaving $`50`$ ml of kefir, which we ignore by using $`floor`$.

Find the minimum of $`a`$ and $`b`$ and call it $`p`$. 
$`p`$ is the number of portions we can make.

$`p * 8`$ is the answer to the problem ($`8`$ is the number of pancakes per portion). 
But we still need to remove the used ingredients from the fridge.

Remove the used ingredients from the fridge: $`p * 1`$ eggs and $`p * 250`$ ml of kefir.

### 3. Formal definition of the algorithm interface

An interface describes what an algorithm depends on and the form in which it provides its answer.

Our algorithm depends on the state of the fridge ($`X`$ and $`Y`$).
If the algorithm is generalised slightly, we can also introduce parameters for the amounts of eggs and kefir
needed for one portion of pancakes.

The algorithm produces a number represented by the expression $`p * 8`$ and changes the state of the fridge that was passed in.

### 4. Interface implementation

The function that implements the algorithm needs to receive the fridge as an argument.
Which fridge it receives must be controlled by the **user calling the function**.
Therefore, the fridge will be a function parameter.

The function will:
- Calculate the number of pancakes;
- Update the fridge.

The function will return the number of pancakes made.
This is **its return value**.

Updating the fridge is a **side effect** of the function.
If a function updates something instead of only returning an answer,
the thing it updates must be passed to it **by pointer**.

Standard function syntax:
```cpp
возвращаемый_тип имя(тип_параметра_1 имя_параметра_1, тип_параметра_2 имя_параметра_2)
```

The function can be named, for example, `приготовить_панкейки`. 

**return type -> type of the return value -> type of the "number of pancakes" -> `int`**

One parameter will be the **fridge** (as explained above).
The fridge type will be `Холодильник` (more on it later).
Let us call the parameter `считать_ингредиенты_холодильник`.

The second parameter will also represent a **fridge**—the one from which we will remove the ingredients.
The fridge type will be `Холодильник*`.
A pointer is used because we will change its data within the function.
Let us call the parameter `вытащить_ингредиенты_холодильник`.

The initial version of the interface:
```cpp
int приготовить_панкейки(
    Холодильник считать_ингредиенты_холодильник,
    Холодильник* вытащить_ингредиенты_холодильник)
```

However, it is logical to expect that *we will remove ingredients from the same fridge
that we use to determine the number of portions*.
Moreover, passing a different fridge would probably be a logical error.
Because **data can be read through a pointer as well as written**,
we can pass just 1 pointer parameter:

```cpp
int приготовить_панкейки(Холодильник* холодильник)
```

We will also change the names to follow English naming conventions:

```cpp
int cook_pancakes(Fridge* fridge)
```

In addition, we could add configuration for the recipe:
- How many pancakes are produced by 1 portion of the recipe;
- How many ml of kefir are needed for 1 portion of the recipe.

We can pass these as 2 more parameters:
```cpp
int cook_pancakes(Fridge* fridge, int pancakesPerPortion, int kefirMlUsedPerPortion)
```

This can also be represented by a single abstraction that contains both values.
Then we can pass all the settings in one parameter.

```cpp
struct PancakesRecipeConfiguration
{
    int pancakesPerPortion;
    int kefirMlUsedPerPortion;
};
int cook_pancakes(Fridge* fridge, PancakesRecipeConfiguration config)
```

### 5. Modelling the problem

We have not modelled the fridge yet.
We need to create a `Fridge` structure that represents an **abstraction of the fridge's state**.
We are interested only in the **amount of each ingredient type specified in the problem**;
we can ignore the other data about the fridge because it is irrelevant to this problem.

What data type should the number of eggs have? Clearly, it should be an integer. 
The simplest choice is `int`, but another type can also be used, 
such as `uint32_t`, `uint16_t`, `int16_t`, `size_t`, and others.
Technically, to represent the data correctly in a program,
it would be more appropriate to use an unsigned type,
because the number of eggs cannot be negative.
We will use `int` because it is simpler.

What data type should the amount of kefir have? This is more debatable.
It would be logical to use `float` because the number of millilitres of kefir may not be a whole number.
However, I will use `int` to simplify calculations.
We will assume that kefir is always poured in whole-millilitre units.

```cpp
struct Fridge
{
    int eggCount;
    int kefirMl;
};
```

The same analysis applies to `PancakesRecipeConfiguration`,
shown above.
I chose `int`s for simplicity.


Now we need to model a simple program setup
and a recipe configuration.
```cpp
// Создаем основную функцию. 
int main()
{
    // В ней нужно будет создать холодильник, заполнить его продуктами,
    Fridge fridge{
        .eggCount = 3,
        .kefirMl = 500,
    };

    // после чего сделать панкейки.
    // Для этого необходимо также создать конфигурацию рецепта.
    PancakesRecipeConfiguration config{
        .pancakesPerPortion = 8;
        .kefirMlUsedPerPortion = 250;
    };
    // Готовим панкейки:
    int preparedPancakeCount{ cook_pancakes(&fridge, config) };

    // После приготовления панкейков, печатаем, сколько их приготовили и сколько осталось продуктов.
    std::cout 
        << "Cooked " 
        << preparedPancakeCount 
        << " pancakes" 
        << std::endl;
    std::cout 
        << "Left "
        << fridge.eggCount 
        << " eggs and " 
        << fridge.kefirMl
        << "ml of kefir in the fridge"
        << std::endl;
}
```

### 6. Function implementation

Translate the formal steps of the algorithm into instructions for the function:
1. $`a = X`$ - `int a { fridge->eggCount };`
2. $`b = floor(Y / 250)`$ - `int b { fridge->kefirMl / config.kefirMlUsedPerPortion };` 
   (uses division of `int`s, which rounds down)
3. $`p = min(a, b)`$ - `int p { min(a, b) };` 
   (`min` is a built-in function; without it, you would have to use `if`)
4. $` p * 8 `$ is the result - `return p * config.pancakesPerPortion;`
5. Update the fridge - `fridge->eggCount -= p; fridge->kefirMl -= p * config.kefirMlUsedPerPortion;`

The fridge must be updated before `return`, 
because `return` ends the function immediately.
Instructions after it will not be executed.
This issue can be avoided by creating a temporary variable for the result, 
or by updating the fridge before calculating `p * 8`.

```cpp
int cook_pancakes(Fridge* fridge, PancakesRecipeConfiguration config)
{
    int a { fridge->eggCount };
    int b { fridge->kefirMl / config.kefirMlUsedPerPortion };
    int p { min(a, b) };
    int result { p * config.pancakesPerPortion };
    fridge->eggCount -= p; 
    fridge->kefirMl -= p * config.kefirMlUsedPerPortion;
    return result;
}
```

### 7. Complete program

In addition to the code described above, you need to include a couple of headers 
to use `min` and `std::cout <<`.
These are `#include <cmath>` and `#include <iostream>` respectively.

```cpp
#include <cmath>
#include <iostream>

struct Fridge
{
    int eggCount;
    int kefirMl;
};

struct PancakesRecipeConfiguration
{
    int pancakesPerPortion;
    int kefirMlUsedPerPortion;
};

int cook_pancakes(Fridge* fridge, PancakesRecipeConfiguration config)
{
    int a { fridge->eggCount };
    int b { fridge->kefirMl / config.kefirMlUsedPerPortion };
    int p { min(a, b) };
    int result { p * config.pancakesPerPortion };
    fridge->eggCount -= p; 
    fridge->kefirMl -= p * config.kefirMlUsedPerPortion;
    return result;
}

int main()
{
    Fridge fridge{
        .eggCount = 3,
        .kefirMl = 500,
    };

    PancakesRecipeConfiguration config{
        .pancakesPerPortion = 8;
        .kefirMlUsedPerPortion = 250;
    };
    int preparedPancakeCount{ cook_pancakes(&fridge, config) };

    std::cout 
        << "Cooked " 
        << preparedPancakeCount 
        << " pancakes" 
        << std::endl;
    std::cout 
        << "Left "
        << fridge.eggCount 
        << " eggs and " 
        << fridge.kefirMl
        << "ml of kefir in the fridge"
        << std::endl;
}
```

## Practice tasks

- **Battery charge.** A phone has a charge level expressed as a percentage.
  Each minute on the charger adds 1%, but the charge cannot go above 100%.
  Write a function that charges the battery and returns nothing —
  its only result is changing the state of the battery.

  <details>
  <summary>
  Possible solution
  </summary>

  ```cpp
  struct Battery
  {
      int chargePercent;
  };

  void charge(Battery* battery, int minutes)
  {
      battery->chargePercent = std::min(100, battery->chargePercent + minutes);
  }
  ```

  The return type is `void` because the algorithm has nothing to return as a result:
  the result of the function is the side effect, updating the battery through the pointer.
  `std::min` caps the charge at 100, even if `chargePercent + minutes` is greater than 100.

  Usage from `main`:
  ```cpp
  Battery battery{ .chargePercent = 40 };
  charge(&battery, 90);
  std::cout << battery.chargePercent << std::endl; // 100
  ```
  </details>

- **Time normalization.**
  A time value was stored as 4 hours, 138 minutes, 250 seconds —
  this is an inconvenient way to store time: a minute cannot contain more than 60 seconds,
  and an hour cannot contain more than 60 minutes.
  Write a function that returns the same time in normalized form.
  The original time must not change.

  <details>
  <summary>
  Possible solution
  </summary>

  ```cpp
  struct Time
  {
      int hours;
      int minutes;
      int seconds;
  };

  Time normalized(Time time)
  {
      int totalSeconds{ time.hours * 3600 + time.minutes * 60 + time.seconds };
      return Time{
          .hours = totalSeconds / 3600,
          .minutes = totalSeconds / 60 % 60,
          .seconds = totalSeconds % 60,
      };
  }
  ```

  The return type is a struct because the answer consists of three numbers.
  The parameter is passed by value, so the function does not modify the original in `main` —
  it does not overwrite anything; it computes and returns a new value.
  Division and remainder separate complete units from the remainder that does not fit into them:
  For 4 hours, 138 minutes, 250 seconds, the function gives 6 hours, 22 minutes, 10 seconds.
  </details>

- **Pouring water.**
  There are two bottles, each with its own capacity and current amount of water.
  Write a function that pours water from the first bottle into the second:
  you cannot pour more into the second bottle than its free space allows,
  and you cannot pour more out of the first bottle than it contains.
  The function should return how many milliliters were poured,
  and the amount of water in both bottles should be updated.

  <details>
  <summary>
  Possible solution
  </summary>

  ```cpp
  struct Bottle
  {
      int capacityMl;
      int ml;
  };

  int free_space(Bottle bottle)
  {
      return bottle.capacityMl - bottle.ml;
  }

  int pour(Bottle* from, Bottle* to)
  {
      int transferredMl{ std::min(from->ml, free_space(*to)) };
      from->ml -= transferredMl;
      to->ml += transferredMl;
      return transferredMl;
  }
  ```

  The algorithm is implemented with two functions: the helper `free_space` computes the free space,
  and the main `pour` calls it internally.
  `pour` takes **two pointers** because it modifies **two different objects**,
  and returns the transferred amount in addition to that side effect.
  `free_space` does not change anything, so passing the bottle by value is sufficient.
  </details>

- **Lever.** A lever has two positions: `0` and `1`.
  Write functions that set the lever to `0` and `1`.
  If it is already at the requested value, nothing changes.
  Also write a function that toggles it to the opposite value.

- **Maximum of three numbers.** The built-in `std::max` takes only two numbers.
  Write a function that returns the largest of three numbers.

- **Calorie content of a dish.**
  A dish contains specified amounts of protein, fat, and carbohydrates in grams.
  Its calorie content is 4 kcal per gram of protein, 9 kcal per gram of fat, 4 kcal per gram of carbohydrates.
  Compute the calorie content of the dish.

- **Average temperature.**
  A sensor took two readings over the course of a day.
  Compute the average temperature — the result may be fractional.
  Be careful: if you divide one `int` by another,
  the fractional part will be lost before the result is stored.

- **Packing boxes.**
  A warehouse holds `X` identical items, and one box fits `Y` items.
  Compute the number of full boxes and the number of leftover items.

- **Hero damage.**
  A game hero has current and maximum health.
  Taking damage reduces current health, but current health cannot drop below zero.
  Write a function that applies damage to the hero.

- **Hero level-up.**
  For the same hero, when the hero levels up, the maximum health increases by 10,
  and the current health is restored to the new maximum.
  Write a level-up function.

- **Piggy bank.**
  A piggy bank holds `X` dollars and `Y` cents (1 dollar = 100 cents),
  and `A` additional dollars and `B` cents are added to it.
  The piggy bank must never contain more than 99 cents — any excess is carried over to dollars.
  Write a function that tops up the piggy bank.

- **Car tuning.**
  A car has a price and an engine with a given power output (horsepower).
  After tuning, the engine power increases by a given number of horsepower,
  and the price of the car increases by 1000 dollars for each additional horsepower.
  Write a function that tunes the car.

- **Swapping values.**
  Write a function that swaps the values of two variables defined in `main`.
  Recall the value-swapping example from the variables lab:
  you cannot do it without a temporary variable.

- **Sharing candies.**
  `N` candies are shared equally among `M` children, and the remainder goes to the youngest child.
  Compute how many candies each child gets, and how many the youngest gets in total (equal share plus remainder).

- **Clamping to a range.**
  A parameter has an allowed range of values — from `low` to `high`.
  Write a function that clamps any value to the allowed range.
  The range itself must not change.

- **Printing a student record.**
  A student has a student ID, a year of study, and a GPA (average grade).
  Write a function that prints all student data to the screen.
  The function does not modify the student data.

- **Three numbers in ascending order.**
  Three numbers are given. Write a function that returns them in ascending order.
  Hint: the smallest and the largest are found using nested `std::min` and `std::max`,
  and the middle one is computed as the sum of all three minus the smallest and the largest.

- **Board squares.**
  The squares of an 8×8 board are numbered from 0 to 63, left to right, top to bottom.
  Write functions that convert a square number into its row and column
  and vice versa — convert a row and column back into the square number.

- **Duration in seconds.**
  Write a function that converts a duration given in hours, minutes, and seconds
  into the total number of seconds.

- **Painting a room.**
  A room has length, width, and height.
  Compute the area of all four walls of the room (the floor and the ceiling do not need painting)
  and the cost of painting at a given price per square meter.

- **Discounted subscription.**
  A subscription plan is defined by a price per month and a discount percentage.
  Compute the cost of a subscription for a given number of months with this plan.

- **Trip cost.**
  The trip distance, the fuel consumption of a car per 100 km, the price of a liter of fuel,
  the number of nights in a hotel, and the price per night are given. The car makes a round trip — it drives there and back.
  Compute the total cost of the trip.

- **Elevator trips.**
  An elevator fits `K` people, and `N` people are waiting on a building floor to board the elevator.
  Compute how many trips the elevator will make
  if the last trip may be partially full.

- **Distance between points.**
  Two points in the plane with integer coordinates are given.
  Compute the distance between them: the square root of the sum of the squares of the differences in their coordinates.
