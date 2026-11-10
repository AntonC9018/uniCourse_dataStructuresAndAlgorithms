---
slug: ru/cpp/labs/optional
---
<!-- course-site-backlink:start -->
[Этот урок на сайте](https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms/ru/cpp/labs/optional/)
<!-- course-site-backlink:end -->
# `std::optional`

## Концепты

- Значение, которого может не быть
- Самодельный optional в виде структуры (`has_value` + `value`)
- `std::optional<int>`
- Пустое состояние и состояние со значением
- `std::nullopt`, `has_value()`
- Константа для пустого значения
- Возвращение optional из функции
- Массив из optional
- Сигнальные значения (`-1` — нет индекса, `std::string::npos`)
- Указатели уже хранят null (`nullptr`)

## Примеры на понимание

### 1. Самодельный optional в виде структуры
```cpp
#include <iostream>

struct OptionalInt
{
    bool has_value;
    int value;
};

int main()
{
    OptionalInt a{ true, 5 };
    OptionalInt b{ false, 0 };

    if (a.has_value)
    {
        std::cout << a.value << std::endl;
    }

    if (b.has_value)
    {
        std::cout << b.value << std::endl;
    }
    else
    {
        std::cout << "empty" << std::endl;
    }
}
```

<details>
<summary>Ответ</summary>

Иногда значение может отсутствовать, и это нужно показать явно.
Здесь `has_value` показывает, можно ли использовать `value`.

- `a` хранит значение: `has_value` — это `true`, поэтому печатается `a.value` (`5`).
- `b` пустой: `has_value` — это `false`, поэтому `b.value` (`0`) игнорируется,
  а вместо этого печатается `"empty"`.

В этой паре «флаг + значение» и заключается суть optional.
</details>

### 2. Константа для пустого значения
```cpp
#include <iostream>

struct OptionalInt
{
    bool has_value;
    int value;
};

const OptionalInt NO_VALUE{ false, 0 };

int main()
{
    OptionalInt a{ true, 5 };
    OptionalInt b{ NO_VALUE };

    if (a.has_value)
    {
        std::cout << a.value << std::endl;
    }

    if (b.has_value)
    {
        std::cout << b.value << std::endl;
    }
    else
    {
        std::cout << "empty" << std::endl;
    }
}
```

<details>
<summary>Ответ</summary>

Пустому состоянию дают имя, чтобы каждый пустой optional записывался одинаково.
В `NO_VALUE` лежит `has_value = false`, а `0` в нём никогда не читается —
он там лишь потому, что в `value` должно лежать хоть что-то.

`b` инициализируется константой, поэтому он пустой, как и в прошлом примере.

Напечатается `5` и `"empty"`.
</details>

### 3. Функция, возвращающая optional
```cpp
#include <iostream>

struct OptionalInt
{
    bool has_value;
    int value;
};

const OptionalInt NO_VALUE{ false, 0 };

OptionalInt divide(int a, int b)
{
    if (b == 0)
    {
        return NO_VALUE;
    }
    return OptionalInt{ true, a / b };
}

int main()
{
    OptionalInt a{ divide(7, 2) };
    OptionalInt b{ divide(7, 0) };

    if (a.has_value)
    {
        std::cout << a.value << std::endl;
    }

    if (b.has_value)
    {
        std::cout << b.value << std::endl;
    }
    else
    {
        std::cout << "empty" << std::endl;
    }
}
```

<details>
<summary>Ответ</summary>

Функция может возвращать optional, чтобы показать отсутствие результата.
У деления на ноль результата нет, поэтому `divide` в этом случае возвращает `NO_VALUE`.

- `divide(7, 2)` возвращает optional со значением `3`;
- `divide(7, 0)` возвращает пустую константу, поэтому вместо значения печатается `"empty"`.

Напечатается `3` и `"empty"`.
</details>

### 4. Массив из optional
```cpp
#include <array>
#include <iostream>

struct OptionalInt
{
    bool has_value;
    int value;
};

const OptionalInt NO_VALUE{ false, 0 };

int main()
{
    std::array<OptionalInt, 3> arr{
        { true, 1 },
        NO_VALUE,
        { true, 3 },
    };

    for (OptionalInt el : arr)
    {
        if (el.has_value)
        {
            std::cout << el.value << std::endl;
        }
        else
        {
            std::cout << "empty" << std::endl;
        }
    }
}
```

<details>
<summary>Ответ</summary>

Каждый элемент проверяется по очереди: если в нём есть значение, оно печатается,
иначе печатается `"empty"`.

Напечатается `1`, `"empty"`, `3`.
</details>

### 5. `std::optional<int>`
```cpp
#include <iostream>
#include <optional>

int main()
{
    std::optional<int> a{ 5 };
    std::optional<int> b{ std::nullopt };

    if (a.has_value())
    {
        std::cout << a.value() << std::endl;
    }

    if (b.has_value())
    {
        std::cout << b.value() << std::endl;
    }
    else
    {
        std::cout << "empty" << std::endl;
    }
}
```

<details>
<summary>Ответ</summary>

`std::optional<int>` — это стандартная версия самодельной структуры из прошлых примеров.
В нём либо хранится `int`, либо ничего нет.

- `a` хранит значение: `std::optional<int>{ 5 }` создаёт optional со значением `5`,
  поэтому `has_value()` — это `true`, а `value()` даст `5`.
- `b` пустой: `std::nullopt` означает «нет значения»,
  поэтому `has_value()` — это `false`, `value()` вызывать нельзя,
  а вместо этого печатается `"empty"`.

Напечатается `5` и `"empty"`.
</details>

### 6. Функция, возвращающая optional (`std::optional`)
```cpp
#include <iostream>
#include <optional>

std::optional<int> divide(int a, int b)
{
    if (b == 0)
    {
        return std::nullopt;
    }
    return a / b;
}

int main()
{
    std::optional<int> a{ divide(7, 2) };
    std::optional<int> b{ divide(7, 0) };

    if (a.has_value())
    {
        std::cout << a.value() << std::endl;
    }

    if (b.has_value())
    {
        std::cout << b.value() << std::endl;
    }
    else
    {
        std::cout << "empty" << std::endl;
    }
}
```

<details>
<summary>Ответ</summary>

Это тот же `divide`, что и в самодельном примере, но со стандартным типом.
Деление на ноль возвращает `std::nullopt`.

В `return a / b;` фигурные скобки не нужны: обычный `int` неявно
преобразуется в `std::optional<int>` с этим значением.

Напечатается `3` и `"empty"`.
</details>

### 7. Массив из optional (`std::optional`)
```cpp
#include <array>
#include <iostream>
#include <optional>

int main()
{
    std::array<std::optional<int>, 3> arr{
        1,
        std::nullopt,
        3,
    };

    for (std::optional<int> x : arr)
    {
        if (x.has_value())
        {
            std::cout << x.value() << std::endl;
        }
        else
        {
            std::cout << "empty" << std::endl;
        }
    }
}
```

<details>
<summary>Ответ</summary>

Это тот же цикл, что и в самодельном примере, но со стандартным типом.
Обычный литерал `1` неявно преобразуется в `std::optional<int>` со значением `1`.

Напечатается `1`, `"empty"`, `3`.
</details>

### 8. Сигнальное значение вместо optional
```cpp
#include <array>
#include <iostream>

const int NO_INDEX = -1;

int findIndex(std::array<int, 4> arr, int target)
{
    for (int i = 0; i < 4; i++)
    {
        if (arr[i] == target)
        {
            return i;
        }
    }
    return NO_INDEX;
}

int main()
{
    std::array<int, 4> arr{ 5, 8, 2, 8 };
    int a{ findIndex(arr, 8) };
    int b{ findIndex(arr, 7) };

    std::cout << a << std::endl;

    if (b == NO_INDEX)
    {
        std::cout << "not found" << std::endl;
    }
}
```

<details>
<summary>Ответ</summary>

Индекс не бывает отрицательным, поэтому одно невозможное значение, `-1`,
можно зарезервировать под «индекса нет».
Такое зарезервированное значение называют *сигнальным* (sentinel value).
Дополнительный флаг не нужен: пустое состояние хранится в самом `int`.

- `8` впервые встречается по индексу `1`, поэтому `a` равно `1`;
- `7` в массиве нет, поэтому `b` равно `NO_INDEX`.

Выведутся `1` и `"not found"`.

Минус в том, что ничто не заставляет вызывающий код делать проверку:
`arr[b]` скомпилируется и прочитает память за пределами массива (UB).
</details>

### 9. `std::string::npos`
```cpp
#include <iostream>
#include <string>

int main()
{
    std::string s{ "hello" };
    size_t a{ s.find('l') };
    size_t b{ s.find('z') };

    std::cout << a << std::endl;

    if (b == std::string::npos)
    {
        std::cout << "not found" << std::endl;
    }
}
```

<details>
<summary>Ответ</summary>

Стандартная библиотека тоже пользуется сигнальными значениями.
`find` возвращает индекс первого подходящего символа
или `std::string::npos`, если такого нет.

Тип индекса `size_t` беззнаковый, так что `-1` не подходит.
Вместо этого `npos` — наибольшее значение `size_t`
(по сути, он так и определён: `-1`, приведённое к `size_t`).
Строк такой длины не бывает, так что этот индекс тоже невозможен.

Выведутся `2` и `"not found"`.

У `std::optional` нельзя выбрать сигнальное значение:
`std::optional<size_t>` всегда хранит рядом со значением отдельный флаг.
</details>

### 10. Когда для сигнального значения нет свободного места
```cpp
#include <iostream>

const int NO_VALUE = -1;

int divide(int a, int b)
{
    if (b == 0)
    {
        return NO_VALUE;
    }
    return a / b;
}

int main()
{
    std::cout << divide(7, 0) << std::endl;
    std::cout << divide(-7, 7) << std::endl;
}
```

<details>
<summary>Ответ</summary>

Оба раза выведется `-1`.
Вызывающий код не может отличить ошибку от настоящего результата:
результатом деления может быть любой `int`, так что свободного значения под сигнальное не остаётся.
Здесь нужен optional, как в примерах с `divide` выше.

Сигнальное значение подходит, только когда какое-то значение типа
не может быть настоящим результатом — как отрицательный индекс.
</details>

### 8. Указатель уже может хранить null
```cpp
#include <iostream>

int main()
{
    int a{ 5 };
    int* p{ &a };
    int* q{ nullptr };

    if (p != nullptr)
    {
        std::cout << *p << std::endl;
    }

    if (q != nullptr)
    {
        std::cout << *q << std::endl;
    }
    else
    {
        std::cout << "empty" << std::endl;
    }
}
```

<details>
<summary>Ответ</summary>

У указателей уже есть встроенное пустое состояние — `nullptr`.
Им не нужен отдельный флаг вроде `has_value`.

- `p` указывает на `a`, поэтому проверка проходит и печатается `5`;
- `q` хранит `nullptr`, поэтому проверка не проходит и вместо значения печатается `"empty"`.

Напечатается `5` и `"empty"`.
</details>

### 12. `std::optional` для указателей бессмысленен

`std::optional` для указателей бессмысленен: указатели и так могут хранить null,
а обратное — указатель, который гарантированно не null, — через optional выразить нельзя.
Если нужен такой указатель, следует передавать ссылку.

```cpp
#include <iostream>

void print(int* p)
{
    if (p != nullptr)
    {
        std::cout << *p << std::endl;
    }
}

void printRef(int& r)
{
    std::cout << r << std::endl;
}

int main()
{
    int a{ 5 };
    print(&a);
    print(nullptr);
    printRef(a);
}
```

<details>
<summary>Ответ</summary>

Оборачивание указателя в `std::optional<int*>` ничего не даёт:
у указателя уже есть `nullptr` для пустого состояния.

А гарантию «точно не null» optional дать не может.
Эту гарантию даёт ссылка: в `printRef` проверка не нужна,
потому что вызывающий обязан передать настоящую переменную.

Напечатается `5` дважды — из `print(&a)` и из `printRef(a)`.
`print(nullptr)` не печатает ничего.
</details>
