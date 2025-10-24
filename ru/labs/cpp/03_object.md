# Лабораторная работа 3

Тема: *Объекты*.

Сопровождающее [видео](https://www.youtube.com/watch?v=8xXxJ0PZutE&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=9).

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
<summary>Подсказка (поля) 1</summary>

Вспомните синтаксис объявления полей в структурах.
</details>

<details>
<summary>Подсказка (поля) 2</summary>

Синтаксис объявления полей похож на синтаксис объявления переменных.
```
тип имя;
```
</details>

<details>
<summary>Подсказка (тип) 1</summary>
Структура - это пользовательский тип.
</details>

<details>
<summary>Подсказка (тип) 2</summary>

Типы имеют имя.
Имя типа - это не обязательно один идентификатор (слово), тип может иметь и более сложное имя.

Например, `std::vector<int>` - это все тоже имя типа.
</details>

<details>
<summary>Подсказка (поля) 3</summary>

Определения полей это не объекты.

Поля могут быть объектами только внутри уже имеющегося другого объекта.
Тип этого другого объекта должен быть тем, внутри которого объявлено поле (пользовательский тип).

Стандартные типы (такие как `int`) не содержат полей.
Только пользовательские типы (структуры) могут объявлять поля.
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

## Вопросы на понимание

1. ```cpp
   int& b = 5;
   ```

   <details>
   <summary>Ответ</summary>

   
   </details>

1. ```cpp
   int a = 5;
   int& b = a;
   std::cout << a << std::endl;
   std::cout << b << std::endl;
   ```

   <details>
   <summary>Ответ</summary>

   
   </details>


1. ```cpp
   int a = 5;
   int& b = a;
   b = 6;
   std::cout << a << std::endl;
   ```

2. ```cpp
   int a = 5;
   int& b = a;
   a = 6;
   std::cout << b << std::endl;
   ```

2. ```cpp
   int a = 5;
   int& b = 6;
   a = 7;
   std::cout << a << std::endl;
   std::cout << b << std::endl;
   ```

2. ```cpp
   int a = 5;
   int& b = a + 7;
   std::cout << a << std::endl;
   std::cout << b << std::endl;
   ```

2. ```cpp
   int a = 5;
   int& b = a + 7;
   std::cout << a << std::endl;
   std::cout << b << std::endl;
   ```

2. ```cpp
   int a = 5;
   int& b = a;
   b += 7;
   std::cout << a << std::endl;
   std::cout << b << std::endl;
   ```

2. ```cpp
   int a = 1;
   int b = 2;
   int& c = a;
   c = b;
   std::cout << a << std::endl;
   std::cout << b << std::endl;
   std::cout << c << std::endl;
   ```

2. ```cpp
   int a = 1;
   int* pa = &a;
   int& b = *pa;
   *pa = 2;
   b = 3;
   std::cout << a << std::endl;
   std::cout << b << std::endl;
   std::cout << *pa << std::endl;
   ```

2. ```cpp
   std::array<int, 2> arr{ 1, 2 };
   int* pa = a.data();
   int& b = *pa;
   pa += 1;
   std::cout << b << std::endl;
   ```

2. ```cpp
   std::array<int, 2> arr{ 1, 2 };
   std::array<int, 2> other{ 3, 4 };
   arr = other;
   ```

2. ```cpp
   std::array<int, 2> arr{ 1, 2 };
   std::array<int, 2> other{ arr };
   ```

2. ```cpp
   std::array<int, 2> arr{ 1, 2 };
   std::array<int, 2>& other{ arr };
   other[0] = 3;
   std::cout << arr[0] << std::endl;
   ```

2. ```cpp
   #include <iostream>

   struct A
   {
       int x;
       int y;
   };

   int main()
   {
       A a{ 1, 2 };

       A& ra = a;

       int& rx = ra.x;
       ra.x = 3;

       ra.y = 4;
       int& ry = ra.y;

       std::cout << rx << std::endl;
       std::cout << ry << std::endl;

       std::cout << ra.x << std::endl;
       std::cout << ra.y << std::endl;

       std::cout << a.x << std::endl;
       std::cout << a.y << std::endl;
   }
   ```
