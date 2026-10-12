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
- Целочисленные представления адресов и `reinterpret_cast`
- Смещения полей
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

`uintptr_t`, если этот тип доступен, — беззнаковый целочисленный тип, способный хранить преобразованный указатель на объект.
`reinterpret_cast` выполняет это преобразование указателя в число.

`b1 - a1` применяется между адресами как числами.
В этом выражении уже нет информации об исходных типах указателей.
Оно работает с их числовыми значениями.

На реализациях, где числовые адреса соответствуют позициям байтов, результат равен `sizeof(int)`, обычно `4`.
Способ преобразования указателя в число зависит от реализации, поэтому такое расстояние гарантируется не везде.
</details>

### 6. Адрес поля относительно адреса структуры
```cpp
#include <cstdint>
#include <iostream>

struct A
{
    int f;
};

int main()
{
    A a { };
    A* pa { &a };
    int* pf { &pa->f };
    uintptr_t fieldAddress{ reinterpret_cast<uintptr_t>(pf) };
    uintptr_t objectAddress{ reinterpret_cast<uintptr_t>(pa) };
    uintptr_t diff{ fieldAddress - objectAddress };
    std::cout << diff << std::endl;
}
```

<details>
<summary>Ответ</summary>

На реализациях, где преобразование указателя в число сохраняет равенство адресов, выведется `0`.
У этой простой структуры первое поле и сама структура находятся по одному адресу.
`reinterpret_cast<uintptr_t>` преобразует каждый указатель в целочисленное представление его адреса.
Здесь вычитаются числа, а не указатели на разные объекты.
Способ преобразования указателя в число зависит от реализации; расстояния в байтах в общем случае не гарантируются.
</details>

### 7. (продвинутый уровень): Смещения полей
```cpp
#include <cstddef>
#include <iostream>

struct A
{
    int a;
    int b;
};

int main()
{
    std::cout << offsetof(A, a) << std::endl;
    std::cout << offsetof(A, b) << std::endl;
}
```

<details>
<summary>Ответ:</summary>

`offsetof` вычисляется при компиляции и даёт смещение указанного поля в байтах от начала структуры.

Для `a` выведется `0`; смещение `b` обычно равно `4`, если `int` занимает 4 байта.
Точное смещение зависит от реализации и её правил выравнивания.
</details>

### 8. Объект массива и его первый элемент (продвинутый уровень)

```cpp
#include <array>
#include <cstdint>
#include <iostream>

int main()
{
    std::array<int, 2> arr{ 1, 2 };
    uintptr_t elementAddress{ reinterpret_cast<uintptr_t>(arr.data()) };
    uintptr_t arrayAddress{ reinterpret_cast<uintptr_t>(&arr) };
    uintptr_t diff{ elementAddress - arrayAddress };
    std::cout << diff << std::endl;
}
```

<details>
<summary>Ответ</summary>

На распространённых реализациях выведется `0`: первый элемент начинается там же, где объект массива.
Стандарт не требует такого расположения для `std::array`, поэтому этот результат не гарантируется.
У `arr.data()` тип `int*`, а у `&arr` — `std::array<int, 2>*`.
Преобразование в числа позволяет вычесть их числовые значения, но не меняет исходные типы указателей.
Приведение обоих указателей к указателям на байты не сделало бы их вычитание корректным:
вычитать можно указатели на элементы одного массива или на позицию сразу за его последним элементом.
</details>

### 9. Продвинутый уровень: адреса локальных переменных
```cpp
#include <cstdint>
#include <iostream>

uintptr_t f()
{
    int a;
    return reinterpret_cast<uintptr_t>(&a);
}

uintptr_t g()
{
    int b;
    return reinterpret_cast<uintptr_t>(&b);
}

int main()
{
    uintptr_t f1 { f() };
    uintptr_t f2 { f() };
    uintptr_t g1 { g() };

    std::cout << f1 << std::endl;
    std::cout << f2 << std::endl;
    std::cout << g1 << std::endl;
}
```

<details>
<summary>Ответ</summary>

C++ компилятор не гарантирует этого, и на это не стоит полагаться, но,
вероятно, напечатается тот же самый адрес 3 раза.

Это происходит потому, что для локальных переменных выделяется память на стеке,
которая освобождается после завершения вызова функции.
При вызове последующих функций, для их локальных переменных
**может выделиться память, ранее занятая локальными переменными предыдущего вызова**.
Поэтому адреса локальных переменных могут совпасть.
</details>

### 10. Чтение за пределами массива из одного элемента (углублённый уровень)

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

### 11. Запись за пределами массива (углублённый уровень)

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
