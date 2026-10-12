---
slug: ru/cpp/labs/pointer-arithmetic
---
<!-- course-site-backlink:start -->
[Этот урок на сайте](https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms/ru/cpp/labs/pointer-arithmetic/)
<!-- course-site-backlink:end -->
# Арифметика указателей

- [Видео по основам, более углубленная информация](https://www.youtube.com/watch?v=9AhNOjjyAwU&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=14)

## Концепты

- Что делает сложение указателя и числа
- Что дает отнимание двух указателей
- UB в случае, если указатели не из того же блока
- stack

## Примеры на понимание

Для фрагментов без `main` подключите `<array>` и `<iostream>` и поместите код в `main`.

### 1. Переход адреса на 1
```cpp
std::array<int, 2> arr{};
int* p = &arr[0];
p = p + 1;
*p = 2;

std::cout << arr[1];
std::cout << std::endl;
```

<details>
<summary>Ответ</summary>

`p + 1` перемещает указатель на 1 базовый элемент, то есть на 1 `int`, то есть на 4.

`p` в конце функции равен `&arr[1]`.
Считывание из `*p` эквивалетно считыванию из `arr[1]`.
</details>

### 2. Возврат адреса следующего элемента массива

```cpp
#include <array>
#include <iostream>

int* nextElement(int* current)
{
    return current + 1;
}

int main()
{
    std::array<int, 3> arr{ 4, 7, 9 };
    int* next{ nextElement(&arr[0]) };
    *next = 8;
    std::cout << arr[1] << std::endl;
}
```

<details>
<summary>Ответ</summary>

Печатает `8`.
Вызов возвращает `int*`, указывающий на `arr[1]`, поэтому запись через `next` изменяет этот элемент.
Массив принадлежит `main` и продолжает существовать после возврата из функции.
Вызывающий код должен убедиться, что следующий элемент существует, прежде чем разыменовывать указатель.
</details>


### 3. Переход по адресу из выражения
```cpp
std::array<int, 2> arr{};
int* p = &arr[0];
*(p + 1) = 6;

std::cout << *p << std::endl;
std::cout << arr[1] << std::endl;
```

<details>
<summary>Ответ</summary>

С указателем, полученным из выражения, можно работать как и с указателем из обычной переменной.

Еще важно заметить, что `*(p + 1)` *не изменяет `p`*, а создает *временный измененный адрес*.
`*p` считает `0` из первой ячейки массива.
</details>

### 4. Отнимание указателей
```cpp
std::array<int, 2> arr{};
int* pStart = &arr[0];
int* p = pStart + 1;

ptrdiff_t x = p - pStart;
std::cout << x;
std::cout << std::endl;

ptrdiff_t x1 = pStart - p;
std::cout << x1;
std::cout << std::endl;
```

<details>
<summary>Ответ</summary>

Оператор `-` между указателями дает количество базовых элементов между ними.
Результат может быть и отрицательным.

Выведется 1, а потом -1.
</details>

### 5. (продвинутый уровень): Отнимание адресов
```cpp
#include <cstdint>
#include <array>
#include <iostream>

int main()
{
   std::array<int, 2> arr{};
   int* a = &arr[0];
   int* b = &arr[1];
   uintptr_t a1 = reinterpret_cast<uintptr_t>(a);
   uintptr_t b1 = reinterpret_cast<uintptr_t>(b);
   ptrdiff_t x = static_cast<ptrdiff_t>(b1 - a1);

   std::cout << x;
   std::cout << std::endl;
}
```

<details>
<summary>Ответ</summary>

`uintptr_t` это число, занимающее столько же байтов, сколько и `int*` (вероятно, 8 байтов).

`b1 - a1` применяется между адресами как числами. 
Это выражение уже не имеет информацию о том, какого типа указатели были вначале.
Оно работает на числовых значениях указателя.

Ответ будет 4 — разница указателей в байтах.
</details>

### 6. Чтение за пределами массива из одного элемента (углублённый уровень)

```cpp
std::array<int, 1> value{ 5 };
int* p{ value.data() };
int* past{ p + 1 };
std::cout << *past << std::endl;
```

<details>
<summary>Ответ</summary>

Получить указатель за последним элементом допустимо, но его разыменование — неопределённое поведение.
Определённого результата вывода нет.
Соседство другого объекта в памяти не делает этот указатель допустимым для чтения.
</details>

### 7. Запись за пределами массива (углублённый уровень)

```cpp
std::array<int, 2> arr{};
int* past{ arr.data() + arr.size() };
*past = 7;
```

<details>
<summary>Ответ</summary>

`past` — допустимый указатель за последним элементом, но запись через него — неопределённое поведение.
Элементам соответствуют только индексы от нуля до `arr.size() - 1`.
По адресу за последним элементом нет дополнительного элемента массива.
</details>
