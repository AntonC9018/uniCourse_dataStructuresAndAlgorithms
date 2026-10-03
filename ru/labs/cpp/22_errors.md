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

struct Printer
{
    bool jammed;
};

bool printPage(Printer& printer)
{
    if (printer.jammed)
    {
        return false;
    }
    std::cout << "page printed" << std::endl;
    return true;
}

int main()
{
    Printer printer{ true };
    bool printed = printPage(printer);
    std::cout << printed << std::endl;

    printer.jammed = false;
    printed = printPage(printer);
    std::cout << printed << std::endl;
}
```

<details>
<summary>Ответ</summary>

Выведутся `0`, `page printed` и `1`.
`Printer` моделирует принтер, а `jammed` показывает, застряла ли в нём бумага.
Первый запрос не выполняется из-за застрявшей бумаги. После устранения этой проблемы второй запрос печатает страницу и завершается успешно.

Bool сообщает вызывающей функции, выполнена ли операция, но не передаёт причину ошибки.
Этот интерфейс использует `true` для успеха и `false` для ошибки.
</details>

### 2. Вывод сообщения об ошибке

```cpp
#include <iostream>

struct Printer
{
    bool jammed;
};

bool printPage(Printer& printer)
{
    if (printer.jammed)
    {
        std::cerr << "printer is jammed" << std::endl;
        return false;
    }
    std::cout << "page printed" << std::endl;
    return true;
}

int main()
{
    Printer printer{ true };
    bool printed = printPage(printer);
    std::cout << printed << std::endl;
}
```

<details>
<summary>Ответ</summary>

В стандартный поток ошибок выводится `printer is jammed`, а в стандартный поток вывода — `0`.
В `std::cerr` часть `err` означает *error*, то есть «ошибка». Это поток для диагностических сообщений; здесь он используется так же, как `std::cout`.

Сообщение объясняет человеку, что произошло, но вызывающая функция получает только `false`: конкретная причина ошибки в возвращаемом значении теряется.
Здесь это не так важно, потому что функция проверяет только одно условие: застряла ли бумага в принтере.
Если добавить другие проверки, по одному bool уже нельзя будет определить, какая из них не прошла.
</details>

### 3. Возврат причины ошибки

```cpp
#include <iostream>

enum class GradeError
{
    None,
    TooLow,
    TooHigh,
};

GradeError validateGrade(int grade)
{
    if (grade <= 0)
    {
        return GradeError::TooLow;
    }
    if (grade >= 10)
    {
        return GradeError::TooHigh;
    }
    return GradeError::None;
}

int main()
{
    std::cout << (validateGrade(0) == GradeError::TooLow) << std::endl;
    std::cout << (validateGrade(10) == GradeError::TooHigh) << std::endl;
    std::cout << (validateGrade(5) == GradeError::None) << std::endl;
}
```

<details>
<summary>Ответ</summary>

Выведутся `1`, `1` и `1`.
Этот интерфейс принимает оценку строго больше `0` и строго меньше `10`.
Один параметр проверяется по двум условиям: `0` слишком мало, `10` слишком много, а `5` допустимо.
Enum передаёт конкретную причину ошибки, поэтому вызывающая функция может различить две неудачные проверки, не разбирая текст сообщения.
</details>

### 4. Принтер с двумя причинами ошибки

```cpp
#include <iostream>

struct Printer
{
    bool jammed;
    int pagesLoaded;
};

enum class PrintError
{
    None,
    Jammed,
    NoPaper,
};

PrintError printPage(Printer& printer)
{
    if (printer.jammed)
    {
        return PrintError::Jammed;
    }
    if (printer.pagesLoaded == 0)
    {
        return PrintError::NoPaper;
    }
    printer.pagesLoaded -= 1;
    return PrintError::None;
}

int main()
{
    Printer printer{ true, 0 };
    PrintError error = printPage(printer);
    std::cout << (error == PrintError::Jammed) << std::endl;

    printer.jammed = false;
    error = printPage(printer);
    std::cout << (error == PrintError::NoPaper) << std::endl;

    printer.pagesLoaded = 1;
    error = printPage(printer);
    std::cout << (error == PrintError::None) << std::endl;
    std::cout << printer.pagesLoaded << std::endl;
}
```

<details>
<summary>Ответ</summary>

Выведутся `1`, `1`, `1` и `0`.
Принтер теперь хранит и количество загруженных листов. Успешная печать расходует один лист; неудачный запрос не меняет состояние принтера.

Сначала есть обе проблемы, но проверка застрявшей бумаги сразу завершает функцию, поэтому возвращается `Jammed`.
После устранения этой проблемы обнаруживается `NoPaper`. Если загрузить лист, последний запрос выполнится успешно, а `pagesLoaded` уменьшится с `1` до `0`.
Передача принтера по ссылке позволяет функции менять тот же объект принтера.
</details>

### 5. Bool и выходной параметр-указатель

```cpp
#include <iostream>

bool divideExactly(int dividend, int divisor, int* quotient)
{
    if (dividend < 0 || divisor <= 0)
    {
        return false;
    }
    if (dividend % divisor != 0)
    {
        return false;
    }
    *quotient = dividend / divisor;
    return true;
}

int main()
{
    int quotient = 99;
    bool success = divideExactly(8, 2, &quotient);
    std::cout << success << std::endl;
    std::cout << quotient << std::endl;

    success = divideExactly(9, 2, &quotient);
    std::cout << success << std::endl;
    std::cout << quotient << std::endl;
}
```

<details>
<summary>Ответ</summary>

Выведутся `1`, `4`, `0` и `4`.
Функция принимает неотрицательное делимое и положительный делитель и завершается успешно только при делении без остатка.
`8 / 2` — ровно `4`. При `9 / 2` целочисленное деление отбросило бы дробную часть, поэтому проверка остатка отклоняет такой случай.

Bool сообщает об успехе, а частное записывается через параметр-указатель.
При ошибке присваивания нет: последнее `4` — предыдущий результат, а не результат для `9 / 2`.
`quotient` должен указывать на существующий объект типа `int`.
</details>

### 6. Тот же выходной параметр через ссылку

```cpp
#include <iostream>

bool divideExactly(int dividend, int divisor, int& quotient)
{
    if (dividend < 0 || divisor <= 0)
    {
        return false;
    }
    if (dividend % divisor != 0)
    {
        return false;
    }
    quotient = dividend / divisor;
    return true;
}

int main()
{
    int quotient = 99;
    bool success = divideExactly(8, 2, quotient);
    std::cout << success << std::endl;
    std::cout << quotient << std::endl;

    success = divideExactly(9, 2, quotient);
    std::cout << success << std::endl;
    std::cout << quotient << std::endl;
}
```

<details>
<summary>Ответ</summary>

Выведутся те же `1`, `4`, `0` и `4`.
Параметр-ссылка ссылается на переменную в вызывающей функции, поэтому присваивание в `quotient` меняет эту переменную.
Передаётся сама переменная, а не её адрес.
Правило деления без остатка и обещание не менять выходное значение при ошибке остаются прежними.
</details>

### 7. Игнорирование признака успеха

```cpp
#include <iostream>

struct TemperatureSensor
{
    bool connected;
    int temperature;
};

bool readTemperature(const TemperatureSensor& sensor, int& temperature)
{
    if (!sensor.connected)
    {
        return false;
    }
    temperature = sensor.temperature;
    return true;
}

int main()
{
    TemperatureSensor sensor{ false, 17 };
    int temperature = 21;
    readTemperature(sensor, temperature);
    std::cout << temperature << std::endl;
}
```

<details>
<summary>Ответ</summary>

Выведется `21`.
Отключённый датчик не может передать новое измерение, поэтому функция возвращает `false`, не меняя выходное значение.
Вызывающая функция игнорирует этот признак ошибки и выводит старую температуру.
`21` — инициализированное значение, но считать его новым измерением было бы логической ошибкой.
Используйте выходное значение как новое измерение только после проверки успеха вызова.
</details>

### 8. Enum и выходное значение

```cpp
#include <iostream>

struct Printer
{
    bool jammed;
    int pagesLoaded;
};

enum class PrintError
{
    None,
    Jammed,
    NoPaper,
};

PrintError printPage(Printer& printer, int& pagesRemaining)
{
    if (printer.jammed)
    {
        return PrintError::Jammed;
    }
    if (printer.pagesLoaded == 0)
    {
        return PrintError::NoPaper;
    }
    printer.pagesLoaded -= 1;
    pagesRemaining = printer.pagesLoaded;
    return PrintError::None;
}

int main()
{
    Printer printer{ false, 2 };
    int pagesRemaining = 99;
    PrintError error = printPage(printer, pagesRemaining);
    if (error == PrintError::None)
    {
        std::cout << pagesRemaining << std::endl;
    }

    printer.jammed = true;
    error = printPage(printer, pagesRemaining);
    if (error == PrintError::Jammed)
    {
        std::cout << "printer is jammed" << std::endl;
    }
}
```

<details>
<summary>Ответ</summary>

Выведутся `1` и `printer is jammed`.
Успешный запрос расходует один из двух загруженных листов и записывает оставшееся количество через параметр-ссылку.
Enum сообщает об успехе или конкретной причине ошибки.

Неудачный запрос не меняет ни принтер, ни `pagesRemaining`.
Старое количество не используется как новый результат: вместо этого вызывающая функция обрабатывает `Jammed`.
Здесь подробный признак ошибки объединяется с отдельным выходным значением.
</details>

### 9. Нулевой указатель означает ошибку

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

### 10. Возврат собственной структуры результата

```cpp
#include <iostream>

struct TicketMachine
{
    bool online;
    int nextTicket;
};

struct TicketResult
{
    bool success;
    int number;
};

TicketResult issueTicket(TicketMachine& machine)
{
    if (!machine.online)
    {
        return { false, 0 };
    }
    int number = machine.nextTicket;
    machine.nextTicket += 1;
    return { true, number };
}

int main()
{
    TicketMachine machine{ true, 42 };
    TicketResult result = issueTicket(machine);
    if (result.success)
    {
        std::cout << result.number << std::endl;
    }

    machine.online = false;
    result = issueTicket(machine);
    if (result.success)
    {
        std::cout << result.number << std::endl;
    }
    else
    {
        std::cout << "machine is offline" << std::endl;
    }
}
```

<details>
<summary>Ответ</summary>

Выведутся `42` и `machine is offline`.
Работающий автомат выдаёт следующий номер талона и увеличивает свой счётчик.
Когда автомат отключён, он не может выдать талон и не меняет счётчик.

Структура возвращает признак успеха и номер талона вместе, без выходного параметра.
При ошибке `number` инициализируется нулём, но это не номер выданного талона.
Это собственная структура optional из [лабораторной по optional](16_optional.md), применённая к операции, которая может завершиться ошибкой.
Если интерфейсу нужна конкретная причина ошибки, поле с признаком успеха можно заменить на enum.
</details>

### 11. Возврат std::optional

```cpp
#include <iostream>
#include <optional>

struct TicketMachine
{
    bool online;
    int nextTicket;
};

std::optional<int> issueTicket(TicketMachine& machine)
{
    if (!machine.online)
    {
        return std::nullopt;
    }
    int number = machine.nextTicket;
    machine.nextTicket += 1;
    return number;
}

int main()
{
    TicketMachine machine{ true, 42 };
    std::optional<int> result = issueTicket(machine);
    if (result.has_value())
    {
        std::cout << *result << std::endl;
    }

    machine.online = false;
    result = issueTicket(machine);
    if (result.has_value())
    {
        std::cout << *result << std::endl;
    }
    else
    {
        std::cout << "machine is offline" << std::endl;
    }
}
```

<details>
<summary>Ответ</summary>

Выведутся те же `42` и `machine is offline`.
`std::optional<int>` обозначает либо номер выданного талона, либо его отсутствие.
`std::nullopt` задаёт пустое состояние, а перед разыменованием вызывающая функция проверяет `has_value()`.
Как и bool, само пустое состояние не объясняет причину ошибки.
</details>

### 12. Сбор нескольких ошибок

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

### 13. Повторное использование списка ошибок

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

### 14. Успешная проверка assert

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

### 15. Неуспешная проверка assert

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

### 16. Assert для проверки условия использования выходного параметра

```cpp
#include <iostream>
#include <cassert>

struct TemperatureSensor
{
    bool connected;
    int temperature;
};

bool readTemperature(const TemperatureSensor& sensor, int* temperature)
{
    assert(temperature != nullptr);
    if (!sensor.connected)
    {
        return false;
    }
    *temperature = sensor.temperature;
    return true;
}

int main()
{
    TemperatureSensor sensor{ false, 17 };
    int temperature = 21;
    bool success = readTemperature(sensor, &temperature);
    std::cout << success << std::endl;
    std::cout << temperature << std::endl;

    sensor.connected = true;
    success = readTemperature(sensor, &temperature);
    std::cout << success << std::endl;
    std::cout << temperature << std::endl;
}
```

<details>
<summary>Ответ</summary>

При включённых проверках assert выведутся `0`, `21`, `1` и `17`.
Этот интерфейс требует существующий выходной объект. Assert проверяет, что указатель не нулевой; оба вызова проходят эту проверку.
Передача `nullptr` нарушила бы условие использования функции.

Отключённый датчик — ожидаемая ошибка, о которой функция сообщает через `false`, поэтому программа может продолжить работу и снова подключить датчик.
После подключения датчик передаёт новое измерение `17`.
Даже при отключённых проверках assert вызывающая функция обязана передавать существующий выходной объект.
Assert и обычная обработка ошибок решают разные задачи.
</details>

### 17. Проверка успеха и ошибки через assert

```cpp
#include <iostream>
#include <cassert>

struct Printer
{
    bool jammed;
    int pagesLoaded;
};

bool printPage(Printer& printer)
{
    if (printer.jammed || printer.pagesLoaded == 0)
    {
        return false;
    }
    printer.pagesLoaded -= 1;
    return true;
}

int main()
{
    Printer printer{ true, 2 };
    bool printed = printPage(printer);
    assert(!printed);
    assert(printer.pagesLoaded == 2);

    printer.jammed = false;
    printed = printPage(printer);
    assert(printed);
    assert(printer.pagesLoaded == 1);
    std::cout << "tests passed" << std::endl;
}
```

<details>
<summary>Ответ</summary>

При включённых проверках assert выведется `tests passed`.
Первый запрос отклоняется из-за застрявшей бумаги; оба загруженных листа остаются.
После устранения этой проблемы второй запрос выполняется успешно и расходует один лист.
Проверки assert подтверждают признак успеха и получившееся состояние того же принтера.

Вызовы `printPage` вынесены из assert, поэтому они выполняются и при отключённых проверках.
Не помещайте необходимые действия только внутрь assert: его выражение может вообще не вычисляться.
При отключённых проверках само сообщение не доказывает, что результаты были проверены.
</details>

[Размеченным объединениям и флагам](32_tagged_unions_and_flags.md) и [исключениям](33_exceptions.md) посвящены отдельные лабораторные в конце курса.
