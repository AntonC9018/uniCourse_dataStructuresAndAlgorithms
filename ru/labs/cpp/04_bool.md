# Лабораторная работа 4

Тема: `bool`, flow control.

Видео:
- [`bool`, flow control](https://www.youtube.com/watch?v=21m4VfonFnA&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=10)
- [span](https://www.youtube.com/watch?v=3aXFuiHxb9k&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=11) (до строк)

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

   void f(bool x)
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
       bool a = true;
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

   void f()
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
       bool result = f();
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
       f(a == 1, &a);
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
   ```

   <details>
   <summary>Ответ</summary>

   `if`, когда ему передают указатель, проверяет, если указатель не является нулевым (`nullptr`).
   `Hello` тут не выведется, а `World` выведется.
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
   void sendWelcomeEmail(User user)
   {
       // Условия перечислены с увеличением вложенности.
       if (user != null)
       {
           if (user.IsActive)
           {
               if (user.EmailConfirmed)
               {
                   // Код с самим действием спрятан в середине функции.
                   Console.WriteLine($"Sending email to {user.Email}");
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
   void sendWelcomeEmail(User user)
   {
       // Можно блоком разграничить контракт 
       // (необходимые условия для выполнения основного действия), 
       // или вынести его в свою функцию.
       {
           // Соблюдена локальность: условия рядом с их обработкой.
           if (user == null)
           {
               std::cout << "User not found." << std::endl;
               return;
           }
       
           if (!user.isActive)
           {
               std::cout << "User is not active." << std::endl;
               return;
           }
       
           if (!user.emailConfirmed)
           {
               std::cout << "Email not confirmed." << std::endl;
               return;
           }
       }
   
       // Основной код находится после всех проверок, а не в середине.
       std::cout << "Sending email to " << user.email << std::endl;
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


### Циклы

- Сделайте функцию которая попарно перемножает числа из 2 массивов, записывая результат в 1-ый массив.

```
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
