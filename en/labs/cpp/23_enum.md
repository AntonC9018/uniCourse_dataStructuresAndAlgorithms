# `enum`

- [Video](https://www.youtube.com/watch?v=Kbc6iaN3M6A&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=17).
- [Information](../../../en/05a_programming_fundamentals/04_enum.md)

## What is the value of `Test::b`, and why?

1.  ```cpp
    enum Test
    {
        a = 1,
        b = 2,
    };
    ```

2.  ```cpp
    enum Test
    {
        a = 1,
        b,
    };
    ```

3.  ```cpp
    enum Test
    {
        a,
        b,
    };
    ```

4.  ```cpp
    enum Test
    {
        a = -1,
        b,
    };
    ```

5.  ```cpp
    enum Test
    {
        a = (5 + 10 * 5) / 5,
        b,
    };
    ```

6.  ```cpp
    enum Test
    {
        other = 5,
        a = other + 6,
        b,
    };
    ```

7.  Write the answer as an integer and as a character.

    ```cpp
    enum Test
    {
        a = '5',
        b = '7',
    };
    ```

8.  Write the answer as an integer and as a character.

    ```cpp
    enum Test
    {
        a = '5',
        b,
    };
    ```

9.  Write the answer as an integer and as a character.

    ```cpp
    enum Test
    {
        a = 'b',
        b,
    };
    ```

9.  Write the answer as an integer.

    ```cpp
    enum Test
    {
        a = 'a' + '1',
        b,
    };
    ```


## Why?

Why is `enum class` better than `enum`?
List the reasons.
(The answers are in the video.)


## Defusing a bomb.

Each bomb has 3 wires, all of different colors: red, yellow, and green.
Write a program that determines which wire must be cut to disable the bomb's timer.

The correct wire can be determined from the bomb's characteristics.
The characteristics are as follows:
- One of the portraits: Lenin, George Washington, Hitler;
- One of the bulb colors: blue, white, red;
- One of 2 switch states (on or off);
- The value on the dial, from 1 to 100.

The required wire can be determined using the following rules:
1. If the portrait is Lenin, the bomb will not explode; nothing needs to be cut;
2. A value is associated with the bulb color. Blue is 11, white is 15, red is 35.
   If the value on the dial is less than this value, cut the red wire.
3. If the portrait is Hitler, the values associated with the bulb colors are shifted by 1 relative to the previous rule. 
   That is, blue has the value of white (15), white has the value of red (35), and red has the value of blue (11).
4. If the value associated with the bulb color equals the value on the dial, cut the green wire.
5. Otherwise, cut the yellow wire.
5. If the switch is on, the wire to be cut is shifted backward by 1.
   Instead of green, cut yellow; instead of yellow, cut red; instead of red, cut green.
6. If the dial value is divisible by 4, 
   shift the required wire forward by the dial value.

Implement the main logic as a function
that takes the bomb's characteristics as parameters
and returns the required action (which wire to cut, or whether anything needs to be cut at all).
Write tests in `main` using `assert`.
You may add keyboard input, but it is not required.

Recommendations:
- Use `enum class` where there is a fixed set of possible values. 
  For example, the bulb color, the person in the portrait, the wire color, and the switch position.
- If there are only 2 states, you do not need an `enum`; you can model the situation with `bool`.
- If a value is associated with every member of an `enum`, 
  use a lookup table or `switch` to associate the values with the members.
  You can also assign that value to the member itself, but do so only if
  the code does not depend on their values being 1 apart.
- Convert between a particular `enum class` type and `int` using `static_cast`.
- Implement forward or backward shifts with modular arithmetic.
- Use an early return when a decision can be made sooner.

> Once you have done it, make me a PR with test cases :)
> 
> I have not written this program myself.


<details>
<summary>Modular arithmetic?</summary>

The idea is to return to the beginning when moving past the end,
and to move to the end when moving backward past the beginning.
It is like a snake going off the right edge and appearing on the left in the same row.

To do this, use the remainder operator.
It effectively ignores complete cycles through a range,
such as the indices of an array.

For an array with 3 elements, to advance one position
and return to the start after reaching the end, take
the remainder after dividing the next index by 3.

```
int i = 0;
i = (i + 1) % 3; // i == 1
i = (i + 1) % 3; // i == 2
i = (i + 1) % 3; // i == 0
i = (i + 1) % 3; // i == 1
i = (i + 1) % 3; // i == 2
```

If the offset is greater than 3, 
the remainder operator absorbs all extra moves through the whole range of values.

```
int i = 0;
i = (i + 12) % 3; // i == 0
i = (i + 13) % 3; // i == 1
```

There is one problem with using the same approach to move backward.
The `%` operator can produce a negative result for a negative dividend.
```
int i = 1;
i = (i - 1) % 3; // i == 0
i = (i - 1) % 3; // i == -1
i = (i - 1) % 3; // i == -2
i = (i - 1) % 3; // i == 0 
```

This can be avoided by adding 3 before taking the remainder,
because the extra 3 will be removed by the remainder operator.
```
int i = 1;
i = (i - 1 + 3) % 3; // i == 0
i = (i - 1 + 3) % 3; // i == 2
i = (i - 1 + 3) % 3; // i == 1
i = (i - 1 + 3) % 3; // i == 0
```

This works only if the number being subtracted is smaller than the divisor (3).
To handle any offset, first calculate the remainder. If the result is negative, it will be no less than -2;
then add 3 to make it non-negative, and take the remainder again
to remove the added 3 if the first step already produced a positive result.

```
int i = 1;
int offset = -5; // 1 целый массив назад, и еще 2 позиции
i = (((i + offset) % 3) + 3) % 3; // 2

// _0_   offset = -5, i = 1  > -3 = нет эффекта
// 0__   offset = -4         >
// __0   offset = -3         >
// _0_   offset = -2
// 0__   offset = -1
// __0   offset = 0, i = 2
```

There are other approaches as well; see [the information](https://stackoverflow.com/questions/14997165/fastest-way-to-get-a-positive-modulo-in-c-c).

</details>


<details>
<summary>How do you indicate the absence of a value?</summary>

If the value is an enum, you can reserve a separate value for it.
Usually, such a member is named `None`.
You can make it the first member of the `enum`; then its value will obviously be 0.
If you need modular arithmetic for color values, it can be more convenient to give `None` a different value,
by placing `None` at the end of the `enum`, or by setting it manually to, for example, -1.
However, you can also handle edge cases with additional checks, leaving `None` at 0.

Alternatively, you can use a structure for the answer with a separate `bool` field
that indicates whether any wire needs to be cut at all.
```cpp
enum class BombWireColor
{
    Red,
    Yellow,
    Green,
};

struct BombDefusionDecision
{
    bool shouldDefuse;
    BombWireColor wireColor;
};

BombDefusionDecision decideBombDefusion(BombCharacteristics bomb)
{
    if (bomb.portrait == Portrait::Lenin)
    {
        BombDefusionDecision result{};

        // После {} и так false.
        // result.shouldDefuse = false;

        return result;
    }

    // ...

    return {
        .shouldDefuse = true,
        .wireColor = BombWireColor.Green,
    };
};

int main()
{
    BombDefusionDecision decision = decideBombDefusion({ ... });
    if (decision.shouldDefuse)
    {
        std::cout << "Cutting the " << getWireColorString(decision.wireColor) << " wire" << std::endl;
    }
}
```

You can also use `std::optional`.
</details>
