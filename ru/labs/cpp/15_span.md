# `std::span`

- [Видео](https://www.youtube.com/watch?v=3aXFuiHxb9k&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=19)

## Примеры на понимание

### 1. Индексирование указателей
```cpp
std::array<int, 3> arr{ 0, 1, 2 };
int* arrStart{ arr.data() };
*arrStart = 3;
*(arrStart + 0) = 4;
arrStart[0] = 5;
*(arrStart + 1) = 6;
arrStart[1] = 7;
*(arrStart + 2) = 8;
arrStart[2] = 9;

int item0{ *arrStart };
item0 = arrStart[0];
int item1{ *(arrStart + 1) };
item1 = arrStart[1];
```

<details>
<summary>Ответ:</summary>

`arrStart` получает адрес первого элемента в массиве, благодаря `.data()`.

Далее `*arrStart` ссылается на первый элемент в массиве по адресу.
`*arrStart` эквивалентно `*(arrStart + 0)`.

Синтаксис `*(x + 1)` эквивалентен синтаксису `x[1]`.
Соответственно, `*(arrStart + 0)` можно индексированием записать как `arrStart[0]`.

> `x[1]` так же эквивалентен `1[x]`

`*(arrStart + 1)` эквивалентно `arrStart[1]`, что эквивалентно `arr[1]`.
Здесь, мы перепрыгиваем через первый элемент (`+ 1`), 
начиная с начала первого элемента (`arrStart`),
попадая на следующую ячейку в памяти.

Эти выражения можно использовать как для вписывания значений,
так и для их считывания.
</details>

### 2. Передача массива как указатель
```cpp
#include <iostream>
#include <array>

void func(int* arr)
{
   std::cout << arr[0] << std::endl;
   std::cout << arr[1] << std::endl;
}

int main()
{
   std::array<int, 2> arr{ 1, 2 };
   func(arr.data());
}
```

<details>
<summary>Ответ:</summary>

Здесь функции передается адрес первого элемента из массива.

`arr[0]` эквивалентен `*(arr + 0)` 
и считает первый элемент из массива `arr` из функции `main`.

Соответственно `arr[1]` эквивалентен `*(arr + 1)` и напечатает второй элемент.

Выведется `1` и `2`.
</details>

### 3. Особый синтаксис передачи массива
```cpp
#include <iostream>
#include <array>

void func(int arr[])
{
   std::cout << arr[0] << std::endl;
   std::cout << arr[1] << std::endl;
}

int main()
{
   std::array<int, 2> arr{ 1, 2 };
   func(arr.data());
}
```

<details>
<summary>Ответ:</summary>

`int* arr` эквивалентно `int arr[]` когда используется в качестве параметра.
Этот пример эквивалентен предыдущему.
</details>

### 4. Чтение за пределами массива
```cpp
#include <iostream>
#include <array>

void func(int arr[])
{
   std::cout << arr[0] << std::endl;
   std::cout << arr[1] << std::endl;
   std::cout << arr[2] << std::endl;
}

int main()
{
   std::array<int, 2> arr{ 1, 2 };
   func(arr.data());
}
```

<details>
<summary>Ответ:</summary>

`arr[2]` в инструкции `std::cout << arr[2] << std::endl` пытается считать по индексу `2` из массива.
В C, попытка считывания по несуществующему индексу считается UB (undefined behavior).
Этот код скомпилируется и запустится без проблем,
но считывание `arr[2]` технически способно привести к любому результату при выполнении.

Подобное считается логической ошибкой в коде.
</details>

<details>
<summary>Как предотвратить данную ошибку?</summary>

Нужно выполнять проверку того, находится ли индекс за пределами массива перед тем,
как считываете по тому или иному индексу.
Для того чтобы выполнить данную проверку, помимо указателя на начало массива
нужно иметь также и длину массива. 
В данном примере, длина массива известна (2), но в общем случае ее тоже нужно будет передать.
Об этом есть в дальнейших примерах.
</details>

### 5. Вызов той же функции для разных массивов
```cpp
#include <iostream>
#include <array>

void func(int arr[])
{
   std::cout << arr[0] << std::endl;
   std::cout << arr[1] << std::endl;
   std::cout << arr[2] << std::endl;
}

int main()
{
   std::array<int, 3> arr1{ 0, 1, 2 };
   std::array<int, 2> arr2{ 0, 1 };
   func(arr1.data());
   func(arr2.data());
}
```

<details>
<summary>Ответ:</summary>

Для первого массива не возникает UB, 
поскольку он позволяет просматривать все индексы от 0 до 2.

Однако для второго массива, повторяется ситуация в примере выше.

Здесь иллюстрируется тот факт, что одна и та же функция может использоваться
для массивов разной длины, и не может предположить ее заранее.
</details>

### 6. Печать циклом
```cpp
#include <iostream>
#include <array>

void print(int* arr)
{
   for (size_t i = 0; i < 2; i++)
   {
       std::cout << arr[i] << std::endl;
   }
}

int main()
{
   std::array<int, 2> arr{ 0, 1 };
   print(arr.data());
}
```

<details>
<summary>Ответ:</summary>

Здесь иллюстрируется то, как можно напечатать в консоль все элементы из массива, используя цикл.

`2` в условии цикла ссылается на длину массива.
</details>

<details>
<summary>Как не дублировать длину для массива?</summary>

Здесь несколько вариантов:
- Передать статический массив или ссылку на него параметром;
- Передать длину отдельным параметром;
- Создать глобальную константу для длины, но тогда функция будет ограничена только этой длиной;
- Передать `span` (указатель на первый элемент и длину одним параметром).

Все это описано в дальнейших примерах.
</details>

<details>
<summary>Что будет, если длина не совпадает?</summary>

Если в цикле упомянуть не ту длину, что длина массива:
```cpp
for (size_t i = 0; i < 3; i++)
```
произойдет чтение за элемента за пределами массива, что считается UB.

Если задать большую длину переменной:
```cpp
std::array<int, 3> arr{ 0, 1, 2 };
```
напечатается не весь массив.

Если меньшую:
```cpp
std::array<int, 1> arr{ 0 };
```
снова получим UB в цикле из `print`.
</details>

### 7. Константа длины массива

В чем преимущество этого подхода по сравнению с предыдущим?

```cpp
#include <iostream>
#include <array>

constexpr size_t ARRAY_LENGTH = 2;

void print(int* arr)
{
   for (size_t i = 0; i < ARRAY_LENGTH; i++)
   {
       std::cout << arr[i] << std::endl;
   }
}

int main()
{
   std::array<int, ARRAY_LENGTH> arr{ 0, 1 };
   print(arr.data());
}
```

<details>
<summary>Что такое <code>constexpr</code></summary>

`constexpr` (от constant expression) это константа (неизменяемое значение с именем),
известная во время компиляции.
Она как бы заменится компилятором на ее значение везде где она упоминается.

Нам необходима константа на время компиляции, 
потому что `ARRAY_LENGTH` в `std::array<int, ARRAY_LENGTH>` это часть типа,
а размеры типов в C++ всегда известны при копиляции.

Например, следующее не скомпилируется:
```cpp
#include <array>

int main()
{
   size_t len = 2;
   std::array<int, len> arr{ 1, 2 };
}
```

А следующее — да:
```cpp
#include <array>

int main()
{
   constexpr size_t len = 2;
   std::array<int, len> arr{ 1, 2 };
}
```

`constexpr` в данном примере можно заменить на `static inline const` 
(в теме с линкером будет больше об этом), чтобы получить то же поведение
(`const` `int`-ы в C++ являются так же константами при компиляции).
</details>

<details>
<summary>Ответ</summary>

Преимущество в том, что теперь сложнее передать массив не той что надо длины,
хотя это все еще возможно.
Например:
```cpp
std::array<int, 3> arr{};
print(arr.data());
```

Это происходит, поскольку нет проверки на то *откуда появился указатель* при вызове функции.
</details>

### 8. Как получить длину C-массива? А `std::array`?

<details>
<summary>C-массив? Ты о чем?</summary>

Вот это определение C-массива:
```cpp
int arr[2]{};
```

А вот тут определяется C++ массив (`std::array`):
```cpp
std::array<int, 2> arr{};
```

Если инициализируете элементы, `int` и `2` можно не писать, их компилятор сам поймет:
```cpp
std::array arr{1, 2};
```
</details>

<details>
<summary>Подсказка 1</summary>

У C-массива нет метода `.size()` как у `std::array`.
</details>

<details>
<summary>Подсказка 2</summary>

Приходится обходить систему через `sizeof`.
</details>

<details>
<summary>Подсказка 3</summary>

`sizeof` для всего массива дает его величину в байтах.
</details>

<details>
<summary>Подсказка 4</summary>

`sizeof` выражения одного из элементов или базового типа дает его величину.
Это можно совместить с предыдущей подсказкой.
</details>

<details>
<summary>Ответ</summary>

Количество байтов, выделенное под массив, делите на то, 
сколько байтов занимает один из элементов, получаете количество элементов. 

> Например, есть массив из 3 элементов `int arr[3]{}`.
> Всего он занимает 12 байтов (3 раза по 4 байта для каждого из элементов).
> Каждый элемент занимает по 4 байта.
>
> Если цель получить длину массива (3), имея общую длину в байтах (12),
> нужно посчитать, сколько групп байтов размером в 1 элемент (по 4 байта) влезает в общую длину (12).
> Для этого применяется деление (12 / 4 = 3).

Если ранее был определен `arr`:
```cpp
int arr[3]{};
```

Этого можно достичь вот так:
```cpp
constexpr size_t len{ sizeof(arr) / sizeof(int) };
```

Или вот так, что более гибко:
```cpp
constexpr size_t len{ sizeof(arr) / sizeof(arr[0]) };
```

`sizeof(arr[0])` дает константу, потому что `sizeof` смотрит лишь на *тип выражения* —
операция `arr[0]` и не вычислится априори — компилятор смотрит на то, какой тип *бы* вернулся.
</details>

### 9. Передача массива как параметры для указателя и для длины

В чем преимущества и недостатки этого подхода?
```cpp
#include <array>
#include <iostream>

void print(int* arr, size_t length)
{
    for (size_t i = 0; i < length; i++)
    {
         std::cout << arr[i] << std::endl;
    }
}

int main()
{
    std::array<int, 2> arr{ 0, 1 };
    print(arr.data(), arr.size());

    int arr1[3]{};
    print(arr1, sizeof(arr1) / sizeof(arr1[0]));
}
```

<details>
<summary>Ответ</summary>

Преимущество в том, что теперь функция будет работать для массивов разных длин.

Еще один плюс в том, что еще сложнее ошибится при передаче длины —
просто нужно передать длину массива, который передаете.

Главный недостаток в том, что длину таки надо передать правильно,
и в этом моменте можно допустить ошибку.
Например:
```cpp
std::array<int, 2> arr{};
print(arr.data(), 3);
```
</details>


### 10. (продвинутый уровень) Ссылка на C-массив
```cpp
#include <iostream>

int main()
{
   int arr[3]{};
   int (&arrRef)[3]{ arr };
   arrRef[0] = 1;
   std::cout << arr[0] << std::endl;
}
```

### 11. (продвинутый уровень) Передача ссылки на C-массив
```cpp
#include <iostream>

void print(int (&arr)[3])
{
    for (size_t i = 0; i < 3; i++)
    {
         std::cout << arr[i] << std::endl;
    }
}

int main()
{
    int arr1[3]{};
    print(arr1);
}
```

### 12. (продвинутый уровень) Темплейт длины массива
```cpp
#include <iostream>

template<size_t len>
void print(int (&arr)[len])
{
    for (size_t i = 0; i < len; i++)
    {
         std::cout << arr[i] << std::endl;
    }
}

int main()
{
    int arr1[3]{};
    print(arr1);
}
```

<details>
<summary><code>template</code>?</summary>

Идея в том, что компилятор определит каждое использование данной функции для разных длин массивов,
и создаст разные функции `print`, подставляя соответствующий `len`, исходя из этой длины.

Например, здесь, `print` заменится на `print` с подстановкой `3` как `len`, что иначе можно записать
вот так:
```cpp
print<3>(arr1);
```

</details>

<details>
<summary>Ответ</summary>

В шаблоны можно таким образом передавать ссылки на массивы.
</details>

### 13. Изменение элементов C++ массива, переданного параметром (1)
```cpp
#include <array>
#include <iostream>

void change(std::array<int, 3> arr)
{
    arr[0] = 1;
}

int main()
{
    std::array<int, 3> arr{};
    change(arr);
    std::cout << arr[0] << std::endl;
}
```

<details>
<summary>Ответ</summary>

`arr` не изменится, поскольку функции была передана копия его значения.
</details>

### 14. Изменение элементов C++ массива, переданного параметром (2)
```cpp
#include <array>
#include <iostream>

void change(std::array<int, 3>& arr)
{
    arr[0] = 1;
}

int main()
{
    std::array<int, 3> arr{};
    change(arr);
    std::cout << arr[0] << std::endl;
}
```

<details>
<summary>Ответ</summary>

В `arr[0]` запишется `1`, поскольку функции была передана *ссылка* на объект масссива в `main`.
</details>

### 15. Передача C++ массива ссылкой
```cpp
#include <array>
#include <iostream>

void print(std::array<int, 3>& arr)
{
   for (size_t i = 0; i < arr.size(); i++)
   {
       std::cout << arr[i] << std::endl;
   }
}

int main()
{
    std::array<int, 3> arr{};
    print(arr);
}
```

<details>
<summary>Ответ</summary>

Здесь, в функцию был передан массив ссылкой.
Теперь невозможно передать массив неправильной длины!
Например, следующее не скомпилируется:
```cpp
std::array<int, 2> arr{};
print(arr);
```

Недостаток этого подхода в том, что функция поддерживает только массивы длиной 3.
</details>

### 16. (продвинутый уровень) Темплейт длины C++ массива
```cpp
#include <array>
#include <iostream>

template<size_t len>
void print(std::array<int, len>& arr)
{
   for (size_t i = 0; i < arr.size(); i++)
   {
       std::cout << arr[i] << std::endl;
   }
}

int main()
{
    std::array<int, 3> arr{};
    print(arr);

    std::array<int, 2> arr1{};
    print(arr1);
}
```

<details>
<summary>Ответ</summary>

Данный подход позволяет создавать по функции для каждой длины массива.
Теперь функция поддерживает любую длину массива!

Недостатка сейчас 2:
- Функция поддерживает только C++ массивы со *статически* известной длиной
 (длина часть типа и известна при компиляции);
- Будет создано по одной новой функции для каждой длины, что
 будет тратить лишнюю память в виде инструкций в скомпилированной программе
 (об этом больше в своей теме).

Эти недостатки можно решить, передавая длину параметром как значение,
а не как часть типа.
</details>

### 17. `std::span`
```cpp
#include <span>
#include <iostream>
#include <array>

int main()
{
   std::array<int, 6> arr{0, 1, 2, 3, 4, 5};
   std::span<int> span{ arr };

   std::cout << "Item 1: " << span[1] << std::endl;
   std::cout << "Item 4: " << span[4] << std::endl;
   std::cout << "arr size in bytes: " << sizeof(arr) << std::endl;
   std::cout << "span size in bytes: " << sizeof(span) << std::endl;
   std::cout << "span length: " << span.size() << std::endl;
}
```

<details>
<summary><code>span</code></summary>

`span` — это указатель на первый элемент и длина в одном объекте.
</details>

<details>
<summary>Ответ (индексирование):</summary>

Индексирование `span`-а применяется к основной памяти массива.

Напечатается `1` и `4` из `arr`.
</details>

<details>
<summary>Ответ (<code>sizeof</code>):</summary>

`arr` состоит из 6 `int`, каждый из которых занимает по 4 байта.
Итого, 6 × 4 = 24 байта.

`span` хоть и ссылается на `arr`, делает он это благодаря указателю.
`span` это один указатель `int*` на начало массива и один `size_t` с длиной массива.

Итого, `sizeof(int*)` + `sizeof(size_t)` = 8 + 8 = 16.
</details>

<details>
<summary>Ответ (<code>span.size()</code>):</summary>

`span.size()` получает доступ к сохраненной в `span` длине и возвращает `6`.
</details>

### 18. `std::span` из C++ массива
```cpp
#include <span>
#include <iostream>
#include <array>

int main()
{
   std::array<int, 2> arr{1, 2};
   std::span<int> span{ arr };
   arr[0] = 3;
   arr[1] = 4;

   std::cout << span[0] << std::endl;
   std::cout << span[1] << std::endl;
}
```

<details>
<summary>Ответ:</summary>

Поскольку `span` хранит *адрес начала массива*, а не его копию, 
всегда будут выводится текущие значения из массива.

Выведется `3`, `4`.
</details>

### 19. Метод `at`
```cpp
#include <iostream>
#include <array>

int main()
{
   std::array<int, 2> arr{1, 2};
   std::cout << arr[0] << std::endl;
   std::cout << arr.at(0) << std::endl;
   std::cout << arr[2] << std::endl;
   std::cout << arr.at(2) << std::endl;
}
```

<details>
<summary>Что делает <code>arr.at</code></summary>

`at` дает доступ к элементу, точно так же как индексирование (`arr[...]`),
но помимо этого делает проверку длины.
Если заданный индекс за пределами массива, программа крашнется.

> На самом деле выбросится исключение, которое можно поймать, но это мы не проходим.
</details>

<details>
<summary>Ответ</summary>

`arr[0]` как обычно считает значение первого элемента из массива.

`arr.at(0)` сделает то же самое, после удачной проверки на длину.
Проверка на длину успешна, потому что в массиве есть индекс `0`,
так как длина больше `0`.

`arr[2]` это UB (обсуждалось ранее).

`arr.at(2)` крашнет программу при проверке длины.
Проверка на длину не успешна, поскольку в массиве нет индекса `2`,
так как длина не есть больше `2`.

> Эта проверка на длину грамотно называется "bounds-check".

> `at` существует для `std::span` начиная со стандарта `C++ 26`.
</details>

### 20. Передача `std::span` параметром
```cpp
#include <iostream>
#include <array>
#include <span>

void print(std::span<int> s)
{
   for (size_t i = 0; i < s.size(); i++)
   {
       std::cout << s[i] << std::endl;
   }
}

int main()
{
   std::array<int, 3> arr{ 1, 2, 3 };
   std::span<int> span{ arr };
   print(span);

   print({ arr });
   print(arr);
}
```

<details>
<summary>Ответ</summary>

Все 3 синтаксиса `print(span)`, `print({ arr })` и `print(arr)` сработают и сделают то же самое.

`print(span)` передаст копию уже созданного `span`.

`print({ arr })` и `print(arr)` инициализируют временный 
`std::span<int>` и передадут его функции `print`.

В каждом случае, `print` пройдется циклом по элементам `arr` из `main` и напечатает их.
</details>

### 21. Подспан вручную
```cpp
#include <iostream>
#include <array>
#include <span>

void print(std::span<int> s)
{
   for (size_t i = 0; i < s.size(); i++)
   {
       std::cout << s[i] << std::endl;
   }
}

int main()
{
   std::array<int, 4> arr{1, 2, 3, 4};
   std::span<int> wholeSpan{ arr };
   std::span<int> span123{ arr.data(), 3 };
   std::span<int> span234{ arr.data() + 1, 3 };

   print(wholeSpan);

   std::cout << std::endl;
   print(span123);

   std::cout << std::endl;
   print(span234);
}
```

<details>
<summary>Ответ</summary>

`std::span` можно создать как из всего массива, так и из отдельно *указателя* и *длины*.

Например, `std::span<int> span123{ arr.data(), 3 };` передает:
- Адрес начала массива (`arr.data()`) как указатель,
- `3` как длину.

`std::span<int> span234{ arr.data() + 1, 3 };` передает:
- Адрес второго элемента массива (`arr.data() + 1` = `&arr[1]`) как указатель,
- `3` как длину.

При печати `span123` напечатаются первые 3 элемента.

При печати `span234` напечатаются 3 элемента, начиная со второго (2, 3 и 4).
</details>

### 22. Понимание метода `data`

Что будет, если сменить
```cpp
std::span<int> span123{ arr.data(), 3 };
std::span<int> span234{ arr.data() + 1, 3 };
```
на 
```cpp
std::span<int> span123{ wholeSpan.data(), 3 };
std::span<int> span234{ span123.data() + 1, 3 };
```
в предыдущем примере?

<details>
<summary>Ответ:</summary>

`data` для `std::span` возвращает сохраненный в нем указатель.

Результат будет тот же, поскольку и в `wholeSpan` и в `span123` были
сохранены указатели на первый элемент из `arr`.
</details>

### 23. Подспан методом `subspan`
```cpp
#include <iostream>
#include <array>
#include <span>

void print(std::span<int> s)
{
   for (size_t i = 0; i < s.size(); i++)
   {
       std::cout << s[i] << std::endl;
   }
}

int main()
{
   std::array<int, 4> arr{1, 2, 3, 4};
   std::span<int> wholeSpan{ arr };
   std::span<int> span123{ wholeSpan.subspan(0, 3) };
   std::span<int> span234{ wholeSpan.subspan(1, 3) };

   print(wholeSpan);

   std::cout << std::endl;
   print(span123);

   std::cout << std::endl;
   print(span234);
}
```

<details>
<summary>Ответ</summary>

`subspan` принимает 2 аргумента:
- *С какого индекса* начать;
- Какая будет длина.

`wholeSpan.subspan(0, 3)` говорит начать с индекса `0`, с длиной `3`.
Это эквивалентно `wholeSpan.data() + 0, 3`.

`wholeSpan.subspan(1, 3)` говорит начать с индекса `1`, с длиной `3`.
Это эквивалентно `wholeSpan.data() + 1, 3`.

Если параметр длины опустить, он определится сам так, 
чтобы `span` шел до конца массива.

Например, вместо `wholeSpan.subspan(1, 3)` можно сделать `wholeSpan.subspan(1)`.
</details>

### 24. Тонкости `subspan`

Что если в предыдущем примере выйти за рамки массива, например вот так:
```cpp
std::span<int> s{ wholeSpan.subspan(2, 3) };
```

<details>
<summary>Ответ</summary>

Тут не делается bounds-checking, это просто UB при считывании из позиции `2` в `s`

> Создание некорректного `std::span` не считается UB, 
> по аналогии с указателями, а вот считывание за пределами массива считается.
</details>

### 25. Цикл в обратную сторону (1)

Что выведется здесь?
```cpp
#include <iostream>
#include <array>
#include <span>
#include <cassert>

void print(std::span<int> s)
{
   int lastIndex = static_cast<int>(s.size()) - 1;
   for (int i { lastIndex }; i >= 0; i--)
   {
       size_t si = static_cast<size_t>(i);
       assert(si < s.size());

       std::cout << s[si] << std::endl;
   }
}

int main()
{
   std::array<int, 4> arr{1, 2, 3, 4};
   print({ arr });
}
```

<details>
<summary>Ответ</summary>

В примере элементы массива печатаются в обратном порядке.

`static_cast` используются, чтобы обойти предупреждения 
о возможной потере информации (narrowing conversion из `size_t` в `int`)
и неявной смене знака (из `int` в `size_t`).
</details>

### 26. Цикл в обратную сторону (2)

Что выведется здесь?
```cpp
#include <iostream>
#include <array>
#include <span>
#include <cassert>

void print(std::span<int> s)
{
   for (size_t i { s.size() - 1 }; i >= 0; i--)
   {
       assert(i < s.size());

       std::cout << s[i] << std::endl;
   }
}

int main()
{
   std::array<int, 4> arr{1, 2, 3, 4};
   print({ arr });
}
```

<details>
<summary>Ответ</summary>

Напечатаются все элементы, затем программа крашнется.

Так как `i` — это тип без знака, 
`0 - 1` как `size_t` будет не `-1`, а случится underflow и число станет максимальным.
Тогда `assert(i < s.size())` крашнет программу, поскольку `i` станет больше размера массива.

Это можно обойти, если делать проверку вручную:

```cpp
void print(std::span<int> s)
{
   if (s.size() == 0)
   {
       return;
   }
   size_t i { s.size() - 1 };
   while (true)
   {
       assert(i < s.size());
       std::cout << s[i] << std::endl;
       if (i == 0)
       {
           return;
       }
       i--;
   }
}
```

Или считать максимальное значение недопустимым индексом и делать проверку на `-1` как `size_t`:

```cpp
void print(std::span<int> s)
{
   for (size_t i { s.size() - 1 }; i != static_cast<size_t>(-1); i--)
   {
       assert(i < s.size());
       std::cout << s[i] << std::endl;
   }
}
```
</details>

### 27. Итерация указателями (1)
```cpp
#include <iostream>
#include <array>
#include <cassert>

void print(int* start, int* end)
{
   for (int* current{start}; current <= end; current++)
   {
       std::cout << *current << std::endl;
   }
}

int main()
{
   std::array<int, 4> arr{1, 2, 3, 4};
   print(arr.data(), &arr[arr.size() - 1]);
}
```

<details>
<summary>Ответ</summary>

Здесь иллюстрируется другой подход к пределам итерации.
Цикл работает не исходя из количества элементов в массиве, 
а исходя из первого и последнего адреса.
</details>

### 28. Итерация указателями (2)
```cpp
#include <iostream>
#include <array>
#include <cassert>

void print(int* start, int* pastEnd)
{
   for (int* current{start}; current != pastEnd; current++)
   {
       std::cout << *current << std::endl;
   }
}

int main()
{
   std::array<int, 4> arr{1, 2, 3, 4};
   print(arr.data(), &arr[arr.size()]);
   print(arr.begin(), arr.end());
}
```

<details>
<summary>Ответ</summary>

Здесь применяется подход итераторов: вместо адреса последнего элемента
передается *первый адрес после последнего*.

`arr.begin()` возвращает *итератор* (есть в другой теме) первого элемента,
а `arr.end()` возвращает итератор последнего.
Итераторы можно автоматически конвертировать в адреса, 
что и происходит при их передачи как параметр.
</details>
