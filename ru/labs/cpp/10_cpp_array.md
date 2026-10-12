---
slug: ru/cpp/labs/cpp-array
---
<!-- course-site-backlink:start -->
[Этот урок на сайте](https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms/ru/cpp/labs/cpp-array/)
<!-- course-site-backlink:end -->
# C++ массивы (`std::array`)

- [Информация](../../../en/06_arrays/doc.md)

## Концепты

- Преимущество C++ массивов над C массивами
- Копирование и инициализация массивов
- Индексирование C++ массивов
- `data`
- Получение адресов элементов массива
- Типы данных кроме `int` под элементы массива


## Примеры

Для фрагментов без `main` подключите `<array>` и `<iostream>` и поместите код в `main`.

### 1. Получение адреса первого элемента

```cpp
std::array<int, 2> arr{ 1, 2 };
int* p{ arr.data() };
*p = 3;
std::cout << arr[0] << std::endl;
std::cout << arr[1] << std::endl;
```

<details>
<summary>Ответ</summary>

`arr.data()` возвращает указатель на первый элемент, как и `&arr[0]`.
Запись через этот указатель изменяет элемент.
Печатает `3` и `2`.
</details>

### 2. Количество элементов

```cpp
std::array<int, 3> arr{ 4, 7, 9 };
std::cout << arr.size() << std::endl;
```

<details>
<summary>Ответ</summary>

Печатает `3`.
`arr.size()` возвращает количество элементов, а не число байтов.
Здесь это аргумент размера в `std::array<int, 3>`.
</details>

### 3. Инициализация C++ массивов (1)
```cpp
std::array<int, 2> arr{ 1, 2 };
std::array<int, 2> other{ 3, 4 };
arr = other;
```

<details>
<summary>Ответ</summary>

Тут каждый элемент копириуется из `other` в `arr`.
</details>

### 4. Инициализация C++ массивов (2)
```cpp
std::array<int, 2> arr{ 1, 2 };
std::array<int, 2> other{ arr };
```

<details>
<summary>Ответ</summary>

Тут тоже, но при создании `other`.
</details>

### 5. Адрес массива
```cpp
std::array<int, 2> arr{ 1, 2 };
std::array<int, 2>* p{ &arr };
*p = { 3, 4 };
std::cout << arr[0] << std::endl;
std::cout << arr[1] << std::endl;
```

<details>
<summary>Ответ</summary>

`p` будет содержать адрес начала всего объекта массива.
Объект массива покрывает все его элементы.

Здесь, изначальные элементы перезаписываются на `3, 4`.
</details>

### 6. Dereference адреса массива
```cpp
std::array<int, 2> arr{ 1, 2 };
std::array<int, 2>* p{ &arr };
std::array<int, 2> arr1{ *p };
arr1[0] = 3;
arr1[1] = 4;
std::cout << arr[0] << std::endl;
std::cout << arr[1] << std::endl;
```

<details>
<summary>Ответ</summary>

Тип у `p` — `std::array<int, 2>*`, выражение `*p` даст значение
типа `std::array<int, 2>`, то есть в `arr1` попадет копия всего массива

Поскольку `arr1` это копия, ее изменения не повлияют на `arr`.
</details>

### 7. Индексирование элементов из адреса
```cpp
std::array<int, 2> arr{ 1, 2 };
std::array<int, 2>* p{ &arr };
(*p)[0] = 3;
(*p)[1] = 4;
std::cout << arr[0] << std::endl;
std::cout << arr[1] << std::endl;
```

<details>
<summary>Ответ</summary>

`*p` обращается к исходному объекту массива.
`(*p)[0]` и `(*p)[1]` обращаются к его элементам, поэтому присваивания изменяют `arr`.
Печатает `3` и `4`.
</details>

### 8. Матрицы (двумерные массивы)
```cpp
std::array<std::array<int, 2>, 3> arr{
    std::array{ 1, 2 },
    { 3, 4 },
    { 5, 6 },
};
std::array<int, 2> firstRow { arr[0] };
std::array<int, 2> lastRow { arr[2] };
arr[0][0] = 7;
arr[2][1] = 8;
arr[1] = { 9, 10 };
```

<details>
<summary>Ответ</summary>

Тут иллюстрируется использование массива, где тип элемента не `int`, а массив.
Каждый элемент массива по сути теперь хранит в себе по два инта.

> В инициализации `arr` необходимо указать `std::array`,
> потому что иначе компилятор не может определить тип элемента из инициализации.
> Ему нужно слегка помочь.
>
> Механизм этого вам пока не обязательно понимать.
</details>

<details>
<summary>Можно ли использовать пользовательский тип как элемент массива?</summary>

Можно. Попробуйте определить тип, например:
```cpp
struct Item
{
    int f1;
    int f2;
};
```

И использовать его в качестве типа элемента, вот так:
```cpp
std::array<Item, 3> arr{
    Item{ 1, 2 },
    { 3, 4 },
    { 5, 6 },
};
```
</details>


## Структуры и массивы

### 1. Поле массива из адресов
```cpp
#include <iostream>
#include <array>

struct A
{
    std::array<int*, 2> f;
};

int main()
{
    int var1;
    int var2;
    A a { .f = { &var1, &var2 } };
    *a.f[0] = 1;
    *a.f[1] = 2;
    int** b = a.f.data();
    int c = **b;

    std::cout << var1 << std::endl;
    std::cout << var2 << std::endl;

    std::cout << a.f[0] << std::endl;
    std::cout << a.f[1] << std::endl;

    std::cout << b << std::endl;
    std::cout << c << std::endl;
}
```

<details>
<summary>Ответ:</summary>

Строчка `A a { .f = { &var1, &var2 } };` инициализирует `a`,
вписав в поле `a.f[0]` адрес на `var1` и в `a.f[1]` адрес на `var2`.

В строчке `*a.f[0] = ...`, происходит переход по адресу, сохраненному в `a.f[0]`:
`*a.f[0]` -> `*(a.f[0])` -> `*(&var1)` -> `var1`.

В `int** b = a.f.data();` метод `.data()` возвращает `&(a.f[0])` типа `int**`.
Это адрес первого элемента массива `f` внутри `a`.

Выведется:
- `1`, `2` как значения `var1` и `var2`;
- адреса `var1` и `var2` как значения `a.f[0]` и `a.f[1]`;
- `c` будет равно `1`.

</details>

### 2. Размер структуры (2)
```cpp
#include <iostream>
#include <array>

struct A
{
    std::array<int, 4> f1;
    int* f2;
};

int main()
{
    std::cout << sizeof(A) << std::endl;
}
```

<details>
<summary>Ответ:</summary>

- `std::array<int, 4> f1` - это 4 `int`, каждый по 4 байта - 16 байт;
- `int* f2` - 8 байтов на 64-битном процессоре.

В сумме 24 байта.
</details>

### 3. Инициализация поля массива
```cpp
#include <iostream>
#include <array>

struct A
{
    std::array<int, 2> arr;
};

int main()
{
    A a { { 1, 2 } };
    A b { { 3, 4 } };
    b = a;

    std::cout << b.arr[0] << std::endl;
    std::cout << b.arr[1] << std::endl;
}
```

<details>
<summary>Ответ:</summary>

Выведется `1`, `2`.
</details>

### 4. Копирование структуры с полем-массивом
```cpp
#include <iostream>
#include <array>

struct A
{
    std::array<int, 2> arr;
};

int main()
{
    A a { { 1, 2 } };
    A b { a };

    a.arr[0] = 3;

    std::cout << b.arr[0] << std::endl;
    std::cout << b.arr[1] << std::endl;
    std::cout << a.arr[0] << std::endl;
    std::cout << a.arr[1] << std::endl;
}
```

<details>
<summary>Ответ:</summary>

`A b{ a }` копирует значения *всех полей*, включая массив целиком, поэлементно.

На момент копирования в `a` лежит `arr[0] = 1`, `arr[1] = 2`,
поэтому в `b` попадут те же значения: `b.arr[0] = 1`, `b.arr[1] = 2`.
Но это отдельная копия в отдельной памяти: сам массив `arr`
хранится внутри `A` по значению, а не по адресу.

Поэтому последующее изменение `a.arr[0] = 3`
меняет только `a`, а `b` остается нетронутым.

Выведется `1`, `2`, `3`, `2`.
</details>

### 5. Массив структур
```cpp
#include <iostream>
#include <array>

struct A
{
    int f1;
    int f2;
};

int main()
{
    std::array<A, 3> arr{};

    arr[0].f2 = 1;

    arr[1] = A{ 2, 3 };

    A copy { arr[2] };
    copy.f1 = 4;
    copy.f2 = 5;

    std::cout << arr[0].f1 << std::endl;
    std::cout << arr[0].f2 << std::endl;
    std::cout << arr[1].f1 << std::endl;
    std::cout << arr[1].f2 << std::endl;
    std::cout << arr[2].f1 << std::endl;
    std::cout << arr[2].f2 << std::endl;
}
```

<details>
<summary>Ответ:</summary>

Строчка `std::array<A, 3> arr{};`:
- Определяет массив из трех переменных типа `A`.
 В общей сложности выделется память под 6 `int`-ов.
- Фигурные скобки означают "инициализация нулями".
 Каждый элемент массива заполнится дефолтным `A`, то есть `A{}`,
 что означает, что все 6 `int`-ов станут нулями.

В `arr[0].f2 = 1;`, `arr[0]` получает доступ к памяти
первой переменной в массиве.
Эта переменная типа `A` (не `int`! очень важно понимать).
В ней внутри во второе поле (`.f2`) вписывается `1` (`= 1`).

`arr[1] = A{ 2, 3 };` перезаписывает весь второй элемент
результатом выражения `A{ 2, 3 }`.
Это перезапишет оба поля.

`A copy { arr[2] };` считывает из третьего элемента массива,
копируя то, что есть там, во временную переменную `copy`.
`copy` хранит копию значения из `arr[2]` типа `A` (то есть, имеет копию всех полей).
Следовательно, последующие воздействия на `copy` не повлияют на `arr[2]`.

```
0
1
2
3
0
0
```
</details>
