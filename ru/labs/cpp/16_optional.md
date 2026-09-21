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

### 2. `std::optional<int>`
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
