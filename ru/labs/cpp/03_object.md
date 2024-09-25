# Лабораторная работа 3

Тема: *Объекты*.


## Задания

Какие тут типы, и какие тут объекты? перечислите все.

```cpp
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
<summary>Подсказка (объект) 1</summary>
Объект - это кусок памяти конкретного типа.
</details>

<details>
<summary>Подсказка (объект) 2</summary>
Объект может быть любого типа.
</details>

<details>
<summary>Подсказка (массив) 1</summary>
Массивы хранят в себе несколько объектов.
</details>

<details>
<summary>Подсказка (массив) 2</summary>
C массивы не являются объектами в обыкновенном смысле слова. 
У них есть странности.
</details>

