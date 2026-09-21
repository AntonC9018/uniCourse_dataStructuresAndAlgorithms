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
#include <iostream>

struct OptionalInt
{
    bool has_value;
    int value;
};

const OptionalInt NO_VALUE{ false, 0 };

int main()
{
    OptionalInt arr[3]{ { true, 1 }, NO_VALUE, { true, 3 } };

    int i{ 0 };
    while (i < 3)
    {
        if (arr[i].has_value)
        {
            std::cout << arr[i].value << std::endl;
        }
        else
        {
            std::cout << "empty" << std::endl;
        }
        i = i + 1;
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

`std::optional<int>` — это стандартная версия самодельной структуры из прошлого примера.
В нём либо хранится `int`, либо ничего нет.

- `a` хранит значение: `std::optional<int>{ 5 }` создаёт optional со значением `5`,
  поэтому `has_value()` — это `true`, а `value()` даст `5`.
- `b` пустой: `std::nullopt` означает «нет значения»,
  поэтому `has_value()` — это `false`, `value()` вызывать нельзя,
  а вместо этого печатается `"empty"`.

Напечатается `5` и `"empty"`.
</details>

### 6. Константа для пустого значения (`std::optional`)
```cpp
#include <iostream>
#include <optional>

const std::optional<int> NO_VALUE{ std::nullopt };

int main()
{
    std::optional<int> a{ 5 };
    std::optional<int> b{ NO_VALUE };

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

Это аналог самодельной константы из прошлого примера,
но со стандартным типом: `NO_VALUE` — это пустой `std::optional<int>`.

Напечатается `5` и `"empty"`.
</details>

### 7. Функция, возвращающая optional (`std::optional`)
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

### 8. Массив из optional (`std::optional`)
```cpp
#include <iostream>
#include <optional>

const std::optional<int> NO_VALUE{ std::nullopt };

int main()
{
    std::optional<int> arr[3]{ 1, NO_VALUE, 3 };

    int i{ 0 };
    while (i < 3)
    {
        if (arr[i].has_value())
        {
            std::cout << arr[i].value() << std::endl;
        }
        else
        {
            std::cout << "empty" << std::endl;
        }
        i = i + 1;
    }
}
```

<details>
<summary>Ответ</summary>

Это тот же цикл, что и в самодельном примере, но со стандартным типом.
Обычный литерал `1` неявно преобразуется в `std::optional<int>` со значением `1`.

Напечатается `1`, `"empty"`, `3`.
</details>
