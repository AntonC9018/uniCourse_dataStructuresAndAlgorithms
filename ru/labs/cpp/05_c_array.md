---
slug: ru/cpp/labs/c-array
---
<!-- course-site-backlink:start -->
[Этот урок на сайте](https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms/ru/cpp/labs/c-array/)
<!-- course-site-backlink:end -->
# C-массивы (группы переменных)

- [Массивы и индекс](https://www.youtube.com/watch?v=859Y0Q8pyLg&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=8)
- [Видео по основам, более углубленная
информация](https://www.youtube.com/watch?v=9AhNOjjyAwU&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=14)

## Концепты

- Индексирование
- Получение адреса первого элемента

## Примеры на понимание

### 1. Массив

```cpp
int arr[2]{};
arr[0] = 1;
arr[1] = 2;

std::cout << arr[0];
std::cout << std::endl;

std::cout << arr[1];
std::cout << std::endl;
```

<details>

<summary>

Что значит `int arr[2]{}`?

</summary>

Типа группы из 2 переменных (массив), по умолчанию равным нулю (благодаря {}).
</details>

<details>
<summary>Что такое массив?</summary>

Массив это как бы несколько переменных в одной. 
В данном случае, переменных как бы 2: `arr[0]` и `arr[1]`.

Выражение "как бы" тут нарочно, потому что по факту `arr[0]` и `arr[1]` — это объекты,
а не переменные, но это в другом уроке.
</details>

<details>
<summary>Ответ</summary>

`arr[0]` и `arr[1]` как бы эквивалентны именам переменных.
То есть напечатается 1 и 2.
</details>

### 2. Инициализация массива
```cpp
int arr1[2]{ 21, 32 };

std::cout << arr1[0];
std::cout << std::endl;

std::cout << arr1[1];
std::cout << std::endl;
```

<details>
<summary>Что значит этот синтаксис?</summary>

Здесь элементы массива заданы при создании, в том же порядке (0, 1).
</details>

### 3. Массив с неуказанной длинной
```cpp
int arr1[3]{ 1, 2, 3 };
int arr2[]{ 1, 2, 3, 4 };

std::cout << sizeof(arr1);
std::cout << std::endl;

std::cout << sizeof(arr2);
std::cout << std::endl;
```

<details>

<summary>

Что такое `sizeof`?

</summary>

Это оператор, выполняющийся во время компиляции, который дает размер всего массива в байтах.
В данном примере, в массиве `arr1` 3 инта, каждый по 4 байта, поэтому общий размер будет 12.
</details>

<details>

<summary>

Какой размер у `arr2`?

</summary>

У `arr2` не задан размер, он определится автоматически из элементов.
</details>

<details>

<summary>

Что значит `[]`?

</summary>

Это заменится во время компиляции на количество элементов справа 
(то есть 4, в этом примере) в качестве длины.
</details>

<details>
<summary>Ответ</summary>

3 инта по 4 байта — это 12.

4 инта по 4 байта — это 16.
</details>

### 4. Размер массива с элементами типа `size_t`
```cpp
size_t arr[3]{ 1, 2, 3 };

std::cout << sizeof(arr);
std::cout << std::endl;
```

<details>
<summary>Ответ</summary>

`sizeof` дает размер всего массива в байтах, а не количество элементов.
Здесь каждый элемент имеет тип `size_t` — это 8 байт на 64-битной системе,
поэтому 3 элемента по 8 байт — это 24.
</details>

### 5. Вычисление количества элементов через `sizeof`
```cpp
int arr[]{ 1, 2, 3, 4, 5 };

std::cout << sizeof(arr);
std::cout << std::endl;

std::cout << sizeof(arr[0]);
std::cout << std::endl;

std::cout << sizeof(arr) / sizeof(arr[0]);
std::cout << std::endl;
```

<details>
<summary>Как вычислить количество элементов через sizeof?</summary>

Чтобы получить количество элементов, нужно поделить размер всего массива на размер одного элемента.
</details>

<details>
<summary>Ответ</summary>

Здесь `sizeof(arr)` — это 20 (5 интов по 4 байта),
`sizeof(arr[0])` — это 4 (один `int`),
поэтому `20 / 4` даст 5 элементов.

Это работает, только пока `arr` остается массивом.
Как только он деградирует (decays) в указатель (см. ниже),
`sizeof` вернёт размер указателя.
</details>

### 6. Чтение по индексу
```cpp
int arr[3]{ 1, 2, 3 };
size_t index { 2 };
int it { arr[index] };
std::cout << it;
std::cout << std::endl;
```

<details>
<summary>Ответ</summary>

Можно использовать "номер переменной" (индекс) 
из другой переменной или выражения.

Ответ будет 3.
</details>

### 7. Вписывание по индексу
```cpp
int arr[3]{};
size_t index { 2 };
arr[index] = 5;
std::cout << arr[2];
std::cout << std::endl;
```

<details>
<summary>Ответ</summary>

Запись по индексу тоже можно делать исходя из индекса,
произошедшего из выражения.
</details>

### 8. Выражение как индекс
```cpp
int arr[3]{};
size_t index { 1 };
arr[index + 1] = 5;
std::cout << arr[2];
std::cout << std::endl;
std::cout << index;
std::cout << std::endl;
```

<details>
<summary>Ответ</summary>

Здесь демонстрируется использование более сложного выражения
для получения индекса.

`index + 1` равно `2`, поэтому `5` записывается в `arr[2]`.
Сам `index` при этом не меняется,
поэтому затем печатается `1`.
</details>

### 9. Связь переменной и массива после перезаписи
```cpp
int arr[3]{ 0, 2, 1 };
size_t index { 2 };
int it { arr[index] };
arr[index] = 5;
std::cout << it;
std::cout << std::endl;
```

<details>
<summary>Ответ</summary>

В `it` на строчке `int it { arr[index] }` будет скопировано *значение `1`*,
а не ссылка на элемент в массиве, поскольку тип `it` это `int`.
Так как это просто `int`, изменение переменной, из которой произошло его значение,
после присваивания, не воздействует на `it`.

Выведется `1`.
</details>

### 10. auto из элемента массива

```cpp
int arr[2]{ 3, 7 };
auto value{ arr[1] };
arr[1] = 9;
std::cout << value << std::endl;
std::cout << arr[1] << std::endl;
```

<details>
<summary>Ответ</summary>

У `arr[1]` тип `int`, поэтому у `value` тип `int`.
Это копия, а не другое имя элемента массива.
Печатает `7` и `9`.
</details>

### 11. auto из адреса элемента массива

```cpp
int arr[2]{ 3, 7 };
auto p{ &arr[1] };
*p = 9;
std::cout << arr[1] << std::endl;
```

<details>
<summary>Ответ</summary>

У `&arr[1]` тип `int*`, поэтому у `p` тип `int*`.
Печатает `9`: указатель обращается к самому элементу массива.
</details>

### 12. Указатель как тип элемента
```cpp
int a = 1;
int b = 2;
int* arr[]{ &a, &b };
*arr[0] = 3;
*arr[1] = *arr[0];

std::cout << arr[0] << std::endl;
std::cout << arr[1] << std::endl;

std::cout << *arr[0] << std::endl;
std::cout << *arr[1] << std::endl;
```

<details>
<summary>Ответ</summary>

В массивах можно хранить данные, отличные от `int`.
В данном примере, в массиве были сохранены указатели на `int` (`int*`).

- `arr[0]` содержит адрес переменной `a`.
- `arr[1]` содержит адрес переменной `b`.
- `a`, эквивалентно `*arr[0]`, равно `3`.
- `b`, эквивалентно `*arr[1]`, равно `3`.
</details>

### 13. Использование массива как адрес
```cpp
int arr[2]{};
int* p = arr;
*arr = 1;

std::cout << *p;
std::cout << std::endl;

std::cout << arr[0];
std::cout << std::endl;

std::cout << arr[1];
std::cout << std::endl;
```

<details>
<summary>Ответ</summary>

Когда `arr` используется в качестве выражения в `int* p = arr`,
он деградирует (decays) в указатель на первый элемент из массива.
`arr` тут эквивалентно `&arr[0]` или `&(arr[0])`.

И `*p`, и `*arr`, и `arr[0]` ссылаются на ту же переменную.

Печатает `1`, `1` и `0`: второй элемент массива остаётся нулём.
</details>

### 14. auto из выражения-массива

```cpp
int arr[2]{ 3, 7 };
auto p{ arr };
*p = 8;
std::cout << arr[0] << std::endl;
```

<details>
<summary>Ответ</summary>

В этой инициализации `arr` преобразуется в `int*`, указывающий на первый элемент массива.
Поэтому `auto` выводит для `p` тип `int*`; массив не копируется.
Печатает `8`.
Запись `auto p{ &arr[0] };` явно задаёт тот же адрес.
</details>

### 15. Печать массива
```cpp
int arr[3]{ 1, 2, 3 };
std::cout << arr;
std::cout << std::endl;
```

<details>
<summary>Ответ</summary>

Когда `arr` используется в качестве выражения (как аргумент `<<`),
он деградирует в указатель на первый элемент, то есть эквивалентно `&arr[0]`.

`std::cout` не умеет печатать C-массивы фиксированного размера —
он видит лишь указатель, поэтому напечатается этот адрес, а не элементы `1`, `2`, `3`.
Чтобы напечатать элементы, нужно выводить каждый элемент по индексу, как в первых примерах.
</details>

### 16. Присваивание массива (1)
```cpp
int arr1[2]{ 1, 2 };
int arr2[2]{ 3, 4 };
arr1 = arr2;
```
<details>
<summary>Ответ</summary>

Несмотря на то, что логически это должно скопировать каждый элемент
из `arr2` в `arr1`, программа не скомпилируется.
Такой синтаксис просто не работает в C++.
</details>

### 17. Присваивание массива (2)
```cpp
int arr1[2]{ 1, 2 };
int arr2[2]{ 3, 4 };
int* first{ &arr1[0] };
int* second{ &arr2[0] };
*first = *second;
```
<details>
<summary>Ответ</summary>

`first` указывает на `arr1[0]`, а `second` — на `arr2[0]`.
`*first = *second` копирует значение `3` в `arr1[0]`; остальные элементы не изменяются.
Присваивания массива целиком нет.
</details>

### 18. Присваивание массива в переменную типа `int`
```cpp
int arr[2]{ 1, 2 };
int x = arr;
```
<details>
<summary>Ответ</summary>

Когда `arr` используется как выражение, он деградирует (decays)
в указатель на первый элемент, то есть в `int*`.
`int*` нельзя неявно преобразовать в `int`,
поэтому программа не скомпилируется.

Чтобы скопировать один элемент, используйте индекс: `int x = arr[0];`.
Чтобы сохранить адрес первого элемента, используйте указатель: `int* p = arr;`.
</details>

<!-- Missing: get address of item at index, different type than int -->
