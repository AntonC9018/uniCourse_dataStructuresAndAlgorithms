# 1. C-массивы (группы переменных)

- [Массивы и индекс](https://www.youtube.com/watch?v=859Y0Q8pyLg&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=8)
- [Видео по основам, более углубленная информация](https://www.youtube.com/watch?v=9AhNOjjyAwU&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=14)

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

### 4. Чтение по индексу
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

### 5. Вписывание по индексу
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

### 6. Выражение как индекс
```cpp
int arr[3]{};
size_t index { 1 };
arr[index + 1] = 5;
std::cout << arr[2];
std::cout << std::endl;
```

<details>
<summary>Ответ</summary>

Здесь демонстрируется использование более сложного выражения
для получения индекса.
</details>

### 7. Связь переменной и массива после перезаписи
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

### 8. Указатель как тип элемента
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

### 9. Использование массива как адрес
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

Выведется 1 дважды.
</details>

<!-- Missing: get address of item at index, different type than int -->
