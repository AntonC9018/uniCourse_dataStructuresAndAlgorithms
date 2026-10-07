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
    {
        Printer printer{ true };
        bool printed = printPage(printer);
        std::cout << printed << std::endl;
    }
    {
        Printer printer{ false };
        bool printed = printPage(printer);
        std::cout << printed << std::endl;
    }
}
```

<details>
<summary>Ответ</summary>

Выведутся `0`, `page printed` и `1`.
`Printer` моделирует принтер, а `jammed` показывает, застряла ли в нём бумага.
В первом блоке запрос не выполняется из-за застрявшей бумаги. Во втором блоке создаётся принтер без этой проблемы,
поэтому страница печатается успешно.

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
В `std::cerr` часть `err` означает *error*, то есть «ошибка». Это поток для диагностических сообщений; здесь он
используется так же, как `std::cout`.

Сообщение объясняет человеку, что произошло, но вызывающая функция получает только `false`: конкретная причина ошибки в
возвращаемом значении теряется.
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
    if (grade > 10)
    {
        return GradeError::TooHigh;
    }
    return GradeError::None;
}

void printGradeError(GradeError error)
{
    switch (error)
    {
    case GradeError::None:
        std::cout << "valid grade" << std::endl;
        break;
    case GradeError::TooLow:
        std::cout << "grade too low" << std::endl;
        break;
    case GradeError::TooHigh:
        std::cout << "grade too high" << std::endl;
        break;
    }
}

int main()
{
    printGradeError(validateGrade(0));
    printGradeError(validateGrade(11));
    printGradeError(validateGrade(10));
    printGradeError(validateGrade(5));
}
```

<details>
<summary>Ответ</summary>

Выведутся `grade too low`, `grade too high`, `valid grade` и `valid grade`.
Этот интерфейс принимает целочисленные оценки от `1` до `10` включительно.
Один параметр проверяется по двум условиям: `0` слишком мало, `11` слишком много, а `10` и `5` допустимы.
Enum передаёт причину ошибки вызывающей функции. Вспомогательная функция выводит понятное сообщение для каждого
результата проверки.
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

void printPrinterError(PrintError error)
{
    switch (error)
    {
    case PrintError::None:
        std::cout << "page printed" << std::endl;
        break;
    case PrintError::Jammed:
        std::cout << "printer is jammed" << std::endl;
        break;
    case PrintError::NoPaper:
        std::cout << "no paper" << std::endl;
        break;
    }
}

int main()
{
    {
        Printer printer{ true, 0 };
        PrintError error = printPage(printer);
        printPrinterError(error);
    }
    {
        Printer printer{ false, 0 };
        PrintError error = printPage(printer);
        printPrinterError(error);
    }
    {
        Printer printer{ false, 1 };
        PrintError error = printPage(printer);
        printPrinterError(error);
        std::cout << printer.pagesLoaded << std::endl;
    }
}
```

<details>
<summary>Ответ</summary>

Выведутся `printer is jammed`, `no paper`, `page printed` и `0`.
В каждом блоке создаётся принтер для отдельного случая. Успешная печать расходует один лист; неудачный запрос не меняет
состояние этого принтера.

В первом случае есть обе проблемы, но проверка застрявшей бумаги сразу завершает функцию, поэтому возвращается `Jammed`.
Во втором принтере бумага не застряла, но листов нет, поэтому возвращается `NoPaper`.
В третьем принтере есть один лист: печать выполняется успешно, и `pagesLoaded` уменьшается с `1` до `0`.
Вспомогательная функция выводит сообщение для каждого значения enum. При этом вызывающая функция по-прежнему получает
результат печати в виде enum.
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
    {
        int quotient = 99;
        bool success = divideExactly(8, 2, &quotient);
        std::cout << success << std::endl;
        std::cout << quotient << std::endl;
    }
    {
        int quotient = 99;
        bool success = divideExactly(9, 2, &quotient);
        std::cout << success << std::endl;
        std::cout << quotient << std::endl;
    }
}
```

<details>
<summary>Ответ</summary>

Выведутся `1`, `4`, `0` и `99`.
Функция принимает неотрицательное делимое и положительный делитель и завершается успешно только при делении без остатка.
`8 / 2` — ровно `4`. При `9 / 2` целочисленное деление отбросило бы дробную часть, поэтому проверка остатка отклоняет
такой случай.

У каждого блока свои переменные для частного и признака успеха.
Bool сообщает об успехе, а частное записывается через параметр-указатель.
При ошибке присваивания нет: частное во втором блоке остаётся равным `99`, а не становится результатом для `9 / 2`.
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
    {
        int quotient = 99;
        bool success = divideExactly(8, 2, quotient);
        std::cout << success << std::endl;
        std::cout << quotient << std::endl;
    }
    {
        int quotient = 99;
        bool success = divideExactly(9, 2, quotient);
        std::cout << success << std::endl;
        std::cout << quotient << std::endl;
    }
}
```

<details>
<summary>Ответ</summary>

Выведутся те же `1`, `4`, `0` и `99`.
Параметр-ссылка ссылается на переменную в вызывающей функции, поэтому присваивание в `quotient` меняет эту переменную.
Передаётся сама переменная, а не её адрес.
Правило деления без остатка и обещание не менять выходное значение при ошибке остаются прежними.
В каждом блоке создаётся новое частное, инициализированное значением `99`.
</details>

### 7. Выходная переменная без начального значения

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
    {
        int quotient;
        bool success = divideExactly(8, 2, quotient);
        if (success)
        {
            std::cout << quotient << std::endl;
        }
    }
    {
        int quotient;
        bool success = divideExactly(9, 2, quotient);
        if (success)
        {
            std::cout << quotient << std::endl;
        }
        else
        {
            std::cout << "not exact" << std::endl;
        }
    }
}
```

<details>
<summary>Ответ</summary>

Выведутся `4` и `not exact`.
Обе переменные `quotient` объявлены без начального значения.
При успешном вызове функция записывает `4` через ссылку до того, как вызывающая функция читает значение.
При неудачном вызове функция ничего не записывает, и вызывающая функция не читает это частное.

Стандартный C++ разрешает такой код: объект типа `int` уже существует, а создание ссылки на него не читает его значение.
Запись через эту ссылку может задать его первое значение. То же относится к передаче его адреса через выходной
параметр-указатель.
В C++20 чтение этого неинициализированного числа до успешного присваивания было бы неопределённым поведением.
Если выходная переменная не инициализирована, проверять признак успеха особенно важно.
</details>

### 8. Игнорирование признака успеха

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
    [[maybe_unused]] bool success = readTemperature(sensor, temperature);
    std::cout << temperature << std::endl;
}
```

<details>
<summary>Ответ</summary>

Выведется `21`.
Отключённый датчик не может передать новое измерение, поэтому функция возвращает `false`, не меняя выходное значение.
Вызывающая функция сохраняет признак успеха в переменной с `[[maybe_unused]]` и намеренно не проверяет его.
Атрибут явно обозначает неиспользуемый результат, но не обрабатывает ошибку.

`21` — инициализированное значение, но считать его новым измерением было бы логической ошибкой.
Используйте выходное значение как новое измерение только после проверки успеха вызова.
</details>

### 9. Enum и выходное значение

```cpp
#include <iostream>

struct VendingMachine
{
    int bottles;
    int price;
};

enum class PurchaseError
{
    None,
    SoldOut,
    NotEnoughMoney,
};

PurchaseError buyWater(VendingMachine& machine, int money, int& change)
{
    if (machine.bottles == 0)
    {
        return PurchaseError::SoldOut;
    }
    if (money < machine.price)
    {
        return PurchaseError::NotEnoughMoney;
    }
    machine.bottles -= 1;
    change = money - machine.price;
    return PurchaseError::None;
}

int main()
{
    VendingMachine machine{ 1, 3 };
    {
        int change = 99;
        PurchaseError error = buyWater(machine, 2, change);
        if (error == PurchaseError::NotEnoughMoney)
        {
            std::cout << "not enough money" << std::endl;
        }
    }
    {
        int change = 99;
        PurchaseError error = buyWater(machine, 5, change);
        if (error == PurchaseError::None)
        {
            std::cout << change << std::endl;
        }
    }
    {
        int change = 99;
        PurchaseError error = buyWater(machine, 5, change);
        if (error == PurchaseError::SoldOut)
        {
            std::cout << "sold out" << std::endl;
        }
    }
}
```

<details>
<summary>Ответ</summary>

Выведутся `not enough money`, `2` и `sold out`.
В автомате одна бутылка по цене `3`. Первая оплата в размере `2` отклоняется, и бутылка остаётся в автомате.
Вторая оплата в размере `5` достаточна: бутылка продаётся, а в выходной параметр-ссылку записывается сдача, `5 - 3`.
Последняя покупка не выполняется, потому что автомат уже пуст.

Enum сообщает конкретную причину ошибки, а ссылка передаёт полезный результат при успехе.
У каждого вызова новые переменные для признака ошибки и сдачи. При неудаче сдача не меняется, и вызывающая функция не
использует её как результат.
Один автомат намеренно сохраняется между блоками, чтобы показать, как расходуется его запас.
</details>

### 10. Нулевой указатель означает ошибку

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

### 11. Возврат собственной структуры результата

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
    {
        TicketMachine machine{ true, 42 };
        TicketResult result = issueTicket(machine);
        if (result.success)
        {
            std::cout << result.number << std::endl;
        }
    }
    {
        TicketMachine machine{ false, 42 };
        TicketResult result = issueTicket(machine);
        if (result.success)
        {
            std::cout << result.number << std::endl;
        }
        else
        {
            std::cout << "machine is offline" << std::endl;
        }
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
Это собственная структура optional из [лабораторной по optional](16_optional.md), применённая к операции, которая может
завершиться ошибкой.
Если интерфейсу нужна конкретная причина ошибки, поле с признаком успеха можно заменить на enum.
</details>

### 12. Возврат std::optional

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
    {
        TicketMachine machine{ true, 42 };
        std::optional<int> result = issueTicket(machine);
        if (result.has_value())
        {
            std::cout << *result << std::endl;
        }
    }
    {
        TicketMachine machine{ false, 42 };
        std::optional<int> result = issueTicket(machine);
        if (result.has_value())
        {
            std::cout << *result << std::endl;
        }
        else
        {
            std::cout << "machine is offline" << std::endl;
        }
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

### 13. Сбор нескольких ошибок

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
`std::vector<ValidationError>` хранит список кодов ошибок; `push_back` добавляет одно значение в конец, а `size()` даёт
текущее количество значений.
Вектор передаётся по ссылке, поэтому функция добавляет ошибки в список вызывающей функции.

В отличие от предыдущего примера с enum, ни одна ошибка не приводит к немедленному возврату.
Выполняются обе проверки: сначала записывается `NegativeAmount`, затем `NegativePrice`.
Возвращённый bool показывает, найдены ли ошибки именно в этом вызове.
</details>

### 14. Повторное использование списка ошибок

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
    {
        [[maybe_unused]] bool valid = validateOrder(-1, -2, errors);
    }
    {
        bool valid = validateOrder(3, 4, errors);
        std::cout << valid << std::endl;
        std::cout << errors.size() << std::endl;
    }
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

### 15. Успешная проверка assert

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

### 16. Неуспешная проверка assert

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

При включённых проверках assert условие оказывается ложным: выводится диагностическое сообщение, и программа завершается
вызовом `std::abort`.
`after assert` не выведется. Точный текст диагностического сообщения зависит от реализации.
Assert обнаруживает нарушение предположения; он не возвращает `false` и не даёт вызывающей функции выбрать обычную ветку
обработки ошибки.

Если при компиляции определён `NDEBUG`, assert ничего не проверяет и не вычисляет своё выражение.
Тогда программа выведет `after assert`.
Не используйте assert как единственную проверку ожидаемых ошибок во входных данных.
</details>

### 17. Assert для проверки условия использования выходного параметра

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
    {
        TemperatureSensor sensor{ false, 17 };
        int temperature = 21;
        bool success = readTemperature(sensor, &temperature);
        std::cout << success << std::endl;
        std::cout << temperature << std::endl;
    }
    {
        TemperatureSensor sensor{ true, 17 };
        int temperature = 21;
        bool success = readTemperature(sensor, &temperature);
        std::cout << success << std::endl;
        std::cout << temperature << std::endl;
    }
}
```

<details>
<summary>Ответ</summary>

При включённых проверках assert выведутся `0`, `21`, `1` и `17`.
Каждый блок представляет отдельный случай со своим датчиком, выходной переменной и признаком успеха.
Этот интерфейс требует существующий выходной объект. Assert проверяет, что указатель не нулевой; оба вызова проходят эту
проверку.
Передача `nullptr` нарушила бы условие использования функции.

Отключённый датчик — ожидаемая ошибка, о которой функция сообщает через `false`, поэтому программа может продолжить
работу.
Подключённый датчик во втором блоке передаёт измерение `17`.
Даже при отключённых проверках assert вызывающая функция обязана передавать существующий выходной объект.
Assert и обычная обработка ошибок решают разные задачи.
</details>

### 18. Проверка успеха и ошибки через assert

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
    {
        Printer printer{ true, 2 };
        bool printed = printPage(printer);
        assert(!printed);
        assert(printer.pagesLoaded == 2);
    }
    {
        Printer printer{ false, 2 };
        bool printed = printPage(printer);
        assert(printed);
        assert(printer.pagesLoaded == 1);
    }
    std::cout << "tests passed" << std::endl;
}
```

<details>
<summary>Ответ</summary>

При включённых проверках assert выведется `tests passed`.
Принтер в первом блоке отклоняет запрос из-за застрявшей бумаги; оба загруженных листа остаются.
В принтере второго блока бумага не застряла, поэтому печать выполняется успешно и расходует один лист.
Проверки assert подтверждают признак успеха и получившееся состояние в каждом независимом случае.

Вызовы `printPage` вынесены из assert, поэтому они выполняются и при отключённых проверках.
Не помещайте необходимые действия только внутрь assert: его выражение может вообще не вычисляться.
При отключённых проверках само сообщение не доказывает, что результаты были проверены.
</details>

## Практические задания

Представьте каждую предметную область структурами и напишите процедурные функции. Решите, что получает каждая функция,
что она изменяет и как вызывающий код узнаёт, успешно ли она выполнилась. Используйте способы сообщения об ошибках из
этой лабораторной. Для первого задания приведено полное решение; для остальных готовых решений нет.

### 1. Торговый автомат

Торговый автомат продаёт воду за 3 монеты и сок за 5 монет. В нём изначально две бутылки воды и одна бутылка сока.
Покупатель выбирает товар по индексу и платит целое число монет. Сообщайте о неверном выборе, отрицательной сумме
оплаты, отсутствии товара и недостаточной оплате. Успешная покупка уменьшает запас на одну бутылку и возвращает сдачу
через параметр-ссылку. При неудачной покупке не изменяются ни запасы, ни выходная переменная.

<details>
<summary>Возможное решение</summary>

Структура `Money` представляет целое число монет. Используем её для цен товаров, оплаты и сдачи.
У каждого товара есть название, цена и количество в запасе. Автомат хранит массив товаров фиксированного размера.
Перечисление ошибок описывает результат операции; сдача передаётся отдельно и имеет смысл только при успешной покупке.

Проверяем выбор до обращения к массиву. Затем проверяем оплату и наличие товара. Только после всех проверок уменьшаем
запас и записываем сдачу. Цены должны быть положительными, а количества — неотрицательными: это предположения о
состоянии автомата, которые проверяются утверждениями `assert`.

```cpp
#include <array>
#include <cassert>
#include <cstddef>
#include <iostream>
#include <string_view>

struct Money
{
    int coins;
};

struct Product
{
    std::string_view name;
    Money price;
    int stock;
};

struct VendingMachine
{
    std::array<Product, 2> products;
};

enum class PurchaseError
{
    None,
    InvalidSelection,
    InvalidPayment,
    SoldOut,
    NotEnoughMoney,
};

PurchaseError buyProduct(
    VendingMachine& machine,
    std::size_t productIndex,
    Money payment,
    Money& change)
{
    if (productIndex >= machine.products.size())
    {
        return PurchaseError::InvalidSelection;
    }
    if (payment.coins < 0)
    {
        return PurchaseError::InvalidPayment;
    }

    Product& product = machine.products[productIndex];
    assert(product.price.coins > 0);
    assert(product.stock >= 0);
    if (product.stock == 0)
    {
        return PurchaseError::SoldOut;
    }
    if (payment.coins < product.price.coins)
    {
        return PurchaseError::NotEnoughMoney;
    }

    product.stock -= 1;
    change = Money{ payment.coins - product.price.coins };
    return PurchaseError::None;
}

int main()
{
    VendingMachine machine{
        std::array<Product, 2>{ Product{ "water", Money{ 3 }, 2 }, Product{ "juice", Money{ 5 }, 1 } }
    };
    {
        Money change{ 99 };
        PurchaseError error = buyProduct(machine, 1, Money{ 4 }, change);
        assert(error == PurchaseError::NotEnoughMoney);
        assert(machine.products[1].stock == 1);
        assert(change.coins == 99);
        std::cout << "not enough money" << std::endl;
    }
    {
        Money change;
        PurchaseError error = buyProduct(machine, 1, Money{ 7 }, change);
        assert(error == PurchaseError::None);
        if (error == PurchaseError::None)
        {
            std::cout << machine.products[1].name << ": change " << change.coins << std::endl;
        }
        assert(machine.products[1].stock == 0);
    }
    {
        Money change{ 99 };
        PurchaseError error = buyProduct(machine, 1, Money{ 7 }, change);
        assert(error == PurchaseError::SoldOut);
        assert(machine.products[1].stock == 0);
        assert(change.coins == 99);
        std::cout << "sold out" << std::endl;
    }
}
```

Программа печатает:

```text
not enough money
juice: change 2
sold out
```

Во всех трёх блоках используется один автомат, поэтому вторая покупка расходует запас сока. Для каждой попытки создаются
отдельные переменные статуса и результата. При неудаче выходная переменная сохраняет исходное значение, но это значение
не является сдачей от покупки. При успехе функция записывает результат до того, как вызывающий код его прочитает.

Утверждения проверяют результаты операций и изменения состояния. Вызовы `buyProduct` находятся вне `assert`, поэтому
отключение утверждений не отменяет покупки.

</details>

### 2. Выдача книг в библиотеке

В небольшой библиотеке есть буфер книг фиксированного размера, по одному экземпляру каждой книги. У каждого читателя
есть буфер идентификаторов взятых книг фиксированного размера и количество занятых элементов. Найдите книгу по
идентификатору, возвращая нулевой указатель, если её нет. Выдайте книгу читателю, переданному по указателю. Сообщайте об
отсутствии книги, о том, что она уже выдана, или о заполненном буфере читателя. При успешной выдаче обновляются и
доступность книги, и буфер читателя; при неудаче не изменяется ни то, ни другое. Выберите небольшие размеры буферов,
чтобы все случаи можно было проверить вручную.

### 3. Настраиваемая доставка посылок

Служба доставки получает посылку и конфигурацию с ограничениями на размеры и вес, поддерживаемыми направлениями, ценами
и сроками доставки. Проверьте посылку по переданной конфигурации и рассчитайте стоимость доставки. Верните структуру
результата со статусом, ценой и предполагаемым сроком доставки; поля расчёта имеют смысл только при успехе. Попробуйте
обработать одну посылку с двумя разными конфигурациями.

### 4. Бронирование билетов

В транспортном средстве есть массив мест фиксированного размера с ценами и информацией о том, какие места находятся у
окна. Поддержите три запроса: конкретное место, первое свободное место у окна или любое свободное место. Для последнего
варианта выбирайте первое свободное место; генерация случайных чисел не нужна. Получайте деньги покупателя по ссылке,
возвращайте перечисление ошибок и заполняйте структуру билета через параметр-указатель. Билет содержит выбранное место,
цену и оставшуюся сумму денег. При успехе забронируйте место и вычтите его цену. Сообщайте о неверном номере места,
занятом месте, отсутствии подходящего места и недостатке денег. При неудаче не изменяйте места, деньги и выходную
структуру билета.

### 5. Регистрация на экзамен

Студент хочет записаться на экзамен. Для каждого экзамена заданы необходимые предварительные дисциплины и ограниченное
число мест. Студент может не пройти несколько необходимых дисциплин, места могут закончиться, либо студент уже может
быть зарегистрирован. Соберите все обнаруженные проблемы в вектор ошибок, переданный по ссылке, указав каждую
недостающую дисциплину. Зарегистрируйте студента только при отсутствии проблем. Решите, очищает ли функция переданный
вектор или дописывает в него ошибки, и явно сформулируйте это условие для вызывающего кода.

### 6. Показания датчика

Датчик предоставляет буфер показаний температуры и допустимый диапазон. Отбрасывайте показания вне этого диапазона и
вычисляйте среднее оставшихся. Если допустимых показаний нет, возвращайте пустой `std::optional`; дайте вызывающему коду
возможность сообщить об отброшенных показаниях. Различайте ожидаемые неверные показания и предположения о входных данных
функции, которые следует проверять с помощью `assert`.

### 7. Обмен валют

У обменного пункта есть фиксированная таблица поддерживаемых валютных пар, курсов и комиссий. Клиент запрашивает обмен и
передаёт баланс в исходной валюте по ссылке. Верните перечисление ошибок и заполните структуру квитанции через
параметр-указатель. В квитанции укажите полученную сумму, использованный курс и размер комиссии. Сообщайте о
неподдерживаемой паре, неверной сумме и недостатке денег с учётом комиссии. При успехе вычтите из баланса обмениваемую
сумму и комиссию; при неудаче не изменяйте баланс и квитанцию. Выберите и опишите единицы денежных сумм и правило
округления.


[Размеченным объединениям и флагам](34_tagged_unions_and_flags.md) и [исключениям](35_exceptions.md) посвящены отдельные
лабораторные в конце курса.
