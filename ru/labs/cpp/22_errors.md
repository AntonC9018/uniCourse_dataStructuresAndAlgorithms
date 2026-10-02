---
slug: ru/cpp/labs/errors
---
<!-- course-site-backlink:start -->
[Этот урок на сайте](https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms/ru/cpp/labs/errors/)
<!-- course-site-backlink:end -->
# Ошибки

- [Проверка данных и способы сообщать об ошибках](../../../en/07_serialization/doc.md#validation)

## Концепты

- Ожидаемые ошибки и ошибки программиста
- Признак успеха в виде bool и вывод диагностических сообщений
- Причины ошибок в виде enum
- Выходные значения через параметры-указатели и параметры-ссылки
- Нулевые указатели, собственные структуры результата и `std::optional`
- Сбор нескольких ошибок в вектор, переданный по ссылке
- Assert: предположения, завершение программы, тесты и отключение проверок

## Вопросы на понимание

Для каждого примера определите, что выведется и дойдёт ли выполнение до конца.
Как вызывающая функция узнаёт об успехе? Когда возвращённое или выходное значение имеет смысл?

Каждый блок кода — отдельная программа. Если явно не указано иное, проверки assert включены.

### 1. Возврат bool

```cpp
#include <iostream>

bool isValidAmount(int amount)
{
    return amount >= 0;
}

int main()
{
    std::cout << isValidAmount(3) << std::endl;
    std::cout << isValidAmount(-1) << std::endl;
}
```

<details>
<summary>Ответ</summary>

Выведутся `1` и `0`: без `std::boolalpha` именно так выводятся `true` и `false`.
Функция использует `true` для успеха и `false` для ошибки.
Это соглашение данного интерфейса: сам тип `bool` не задаёт смысл этих значений.
По bool можно узнать, прошла ли проверка, но нельзя узнать причину ошибки.
</details>

### 2. Вывод сообщения об ошибке

```cpp
#include <iostream>

bool isValidAmount(int amount)
{
    if (amount < 0)
    {
        std::cerr << "amount must not be negative" << std::endl;
        return false;
    }
    return true;
}

int main()
{
    bool valid = isValidAmount(-1);
    std::cout << valid << std::endl;
}
```

<details>
<summary>Ответ</summary>

В стандартный поток ошибок выводится `amount must not be negative`, а в стандартный поток вывода — `0`.
`std::cerr` — поток для диагностических сообщений; здесь он используется так же, как `std::cout`.
В терминале обычно видны оба потока; их общий вид зависит от способа вывода и перенаправления.

Сообщение объясняет человеку, что произошло. Вызывающая функция по-прежнему получает только `false`: вывод сообщения не передаёт другим функциям отдельный код причины ошибки.
</details>

### 3. Возврат причины ошибки

```cpp
#include <iostream>

enum class ValidationError
{
    None,
    NegativeAmount,
    NegativePrice,
};

ValidationError validateOrder(int amount, int price)
{
    if (amount < 0)
    {
        return ValidationError::NegativeAmount;
    }
    if (price < 0)
    {
        return ValidationError::NegativePrice;
    }
    return ValidationError::None;
}

int main()
{
    ValidationError result = validateOrder(-1, -2);
    std::cout << (result == ValidationError::NegativeAmount) << std::endl;
    std::cout << (result == ValidationError::NegativePrice) << std::endl;
    std::cout << (validateOrder(3, 4) == ValidationError::None) << std::endl;
}
```

<details>
<summary>Ответ</summary>

Выведутся `1`, `0` и `1`.
Enum позволяет отличить успех от конкретных причин ошибки, не разбирая текст сообщения.
Хотя оба аргумента первого вызова недопустимы, первый `return` сразу завершает функцию.
Возвращается только `NegativeAmount`; до проверки цены выполнение не доходит.
</details>

### 4. Bool и выходной параметр-указатель

```cpp
#include <iostream>

bool tryHalf(int input, int* output)
{
    if (input < 0)
    {
        return false;
    }
    *output = input / 2;
    return true;
}

int main()
{
    int value = 99;
    bool success = tryHalf(8, &value);
    std::cout << success << std::endl;
    std::cout << value << std::endl;

    success = tryHalf(-1, &value);
    std::cout << success << std::endl;
    std::cout << value << std::endl;
}
```

<details>
<summary>Ответ</summary>

Выведутся `1`, `4`, `0` и `4`.
Функция возвращает признак успеха, а вычисленное значение записывает через параметр-указатель.
Она принимает неотрицательные числа и использует целочисленное деление.

При ошибке функция завершает работу до присваивания в `*output`, поэтому выходное значение остаётся без изменений.
Второе `4` — результат предыдущего успешного вызова, а не новый результат для `-1`.
Здесь `output` должен указывать на существующий объект типа `int`: этот параметр обязателен.
</details>

### 5. Тот же выходной параметр через ссылку

```cpp
#include <iostream>

bool tryHalf(int input, int& output)
{
    if (input < 0)
    {
        return false;
    }
    output = input / 2;
    return true;
}

int main()
{
    int value = 99;
    bool success = tryHalf(8, value);
    std::cout << success << std::endl;
    std::cout << value << std::endl;

    success = tryHalf(-1, value);
    std::cout << success << std::endl;
    std::cout << value << std::endl;
}
```

<details>
<summary>Ответ</summary>

Выведутся те же `1`, `4`, `0` и `4`.
Параметр-ссылка ссылается на переменную в вызывающей функции, поэтому присваивание в `output` меняет `value`.
При вызове передаётся `value`, а не его адрес.
Соглашение об успехе и ошибке не меняется; кроме того, ссылка не позволяет обозначить отсутствие выходного объекта через `nullptr`.
</details>

### 6. Игнорирование признака успеха

```cpp
#include <iostream>

bool tryHalf(int input, int& output)
{
    if (input < 0)
    {
        return false;
    }
    output = input / 2;
    return true;
}

int main()
{
    int value = 99;
    tryHalf(-1, value);
    std::cout << value << std::endl;
}
```

<details>
<summary>Ответ</summary>

Выведется `99`.
Вызов возвращает `false`, но этот признак ошибки игнорируется.
В `value` остаётся старое значение; считать его успешно вычисленным результатом было бы логической ошибкой.
Используйте выходное значение как новый результат только после проверки успеха.
Здесь `99` — обычное инициализированное значение: читать его можно, но это не запрошенный результат.
</details>

### 7. Enum и выходное значение

```cpp
#include <iostream>

enum class HalfError
{
    None,
    NegativeInput,
};

HalfError tryHalf(int input, int& output)
{
    if (input < 0)
    {
        return HalfError::NegativeInput;
    }
    output = input / 2;
    return HalfError::None;
}

int main()
{
    int value = 99;
    HalfError error = tryHalf(-1, value);
    if (error == HalfError::None)
    {
        std::cout << value << std::endl;
    }
    else if (error == HalfError::NegativeInput)
    {
        std::cout << "negative input" << std::endl;
    }
}
```

<details>
<summary>Ответ</summary>

Выведется `negative input`.
Здесь выходной параметр объединяется с признаком ошибки в виде enum.
`None` означает успех, а остальные значения объясняют причину ошибки.
Вызывающая функция проверяет признак успеха, прежде чем использовать выходное значение как результат.
Enum особенно полезен, когда возможны разные причины ошибки.
</details>

### 8. Нулевой указатель означает ошибку

```cpp
#include <iostream>
#include <span>

int* findValue(std::span<int> values, int wanted)
{
    for (int& value : values)
    {
        if (value == wanted)
        {
            return &value;
        }
    }
    return nullptr;
}

int main()
{
    int values[]{ 3, 5, 7 };
    int* found = findValue(values, 5);
    if (found != nullptr)
    {
        *found = 6;
    }
    std::cout << values[1] << std::endl;

    int* missing = findValue(values, 9);
    std::cout << (missing == nullptr) << std::endl;
}
```

<details>
<summary>Ответ</summary>

Выведутся `6` и `1`.
При успехе возвращается адрес существующего элемента массива, а при ошибке — `nullptr`.
Перед разыменованием указатель нужно проверить.
Так можно узнать, найдено ли значение, но дополнительной причины ошибки указатель не сообщает.

Возвращённый указатель указывает на элемент массива в вызывающей функции, а не к локальной копии внутри `findValue`.
Массив продолжает существовать, пока используется `found`; ссылка в цикле обозначает его настоящий элемент.
</details>

### 9. Возврат собственной структуры результата

```cpp
#include <iostream>

struct HalfResult
{
    bool success;
    int value;
};

HalfResult tryHalf(int input)
{
    if (input < 0)
    {
        return { false, 0 };
    }
    return { true, input / 2 };
}

int main()
{
    HalfResult result = tryHalf(8);
    if (result.success)
    {
        std::cout << result.value << std::endl;
    }

    result = tryHalf(-1);
    if (result.success)
    {
        std::cout << result.value << std::endl;
    }
    else
    {
        std::cout << "failure" << std::endl;
    }
}
```

<details>
<summary>Ответ</summary>

Выведутся `4` и `failure`.
Структура возвращает признак успеха и значение вместе, без выходного параметра.
При ошибке `value` инициализируется нулём, но при `success == false` это поле не является успешным результатом.
Это собственная структура optional из [лабораторной по optional](16_optional.md), применённая к вычислению, которое может завершиться ошибкой.
Если вызывающей функции нужна причина ошибки, вместо bool можно использовать поле типа enum.
</details>

### 10. Возврат std::optional

```cpp
#include <iostream>
#include <optional>

std::optional<int> tryHalf(int input)
{
    if (input < 0)
    {
        return std::nullopt;
    }
    return input / 2;
}

int main()
{
    std::optional<int> result = tryHalf(8);
    if (result.has_value())
    {
        std::cout << *result << std::endl;
    }

    result = tryHalf(-1);
    if (result.has_value())
    {
        std::cout << *result << std::endl;
    }
    else
    {
        std::cout << "failure" << std::endl;
    }
}
```

<details>
<summary>Ответ</summary>

Выведутся те же `4` и `failure`.
`std::optional<int>` обозначает либо целочисленный результат, либо его отсутствие.
`std::nullopt` задаёт пустое состояние, а перед разыменованием вызывающая функция проверяет `has_value()`.
Как и bool, само пустое состояние не объясняет причину ошибки.
</details>

### 11. Сбор нескольких ошибок

```cpp
#include <iostream>
#include <vector>

enum class ValidationError
{
    None,
    NegativeAmount,
    NegativePrice,
};

bool validateOrder(int amount, int price, std::vector<ValidationError>& errors)
{
    bool valid = true;
    if (amount < 0)
    {
        errors.push_back(ValidationError::NegativeAmount);
        valid = false;
    }
    if (price < 0)
    {
        errors.push_back(ValidationError::NegativePrice);
        valid = false;
    }
    return valid;
}

int main()
{
    std::vector<ValidationError> errors;
    bool valid = validateOrder(-1, -2, errors);
    std::cout << valid << std::endl;
    std::cout << errors.size() << std::endl;
    for (ValidationError error : errors)
    {
        std::cout << static_cast<int>(error) << std::endl;
    }
}
```

<details>
<summary>Ответ</summary>

Выведутся `0`, `2`, `1` и `2`.
`std::vector<ValidationError>` хранит список кодов ошибок; `push_back` добавляет одно значение в конец, а `size()` даёт текущее количество значений.
Вектор передаётся по ссылке, поэтому функция добавляет ошибки в список вызывающей функции.

В отличие от предыдущего примера с enum, ни одна ошибка не приводит к немедленному возврату.
Выполняются обе проверки: сначала записывается `NegativeAmount`, затем `NegativePrice`.
Возвращённый bool показывает, найдены ли ошибки именно в этом вызове.
</details>

### 12. Повторное использование списка ошибок

```cpp
#include <iostream>
#include <vector>

enum class ValidationError
{
    None,
    NegativeAmount,
    NegativePrice,
};

bool validateOrder(int amount, int price, std::vector<ValidationError>& errors)
{
    bool valid = true;
    if (amount < 0)
    {
        errors.push_back(ValidationError::NegativeAmount);
        valid = false;
    }
    if (price < 0)
    {
        errors.push_back(ValidationError::NegativePrice);
        valid = false;
    }
    return valid;
}

int main()
{
    std::vector<ValidationError> errors;
    validateOrder(-1, -2, errors);
    bool valid = validateOrder(3, 4, errors);
    std::cout << valid << std::endl;
    std::cout << errors.size() << std::endl;
}
```

<details>
<summary>Ответ</summary>

Выведутся `1` и `2`.
Второй вызов успешен, но не удаляет ошибки, записанные первым вызовом.
Функция добавляет новые ошибки; возвращённый bool относится только к текущей проверке.
Накапливаемый список может хранить результаты нескольких проверок.
Если для каждого вызова нужен отдельный список, следует создать новый вектор или заранее вызвать `errors.clear()`.
</details>

### 13. Успешная проверка assert

```cpp
#include <iostream>
#include <cassert>

int main()
{
    int amount = 3;
    assert(amount >= 0);
    std::cout << amount << std::endl;
}
```

<details>
<summary>Ответ</summary>

При включённых проверках assert выведется `3`.
`assert` из `<cassert>` проверяет условие, которое должно быть истинным.
Если условие истинно, выполнение продолжается.
В отличие от возвращённого bool, assert не сообщает вызывающей функции об ошибке, после которой можно продолжить работу.
</details>

### 14. Неуспешная проверка assert

```cpp
#include <iostream>
#include <cassert>

int main()
{
    int amount = -1;
    assert(amount >= 0);
    std::cout << "after assert" << std::endl;
}
```

<details>
<summary>Ответ</summary>

При включённых проверках assert условие оказывается ложным: выводится диагностическое сообщение, и программа завершается вызовом `std::abort`.
`after assert` не выведется. Точный текст диагностического сообщения зависит от реализации.
Assert обнаруживает нарушение предположения; он не возвращает `false` и не даёт вызывающей функции выбрать обычную ветку обработки ошибки.

Если при компиляции определён `NDEBUG`, assert ничего не проверяет и не вычисляет своё выражение.
Тогда программа выведет `after assert`.
Не используйте assert как единственную проверку ожидаемых ошибок во входных данных.
</details>

### 15. Assert для проверки условия использования выходного параметра

```cpp
#include <iostream>
#include <cassert>

bool tryHalf(int input, int* output)
{
    assert(output != nullptr);
    if (input < 0)
    {
        return false;
    }
    *output = input / 2;
    return true;
}

int main()
{
    int value = 99;
    bool success = tryHalf(-1, &value);
    std::cout << success << std::endl;
    std::cout << value << std::endl;

    success = tryHalf(8, &value);
    std::cout << success << std::endl;
    std::cout << value << std::endl;
}
```

<details>
<summary>Ответ</summary>

При включённых проверках assert выведутся `0`, `99`, `1` и `4`.
Этот интерфейс требует передавать существующий выходной объект.
Assert проверяет, что вызывающая функция не передала `nullptr`; в обоих вызовах это условие выполнено.
Нулевой указатель при таком соглашении означал бы ошибку программиста, а не допустимый способ обозначить отсутствие выходного объекта.

Отрицательное входное значение — ожидаемая ошибка, о которой функция сообщает через `false`, поэтому программа может продолжить работу.
Даже при отключённых проверках assert вызывающая функция обязана выполнить требование к выходному указателю.
Это показывает, почему assert и обычная обработка ошибок решают разные задачи.
</details>

### 16. Проверка успеха и ошибки через assert

```cpp
#include <iostream>
#include <cassert>

bool tryHalf(int input, int& output)
{
    if (input < 0)
    {
        return false;
    }
    output = input / 2;
    return true;
}

int main()
{
    int value = 99;
    bool success = tryHalf(8, value);
    assert(success);
    assert(value == 4);

    success = tryHalf(-1, value);
    assert(!success);
    assert(value == 4);
    std::cout << "tests passed" << std::endl;
}
```

<details>
<summary>Ответ</summary>

При включённых проверках assert выведется `tests passed`.
Проверки подтверждают и успешный результат, и обещанное сохранение выходного значения при ошибке.
Если ожидание не выполнится, программа остановится на соответствующей проверке.

Вызовы `tryHalf` вынесены из assert, поэтому они выполняются и при отключённых проверках.
Не помещайте необходимые действия только внутрь assert: его выражение может вообще не вычисляться.
При отключённых проверках само сообщение не доказывает, что результаты были проверены.
</details>

[Размеченным объединениям и флагам](32_tagged_unions_and_flags.md) и [исключениям](33_exceptions.md) посвящены отдельные лабораторные в конце курса.
