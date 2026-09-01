# Objects

- [Video (theory)](https://www.youtube.com/watch?v=8xXxJ0PZutE&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=9).
- [Video (example walkthrough)](https://www.youtube.com/watch?v=OvH8meqCnik&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=18).

## Concepts

- Object
- rvalue, lvalue
- Reference
- `std::array`

## Tasks

Which types and objects are present here? List them all.

```cpp
#include <array>

struct Leg
{
    int length;
};

struct Arm
{
    int power;
};

struct Person
{
    std::array<Leg, 2> legs;
    Arm arms[2];
};

int main()
{
    Person person;
}
```

<details>
<summary>Hint (object) 1</summary>
An object is a piece of memory of a particular type.
</details>

<details>
<summary>Hint (object) 2</summary>
An object can be of any type.
</details>

<details>
<summary>Hint (fields) 1</summary>

Recall the syntax for declaring fields in structures.
</details>

<details>
<summary>Hint (fields) 2</summary>

The syntax for declaring fields is similar to the syntax for declaring variables.
```
тип имя;
```
</details>

<details>
<summary>Hint (type) 1</summary>
A structure is a user-defined type.
</details>

<details>
<summary>Hint (type) 2</summary>

Types have names.
A type name is not necessarily a single identifier (word); a type can have a more complex name.

For example, `std::vector<int>` is also a type name.
</details>

<details>
<summary>Hint (fields) 3</summary>

Field definitions are not objects.

Fields are objects only as part of an existing object.
That object must have the user-defined type in which the field is declared.

Standard types (such as `int`) do not contain fields.
Only user-defined types (structures) can declare fields.
</details>

<details>
<summary>Hint (array) 1</summary>
Arrays store several objects.
</details>

<details>
<summary>Hint (array) 2</summary>
C-style arrays are not objects in the ordinary sense of the word.
They have peculiarities.
</details>

<details>
<summary>Answer</summary>

Objects:
```
person
person.legs
person.legs[0]
person.legs[1]
person.legs[0].length
person.legs[1].length
person.arms[0]
person.arms[1]
person.arms[0].power
person.arms[1].power
```

Types:
```
Person
Leg
Arm
int
std::array<Leg, 2>
```
</details>
