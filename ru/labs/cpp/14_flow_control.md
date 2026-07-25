# Flow control

## Концепты

- `if`
- `else`
- `else if`
- `while (true)`
- `continue`
- `break`
- `do ... while`

## Примеры на понимание

### 1. `true` в условии
```cpp
if (true)
{
   std::cout << "Hello" << std::endl;
}
```

<details>
<summary>Ответ</summary>

`true` в условии заставляет тело `if`-а выполняться всегда.
</details>

### 2. `false` в условии
```cpp
if (false)
{
   std::cout << "Hello" << std::endl;
}
```

<details>
<summary>Ответ</summary>

Этот код гарантировано никогда не выполнится.
</details>

### 3. `bool` переменная в условии
```cpp
bool execute = true;
if (execute)
{
   std::cout << "Hello" << std::endl;
}

bool notExecute = !execute;
if (notExecute)
{
   std::cout << "Not executed" << std::endl;
}
```

<details>
<summary>Ответ</summary>

При запуске, выведется только Hello.
</details>

### 4. Числа в условии
```cpp
if (1)
{
   std::cout << "1" << std::endl;
}
if (123)
{
   std::cout << "123" << std::endl;
}
if (0)
{
   std::cout << "0" << std::endl;
}
```

<details>
<summary>Ответ</summary>

В C++ `if` принимает любое выражение, приводимое к `bool`.
Данный код скомпилируется и выведет `1` и `123`.
</details>

### 5. Указатель в условии
```cpp
int* a { nullptr };
if (a)
{
   std::cout << "a is true" << std::endl;
}

int b {};
int* pb { &b };
if (pb)
{
   std::cout << "pb is true" << std::endl;
}
if (b)
{
   std::cout << "b is true" << std::endl;
}

bool c { false };
bool* pc { &c };
if (pc)
{
   std::cout << "pc is true" << std::endl;
}
```

<details>
<summary>Ответ</summary>

`if`, когда ему передают указатель, проверяет, если указатель не является нулевым (`nullptr`).
`a is true` тут не выведется, а `b is true` и `pc is true` выведется.

`if (b)` -> `if (0)` -> `if (false)`.
`b is true` не выведется.
</details>

### 6. Несколько инструкции в теле
```cpp
if (false)
{
   std::cout << "A" << std::endl;
   std::cout << "B" << std::endl;
}
```

<details>
<summary>Ответ</summary>

Ничего не напечатается.
</details>

### 7. Без фигурных скобок
```cpp
if (false)
   std::cout << "A" << std::endl;
   std::cout << "B" << std::endl;
```

<details>
<summary>Ответ</summary>

Напечатается только `B`, потому что лишь первая инструкция прикреплена к `if`.

Эквивалентный код:
```cpp
if (false)
{
   std::cout << "A" << std::endl;
}
std::cout << "B" << std::endl;
```
</details>

### 8. `else`
```cpp
if (false)
{
   std::cout << "A" << std::endl;
}
else
{
   std::cout << "B" << std::endl;
}
```

<details>
<summary>Ответ</summary>

Данный код выведет `B`, поскольку блок `else` выполняется тогда, когда не выполняется условие.
</details>

### 9. Перезапись переменной из условия в теле `if`
```cpp
bool a = true;
if (a)
{
   a = false;
}
else
{
   std::cout << "B" << std::endl;
}
```

<details>
<summary>Ответ</summary>

`B` не напечатается, потому что то, выполнится ли `else`, определяется на момент проверки `a` в `if`,
а это происходит до его изменения.
</details>

### 10. `return` в `if`
```cpp
void F()
{
   if (true)
   {
       return;
   }
   else
   {
       std::cout << "Else" << std::endl;
   }
   std::cout << "After Else" << std::endl;
}
```

<details>
<summary>Ответ</summary>

Здесь `Else` не напечатается.
То, выполнится ли блок `else`, зависит лишь от условия в `if`.

`return` полностью пропускает все последующие интсрукции. 
`After Else` тоже не напечатается.
</details>

### 11. Код после `else`
```cpp
if (true)
   std::cout << "A" << std::endl;
else
   std::cout << "B" << std::endl;
std::cout << "C" << std::endl;
```

<details>
<summary>Ответ</summary>

`B` не напечатается. Напечатаются `A` и `C`.
</details>

### 12. `if` без фигурных скобок, `else` — с
```cpp
if (true)
   std::cout << "A" << std::endl;
else
{
   std::cout << "B" << std::endl;
}
```

<details>
<summary>Ответ</summary>

Допустимо комбинировать прилепление инструкции и явный блок.
</details>

### 13. Цепочка `if`-`else`

Как обычно записывают данный код, используя цепочку `if`-`else`?
```cpp
if (a)
{
   std::cout << "A" << std::endl;
}
else
{
   if (b)
   {
       std::cout << "B" << std::endl;
   }
   else
   {
       if (c)
       {
           std::cout << "C" << std::endl;
       }
   }
}
```

<details>
<summary>Ответ</summary>

`if` обычно цепляют как инструкцию, сопровождающую `else`:

```cpp
if (a)
{
   std::cout << "A" << std::endl;
}
else if (b)
{
   std::cout << "B" << std::endl;
}
else if (c)
{
   std::cout << "C" << std::endl;
}
```
</details>

### 14. Early return 

Попытайтесь представить данный код как цепочку `if`-`else`, ему идентичную.
Как сделать этот код через early return / guard clause?

```cpp
if (a)
{
   std::cout << "A" << std::endl;
}
else
{
   std::cout << "After A" << std::endl;

   if (b)
   {
       std::cout << "B" << std::endl;
   }
   else
   {
       std::cout << "After B" << std::endl;

       if (c)
       {
           std::cout << "C" << std::endl;
       }
       else
       {
           std::cout << "After C" << std::endl;
       }
   }
}
```

<details>
<summary>Ответ (цепочка)</summary>

Этот код невозможно представить как цепочку.
Некуда поставить `After B` и `After C` так, чтобы они выполнялись по тем же правилам.
Можно попробовать их продублировать, но тогда они не будут семантически эквивалентны:

```cpp
if (a)
{
   std::cout << "A" << std::endl;
}
else if (b)
{
   std::cout << "After A" << std::endl;
   std::cout << "B" << std::endl;
}
else if (c)
{
   std::cout << "After A" << std::endl;
   std::cout << "After B" << std::endl;
   std::cout << "C" << std::endl;
}
else
{
   std::cout << "After A" << std::endl;
   std::cout << "After B" << std::endl;
   std::cout << "After C" << std::endl;
}
```
</details>

<details>
<summary>Ответ (guard clause / early return)</summary>

1. Создается функция для этого кусочка кода;
2. Внутри каждого `if` прописывается `return`;
3. `else` и блоки пропадают.

```cpp
#include <iostream>

void f(bool a, bool b, bool c)
{
   if (a)
   {
       std::cout << "A" << std::endl;
       return;
   }
   std::cout << "After A" << std::endl;

   if (b)
   {
       std::cout << "B" << std::endl;
       return;
   }
   std::cout << "After B" << std::endl;

   if (c)
   {
       std::cout << "C" << std::endl;
       return;
   }
   std::cout << "After C" << std::endl;
}

int main()
{
   // предполагается, что a, b, c были созданы ранее ...
   f(a, b, c);
}
```
</details>

<details>
<summary>Зачем этот guard clause / early return?</summary>

- Чтобы поднять обработку ошибок вверх функции, а основную логику опустить вниз.
 Это делает очевидным тот факт, что логика зависит от корректности данных,
 которая проверялась на момент обработки ошибок (контракт).
- Убирает лишнюю вложенность условий;
- Способствует локальности кода проверки ошибки и ее обработки.

Пример кода без применения guard clause / early return:
```cpp
void sendWelcomeEmail(User* user)
{
   // Условия перечислены с увеличением вложенности.
   if (user != nullptr)
   {
       if (user->IsActive)
       {
           if (user->EmailConfirmed)
           {
               // Код с самим действием спрятан в середине функции.
               std::cout << "Sending email to " << user->email << std::endl;
           }
           else
           {
               std::cout << "Email not confirmed." << std::endl;
           }
       }
       else
       {
           std::cout << "User is not active." << std::endl;
       }
   }
   // Не соблюдается локальность:
   // обработка удалена в исходном коде от связанной проверки.
   else
   {
       std::cout << "User not found." << std::endl;
   }
}
```

Тот же код, с его применением:
```cpp
void sendWelcomeEmail(User* user)
{
   // Можно блоком разграничить контракт 
   // (необходимые условия для выполнения основного действия), 
   // или вынести его в свою функцию.
   {
       // Соблюдена локальность: условия рядом с их обработкой.
       if (user == nullptr)
       {
           std::cout << "User not found." << std::endl;
           return;
       }
   
       if (!user->isActive)
       {
           std::cout << "User is not active." << std::endl;
           return;
       }
   
       if (!user->emailConfirmed)
       {
           std::cout << "Email not confirmed." << std::endl;
           return;
       }
   }

   // Основной код находится после всех проверок, а не в середине.
   std::cout << "Sending email to " << user->email << std::endl;
}
```
</details>

### 15. Сложный пример
```cpp
int i = 0;
while (true)
{
   if (i == 4)
   {
       std::cout << "ERROR: Should not happen" << std::endl;
       break;
   }
   if (i == 3)
   {
       std::cout << "Exit" << std::endl;
       break;
   }
   if (i == 0)
   {
       std::cout << "Increase by 2 on first iter" << std::endl;
       i += 2;
       continue;
   }

   std::cout << "Increase by 1 normally" << std::endl;
   i++;
}
```

<details>
<summary>Что делают <code>break</code> и <code>continue</code></summary>

`break` прекращает выполнение цикла (переходит на первую инструкцию после цикла).

`continue` переходит в начало цикла (дальнейшие инструкции из тела цикла не выполняются для этой итерации).
</details>

<details>
<summary>Ответ</summary>

"Increase by 2 on first iter" напечатается в первой итерации цикла, `i++` не выполнится из-за `continue`.

"Increase by 1 normally" напечатается во второй итерации цикла, 
после прохождения с неудачей всех проверок `if`-ов.

"Exit" напечатается в третьей итерации, тогда как проверка `i == 0` и инструкция `i++` не выполнится,
поскольку `break` прервет выполнение цикла.

```
Increase by 2 on first iter
Increase by 1 normally
Exit
```
</details>

### 16. `return` изнутри `while`
```cpp
int F()
{
   while (true)
   {
       if (true)
       {
           return 0;
       }
       break;
   }
   return 1;
}
```

<details>
<summary>Ответ</summary>

Функция вернет `0`. `break` и `return 1` не выполнятся.
</details>

### 17. Пример использования `if`
```cpp
#include <iostream>
#include <cassert>

struct Result
{
   bool isDenominatorZero;
   // Should only be read if there is no error.
   int result;
};

Result ceilingDivide(int numerator, int denominator)
{
   if (denominator == 0)
   {
       return {
           .isDenominatorZero = true,
           .result = 0,
       };
   }

   int value = (numerator + denominator - 1) / denominator;
   return {
       .isDenominatorZero = false,
       .result = value,
   };
}

int main()
{
   {
       int totalStudents { 25 };
       int studentsPerTable { 2 };
       Result result { ceilingDivide(totalStudents, studentsPerTable) };
       if (!result.isDenominatorZero)
       {
           int numTablesNeeded = result.result;
           std::cout << "Number of tables needed is " << numTablesNeeded << std::endl;
       }
       else
       {
           std::cout << "Can't seat any students if no students are seated per table" << std::endl;
           assert(studentsPerTable == 0);
       }
   }
   {
       Result result { ceilingDivide(30, 0) };
       if (result.isDenominatorZero)
       {
           std::cout << "Could not divide" << std::endl;
       }
       else
       {
           std::cout << "The result is " << result.result << std::endl;
       }
   }
}
```

## Рефакторинг

Зарефакторьте этот код, используя guard clause / early return.

```cpp
#include <iostream>

int main()
{
    int number = 10;

    if (number == 5)
    {
        std::cout << "The number is 5" << std::endl;
    }
    else
    {
        std::cout << "The number is not 5" << std::endl;

        if (number % 2 == 1)
        {
            std::cout << "The number is not divisible by 2" << std::endl;
        }
        else
        {
            std::cout << "The number is divisible by 2" << std::endl;

            if (number == 6)
            {
                std::cout << "The number is 6" << std::endl;
            }
        }
    }
}
```

## Сложное логическое выражение

Дан базовый код:

```cpp
#include <iostream>

int main()
{
    int apples;
    int pears;
    int oranges;

    std::cout << "Apples:";
    std::cin >> apples;

    std::cout << "Pears:";
    std::cin >> pears;

    std::cout << "Oranges:";
    std::cin >> oranges;

    // ...

    return 0;
}
```

- Если количество яблок больше 5, количество груш меньше 8
  и количество апельсинов ровно в 2 раза больше чем количество яблок,
  напечатайте на экран "Hello".

- Сделайте временную переменную с результатом выражения.
  Проверяйте ее в if.

- Сделайте по временной переменной для каждого из подусловий.
  Вычисляйте общее условие, используя эти подусловия.

- Объявите временные переменные подусловий в блоке,
  чтобы эти переменные не были видны за пределами блока.
  Используйте внешнее условие вне блока (блок существует для инициализации общего условия).

  Разрешается также из этого блока сделать функцию.

- Зарефакторьте 3 переменные с количеством фруктов в одну структуру (`FruitCounts`)
  с 3 полями, по одному для каждого типа фруктов.
  Переделайте код, чтобы везде использовалась эта структура.
