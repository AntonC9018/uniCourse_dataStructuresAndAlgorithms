# Лабораторная работа 4

Тема: `bool`, flow control.

Видео:
- [`bool`, flow control](https://www.youtube.com/watch?v=21m4VfonFnA&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=10)

## 4.1 bool

### Концепты

- Логические значения (`true`, `false`)
- Логические выражения
- Операторы сравнения чисел `>`, `<`, `>=`, `<=`, `==`, `!=`
- Логические операторы `&&`, `||`, `==`, `!`, `!=`
- Lazy evaluation операндов операторов `&&` и `||`
- Неявное преобразование в `bool` из `int` и указателей
- Макро `NULL`
- Особое значение `nullptr`

### Примеры на понимание

1. ```cpp
   bool a { true };
   std::cout << a << std::endl;
   ```
   
   <details>
   <summary>Ответ</summary>
 
   Тип `bool` принимает только два значения: `true` и `false`.  
   При выводе в консоль, напечатается `1` для `true` и `0` для `false`.
   </details>

2. ```cpp
   bool a { 0 };
   bool b { 1 };
   ```

   <details>
   <summary>Ответ</summary>
 
   Вместо `false` можно также сохранить `0`, а вместо `true` можно сохранить `1`.
   Это с успехом компилируется.
   </details>

3. ```cpp
   bool c { static_cast<bool>(123) };
   ```

   <details>
   <summary>Ответ</summary>
 
   `static_cast<bool>` для `int` дает `true`, если число не `0`, иначе `false`.
   В `c` будет `true`.
   </details>

3. ```cpp
   std::cout << sizeof(bool) << std::endl;
   ```

   <details>
   <summary>Ответ</summary>
 
   `bool` занимает 1 байт, несмотря на то, что для представления 2-х значений, 
   0 или 1, достаточно всего одного бита.
   Если хотите, сохранить несколько `bool` значений в отдельные биты
   в один и тот же байт, необходимо использовать побитовые маски.
   </details>

3. ```cpp
   bool a = 1 == 2;
   std::cout << a << std::endl;
   ```

   <details>
   <summary>Ответ</summary>
 
   Оператор `==` применяется к 2 выражениям и возвращает результат проверки на равенство, как логическое значение.
   Результат `false`.
   </details>

4. ```cpp
   int x = 3;
   int y = 4;
   bool b = x == y;
   std::cout << b << std::endl;
   ```

   <details>
   <summary>Ответ</summary>
 
   Здесь, оператор работает не с числами напрямую, а со значениями переменных.
   При выполнении, вместо `x` как бы вставится значение из `x` (как с выражениями), и так далее.
   </details>

4. ```cpp
   int x = 3;
   int y = 4;
   bool b = x == y;
   x = 4;
   std::cout << b << std::endl;
   ```

   <details>
   <summary>Ответ</summary>
 
   В `b` сохраняется не выражение `x == y`, а результат его вычисления (`false`).
   Последующее изменение `x` никак не воздействует на `b`.
   </details>
  
4. ```cpp
   int x = 3;
   int y = 4;
   bool b = x * 2 == y + 4;
   std::cout << b << std::endl;
   ```

   <details>
   <summary>Ответ</summary>
 
   Пример использования более сложных выражений как операнд.
 
   `bool b = x * 2 == y + 4` воспринимается как `bool b = ((x * 2) == (y + 4))`.
   Дальше вычисления происходят согласно правилам выражений.
   </details>

5. ```cpp
   bool a = 1 > 2;
   a = 3 == 3;
   std::cout << a << std::endl;
   ```

   <details>
   <summary>Ответ</summary>
 
   Здесь, `a` перезапишется с `false` на другое значение (`true`).
   </details>

6. ```cpp
   #include <iostream>

   void f(bool a)
   {
       std::cout << a << std::endl;
   }

   int main()
   {
       bool a = true;
       f(a);
   }
   ```

7. ```cpp
   #include <iostream>

   void f(bool flag)
   {
       std::cout << flag << std::endl;
   }

   int main()
   {
       f(5 > 3);
   }
   ```

   <details>
   <summary>Ответ</summary>
 
   Аргумент `5 > 3` вычисляется перед вызовом функции.  
   В `flag` попадет результат `true`.
   </details>

8. ```cpp
   #include <iostream>

   void f(bool b)
   {
       b = true;
   }

   int main()
   {
       int x { 1 };
       f(x == 2);
       std::cout << x << std::endl;
   }
   ```

   <details>
   <summary>Ответ</summary>
 
   При вызове `f` ей передается результат вычисления выражения `x == 2`.
   Изменение переменной параметра `b` никак не повлияет на `x`.

   Выведется `1`.
   </details>

8. ```cpp
   #include <iostream>

   bool f()
   {
       return true;
   }

   int main()
   {
       bool result = f();
       std::cout << result << std::endl;
   }
   ```

9. ```cpp

   #include <iostream>

   bool IsGreater(int a, int b)
   {
       return a > b;
   }

   int main()
   {
       bool result = IsGreater(5, 6);
       std::cout << result << std::endl;
   }
   ```

10. ```cpp
    bool a = true;
    bool b = false;
    bool c = a == b;
    std::cout << c << std::endl;
    ```
 
    <details>
    <summary>Ответ</summary>
  
    Оператор равенства `==` можно применять к выражениям типа `bool`.
    Сравнение `true == false` даёт `false`.
    </details>

1. ```cpp
   bool a = false;
   bool b = !a;
   std::cout << b << std::endl;
   ```

   <details>
   <summary>Ответ</summary>
  
   Оператор `!` делает из `false` `true` (и наоборот).
   </details>

2. ```cpp
   bool a = true;
   bool b = false;
   bool c = a && b;
   std::cout << c << std::endl;
   ```

   <details>
   <summary>Ответ</summary>

   `a && b` -> `true && false` -> `false`, потому что оба операнда должны быть `true`.
   </details>

3. ```cpp
   #include <iostream>

   bool A()
   {
       std::cout << "A" << std::endl;
       return true;
   }
    
   bool B()
   {
       std::cout << "B" << std::endl;
       return true;
   }

   int main()
   {
       bool result = A() && B();
   }
   ```

   <details>
   <summary>Ответ</summary>

   Для того, чтобы удостоверится, что `A()` и `B()` оба вернут `true`, программе необходимо их обоих вызвать.

   ```
   A
   B
   ```
   </details>

4. ```cpp
   #include <iostream>

   bool A()
   {
       std::cout << "A" << std::endl;
       return true;
   }
    
   bool B()
   {
       std::cout << "B" << std::endl;
       return false;
   }

   int main()
   {
       bool result = A() && B();
   }
   ```

   <details>
   <summary>Ответ</summary>
  
   Первая функция возвращает `true`, поэтому вторая тоже выполняется.  
   Вторая вернет `false`, и результат выражения будет `A() && B()` -> `true && false` -> `false`.

   ```
   A
   B
   ```
   </details>

5. ```cpp
   #include <iostream>

   bool A()
   {
       std::cout << "A" << std::endl;
       return false;
   }
    
   bool B()
   {
       std::cout << "B" << std::endl;
       return true;
   }

   int main()
   {
       bool result = A() && B();
   }
   ```

   <details>
   <summary>Ответ</summary>

   При `&&`, если первый операнд `false`, второй не вычисляется.  
   Это называется lazy evaluation (ленивое вычисление).

   ```
   A
   ```
   </details>

6. ```cpp
   #include <iostream>

   bool A()
   {
       std::cout << "A" << std::endl;
       return true;
   }
    
   bool B()
   {
       std::cout << "B" << std::endl;
       return true;
   }

   int main()
   {
       bool result = A() || B();
   }
   ```

   <details>
   <summary>Ответ</summary>

   При `||`, если первый операнд `true`, второй не вычисляется.  
   Это тоже ленивое вычисление.
    
   ```
   A
   ```
   </details>

6. ```cpp
   #include <iostream>

   void func(bool b, int* a)
   {
       std::cout << b << std::endl;
       *a = 2;
       std::cout << b << std::endl;
   }

   int main()
   {
       int a { 1 };
       func(a == 1, &a);
   }
   ```

   <details>
   <summary>Ответ</summary>

   В `func` передастся **результат вычисления выражения** `a == 1`,
   а также адрес `a`.

   Изменяя `a`, `func` не изменит и `b`, потому что информация о том,
   из какого выражения произошло значение для `b` теперь была потеряна.
   В `b` сохраняется только результат!
   </details>

## 4.2 flow control

### Концепты

- `if`
- `else`
- `else if`
- `while (true)`
- `continue`
- `break`
- `do ... while`

### Примеры на понимание

1. ```cpp
   if (true)
   {
       std::cout << "Hello" << std::endl;
   }
   ```

   <details>
   <summary>Ответ</summary>

   `true` в условии заставляет тело `if`-а выполняться всегда.
   </details>

1. ```cpp
   if (false)
   {
       std::cout << "Hello" << std::endl;
   }
   ```

   <details>
   <summary>Ответ</summary>

   Этот код гарантировано никогда не выполнится.
   </details>

1. ```cpp
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

1. ```cpp
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

1. ```cpp
   int* a { nullptr };
   if (a)
   {
       std::cout << "Hello" << std::endl;
   }

   int b {};
   int* pb { &b };
   if (pb)
   {
       std::cout << "World" << std::endl;
   }
   if (b)
   {
       std::cout << "b is true!" << std::endl;
   }
   ```

   <details>
   <summary>Ответ</summary>

   `if`, когда ему передают указатель, проверяет, если указатель не является нулевым (`nullptr`).
   `Hello` тут не выведется, а `World` выведется.

   `if (b)` -> `if (0)` -> `if (false)`.
   `b is true!` не выведется.
   </details>

1. ```cpp
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

1. ```cpp
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

1. ```cpp
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

1. ```cpp
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

1. ```cpp
   void F()
   {
       if (true)
       {
           return;
       }
       else
       {
           std::cout << "B" << std::endl;
       }
   }
   ```

   <details>
   <summary>Ответ</summary>

   Здесь `B` не напечатается.
   То, выполнится ли блок `else`, зависит лишь от условия в `if`.
   </details>

1. ```cpp
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

1. ```cpp
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

1. Как обычно записывают данный код, используя цепочку `if`-`else`?
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
   </details>

1. Попытайтесь представить данный код как цепочку `if`-`else`, ему идентичную.
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
   
1. ```cpp
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
   <summary>Ответ</summary>

   ```
   Increase by 2 on first iter
   Increase by 1 normally
   Exit
   ```
   </details>

1. ```cpp
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

1. ```cpp
   #include <iostream>

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
       }
       {
           Result result { ceilingDivide(30, 0) };
           std::cout << result.isDenominatorZero << std::endl;
           std::cout << result.result << std::endl;
       }
   }
   ```
   
### Рефакторинг

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

### Сложное логическое выражение

Дан базовый код:

```cpp
#include <iostream>

void main()
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
}
```

1. Если количество яблок больше 5, количество груш меньше 8
   и количество апельсинов ровно в 2 раза больше чем количество яблок,
   напечатайте на экран "Hello".

2. Сделайте временную переменную с результатом выражения.
   Проверяйте ее в if.

3. Сделайте по временной переменной для каждого из подусловий.
   Вычисляйте общее условие, используя эти подусловия.

4. Объявите временные переменные подусловий в блоке,
   чтобы эти переменные не были видны за пределами блока.
   Используйте внешнее условие вне блока (блок существует для инициализации общего условия).

   Разрешается так же из этого блока сделать функцию.

5. Зарефакторьте 3 переменные с количеством фруктов в одну структуру (`FruitCounts`)
   с 3 полями, по одному для каждого типа фруктов.
   Переделайте код, чтобы везде использовалась эта структура.


## 4.3

- Видео по [span](https://www.youtube.com/watch?v=3aXFuiHxb9k&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=11) (до строк)

### Алгоритм

- Сделайте функцию которая попарно перемножает числа из 2 массивов, записывая результат в 1-ый массив.

```cpp
void product(std::span<int> inputOutput, std::span<int> coefficients)
{
    // ...
}
```

- Убедитесь в ней в том, что спаны одинаковой длины, используя `assert`.

<details>
<summary>Как?</summary>

```cpp
assert(inputOutput.size() == coefficients.size());
```
</details>

- Реализуйте версию с бесконечным циклом, используя `break` вручную.

- Реализуйте версию с циклом `while` с условием.

- Реализуйте версию с циклом `for`.


### Примеры на понимание `span` 

1. ```cpp
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

1. ```cpp
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

1. ```cpp
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

1. ```cpp
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

1. ```cpp
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

1. ```cpp
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

1. В чем преимущество этого подхода по сравнению с предыдущим?
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

1. Как получить длину C-массива? А `std::array`?

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

1. В чем преимущества и недостатки этого подхода?
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


1. (продвинутый уровень)
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

1. (продвинутый уровень)
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

1. (продвинутый уровень)
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

1. ```cpp
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

1. ```cpp
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

1. ```cpp
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

1. (продвинутый уровень)
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

1. ```cpp
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

1. ```cpp
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

1. ```cpp
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
   </details>

1. ```cpp
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

1. ```cpp
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

1. Что будет, если сменить 
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

1. ```cpp
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

1. Что если в предыдущем примере выйти за рамки массива, например вот так:
   ```cpp
   std::span<int> s{ wholeSpan.subspan(2, 3) };
   ```

   <details>
   <summary>Ответ</summary>

   Тут не делается bounds-checking, это просто UB при считывании из позиции `2` в `s`

   > Создание некорректного `std::span` не считается UB, 
   > по аналогии с указателями, а вот считывание за пределами массива считается.
   </details>

1. Что выведется здесь?
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

1. Что выведется здесь?
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

1. ```cpp
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

1. ```cpp
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
