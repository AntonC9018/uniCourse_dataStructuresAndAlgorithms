# Лабораторная работа 3

Тема: *Объекты*.

Сопровождающее [видео](https://www.youtube.com/watch?v=8xXxJ0PZutE&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=9).

## Концепты

- Объект
- rvalue, lvalue
- Ссылка
- `std::array`

## Задания

Какие тут типы, и какие тут объекты? перечислите все.

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

<details>
<summary>Ответ</summary>

Объекты:
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

Типы:
```
Person
Leg
Arm
int
std::array<Leg, 2>
```
</details>

## Вопросы на понимание

> Там, где `main` не был расписан, код помещается в типичный основной файл:
> ```cpp
> #include <iostream>
> #include <array> // надо для std::array
>
> int main()
> {
>     // сюда
> }
> ```

1. ```cpp
   5 = 6;
   ```

   <details>
   <summary>Ответ</summary>

   `5` это rvalue, ему нельзя присваивать значение, потому что оно не является объектом (lvalue).
   </details>

1. ```cpp
   int* a = &5;
   ```

   <details>
   <summary>Ответ</summary>

   Нельзя брать адрес rvalue. 
   Можно брать адрес памяти только от lvalue (выражений, результат которого есть объект),
   поскольку числа сами по себе не хранятся в памяти.
   </details>

1. ```cpp
   int* a = &(5 + 6);
   ```

   <details>
   <summary>Ответ</summary>

   Аналогичная ситуация, `(5 + 6)` это rvalue.
   Невозможно взять адрес rvalue.
   </details>

1. ```cpp
   int& a = 5;
   ```

   <details>
   <summary>Ответ</summary>

   В ссылочную переменную можно записать только lvalue (ссылку на объект),
   поскольку `a` должна будет ссылаться по итогу на *ячейку* памяти (объект),
   а не просто на значение.
   </details>

1. ```cpp
   int a = 5;
   int& b = a;
   std::cout << a << std::endl;
   std::cout << b << std::endl;
   ```

   <details>
   <summary>Ответ</summary>

   Здесь, в `b` сохраняется *ссылка* на `a`.
   Под капотом, компилятор либо определит `b` как просто другое имя для `a`,
   либо по факту сохранит в `b` указатель на `a`. 

   При считывании, использование имени `b` аналогично использованию имени `a` 
   — они обе ссылаются на тот же объект.
   Их отличие в том, что `a` для создасться и *хранилище* при выполнении инструкции,
   то есть выделится стековая память под объект.

   Напечатается `5` 2 раза.
   </details>


1. ```cpp
   int a = 5;
   int& b = a;
   b = 6;
   std::cout << a << std::endl;
   ```

   <details>
   <summary>Ответ</summary>

   `a` тут перезапишется на `6` через имя `b`.
   </details>

2. ```cpp
   int a = 5;
   int& b = a;
   a = 6;
   std::cout << b << std::endl;
   ```

   <details>
   <summary>Ответ</summary>

   `a` перезаписывается напрямую. 

   Поскольку `b` является *ссылкой* на `a` (например, хранит в себе адрес `a`)
   считывание из `b` считает из `a`.
   </details>


2. ```cpp
   int a = 5;
   int& b = a + 7;
   std::cout << a << std::endl;
   std::cout << b << std::endl;
   ```

   <details>
   <summary>Ответ</summary>

   `a + 7` это rvalue, а не lvalue.
   Поскольку нельзя получить ссылку на rvalue, данный код не скомпилируется.
   </details>

2. ```cpp
   int a = 5;
   int& b = a;
   b += 7;
   std::cout << a << std::endl;
   std::cout << b << std::endl;
   ```

   <details>
   <summary>Ответ</summary>

   `b` как бы заменяется на `a`.
   Здесь обновится `a`.

   Так как `b` ссылается на `a`, напечатается то же для обеих переменных (12).
   </details>

2. ```cpp
   int a = 1;
   int b = 2;
   int& c = a;
   c = b;
   std::cout << a << std::endl;
   std::cout << b << std::endl;
   std::cout << c << std::endl;
   ```

   <details>
   <summary>Ответ</summary>

   `c = b` не перезаписывает ссылку. Ссылку невозможно перезаписать.

   В `c = b` вы как бы вставляете вместо `c` то, на что она ссылается (`a`),
   получая `a = b`, что перезаписывает `a` на значение из `b`, `2`.

   Выведется:
   ```
   2
   2
   2
   ```

   > Ссылки, в контраст с указателями, невозможно "перенаправить".
   </details>

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

   <details>
   <summary>Ответ</summary>

   `int& b = *pa;` здесь ссылка происходит из указателя.
   Все 3 имени теперь указывают на `a`.

   Выведется `3` 3 раза.
   </details>

2. ```cpp
   std::array<int, 2> arr{ 1, 2 };
   int* pa = a.data();
   int& b = *pa;
   pa += 1;
   std::cout << b << std::endl;
   ```
   <details>
   <summary>

   Что такое `data`?</summary>

   `a.data()` дает адрес первого элемента из массива 
   (`&a[0]`, `a[0]` дает ссылку, потом берем адрес из ссылки).
   </details>

   <details>
   <summary>Ответ</summary>

   `b` будет продолжать ссылаться на первый элемент, несмотря на то, что указатель обновился.
   </details>

2. ```cpp
   int a = 1;
   int& b = a;
   int* c = &b;
   *c = 2;
   std::cout << a << std::endl;
   ```

   <details>
   <summary>Ответ</summary>

   Из ссылки можно также получать адрес.
   Здесь, `*c = 2;` перезапишет `a`.
   </details>

2. ```cpp
   std::array<int, 2> arr{ 1, 2 };
   std::array<int, 2> other{ 3, 4 };
   arr = other;
   ```

   <details>
   <summary>Ответ</summary>

   Тут каждый элемент копириуется из `other` в `arr`.
   </details>

2. ```cpp
   std::array<int, 2> arr{ 1, 2 };
   std::array<int, 2> other{ arr };
   ```

   <details>
   <summary>Ответ</summary>

   Тут тоже, но при создании `other`.
   </details>

2. ```cpp
   std::array<int, 2> arr{ 1, 2 };
   std::array<int, 2>& other{ arr };
   other[0] = 3;
   std::cout << arr[0] << std::endl;
   ```

   <details>
   <summary>Ответ</summary>

   Здесь иллюстрируется создание ссылки на объект типа С++ массива.
   `other` как бы заменяете на `arr`.
   </details>

2. ```cpp
   #include <iostream>

   struct Position
   {
       int x;
       int y;
   };

   int main()
   {
       Position a{ .x = 1, .y = 2 };

       Position& ra = a;

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

   <details>
   <summary>Ответ</summary>

   Ссылки можно создавать на объекты внутри бОльших объектов.

   Тут везде напечатается `3` и `4`.
   </details>

2. ```cpp
   std::array<int, 2> arr{ 1, 2 };
   int& a = arr[0];
   a = 3;
   ```

   <details>
   <summary>Ответ</summary>

   `a = 3` перезаписывает первый элемент массива, 
   поскольку в `a` была сохранена ссылка на 1 элемент (на объект внутри массива).
   </details>

2. ```cpp
   int a = 1;
   int b = 2;
   int* pa = &a;
   int*& rpa = pa;
   pa = &b;
   *rpa = 3;
   std::cout << a << std::endl;
   std::cout << b << std::endl;
   ```

   <details>
   <summary>Ответ</summary>

   Можно создавать ссылки на указатели, потому что указатели тоже объекты (адреса в ячейках памяти).

   Тут мы перезаписывает адрес сохраненный в `pa` напрямую, 
   а считывает *адрес* по ссылке.

   `*rpa` -> `*pa` -> `*(&b)` -> `b`

   В `a` будет `1`, а в `b` будет `3`.
   </details>

2. ```cpp
   int a = 1;
   int b = 2;
   int* pa = &a;
   int*& rpa = pa;
   pa = &b;
   int& rb = *rpa;
   rb = 3;

   std::cout << a << std::endl;
   std::cout << b << std::endl;
   ```

   <details>
   <summary>Ответ</summary>

   Здесь иллюстрируется тот факт, что можно создавать ссылки исходя 
   из любых выражений, которые по итогу дают ссылку.

   `rb = 3` впишет `3` в `b`.
   </details>

2. ```cpp
   std::array<int, 2> arr { 1, 2 };
   int& arr1 = *(p.data() + 1)
   ```

   <details>
   <summary>Ответ</summary>

   Аналогично коду выше, только выражение сложнее.
   Тут в `arr1` попадает адрес `arr[1]`.
   </details>

2. ```cpp
   #include <iostream>

   void resetAmount(int& amount)
   {
       amount = 0;
   }
   int main()
   {
       int appleAmount = 6;
       resetAmount(appleAmount);
       std::cout << appleAmount << std::endl;
   }
   ```

   <details>
   <summary>Ответ</summary>

   `appleAmount` перезапишется на `0`, так как функции передастся ссылка на нее.

   Под капотом, передается *адрес* переменной `appleAmount`, но это скрывается компилятором.
   </details>

2. ```cpp
   #include <iostream>

   struct Arm
   {
       int power;
   };

   void increasePower(Arm& arm)
   {
       arm.power += 1;
   }

   int main()
   {
       Arm arm { 1 };
       increasePower(arm);
       std::cout << arm.power << std::endl;
   }
   ```

   <details>
   <summary>Ответ</summary>

   В функции можно передавать ссылки на объекты типа структуры.
   Здесь, задача функции — увеличить силу.
   </details>

2. Возможно ли у ссылки взять размер? Какой размер у ссылки?

   ```cpp
   #include <iostream>

   int main()
   {
       int a = 6;
       int& b = a;
       std::cout << sizeof(b) << std::endl;
   }
   ```

   <details>
   <summary>Ответ</summary>

   `sizeof(b)` сработает, но даст размер `int`-а, а не ссылки.

   Размер ссылки получить невозможно, это скрыто компилятором.

   Однако, если ссылка передается параметром в функцию, 
   по факту передастся адрес, размер которого 8 байт.

   > Адрес необходимо передать, потому что функция не сможет 
   > получить доступ к той что надо переменной без внешнего контекста.
   > Самый простой способ получить доступ к переменной, определенной извне — это передать ее адрес.
   </details>
