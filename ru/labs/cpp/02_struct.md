# 2. Структуры и функции

## 2.1 Структуры

Сопровождающее [видео](https://www.youtube.com/watch?v=9AhNOjjyAwU&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=8&t=2457).

Объяните словами что происходит в примере [`memory_example_2`](../../../en/05_programming_fundamentals/memory_example_2).
Можете скопировать файл с кодом и написать комментариями прямо в коде, что происходит.
Используйте excel таблицу из примера, чтобы визуализировать планировку памяти.

Можете в целом комментировать не каждый шаг, а что выведеться на каждом этапе, и почему 
(на что указывает в момент времени тот или иной указатель, что на данный момент записано в памяти, т.п.).
Можете также использовать дебаггер для лучшего понимания. 

## Примеры на понимание по структурам

Проанализируйте, что происходит в примерах:

1. ```cpp
   #include<iostream>

   struct A
   {
       int f1;
       int f2;
   };

   int main()
   {
       A a;
       a.f1 = 5;
       a.f2 = 6;

       A b;
       b = a;

       std::cout << a.f1 << std::endl;
       std::cout << a.f2 << std::endl;

       std::cout << b.f1 << std::endl;
       std::cout << b.f2 << std::endl;
   }
   ```

   <details>
   <summary>Ответ:</summary>

   `b = a` копирует значения *всех полей* `a` в `b`.
   </details>

2. ```cpp
   #include <iostream>

   struct A
   {
       int f1;
       int f2;
   };

   int main()
   {
       A a;
       a.f1 = 5;
       a.f2 = 6;
       A* pa = &a;
       A b = *pa;

       std::cout << b.f1 << std::endl;
       std::cout << b.f2 << std::endl;
   }
   ```
   <details>
   <summary>Ответ:</summary>

   На строчке `b = *pa`, `*pa` по сути эквивалентно прямому обращению к переменной `a`. Ситуация та же, что выше.
   </details>

3. ```cpp
   #include <iostream>

   struct A
   {
       int f1;
       int f2;
   };

   int main()
   {
       A a;
       a.f1 = 5;
       A* pa = &a;
       (*pa).f2 = 6;
       pa->f1 = 7;

       std::cout << a.f1 << std::endl;
       std::cout << a.f2 << std::endl;
   }
   ```
   <details>
   <summary>Ответ:</summary>

   `*pa` по сути эквивалентно обращению к `a` напрямую.

   `(*pa).f2 = 6` -> `a.f2 = 6`.

   `pa->f1` означает "перейди на переменную по адресу из `pa`, потом обратись к полю `f1`".
   Это по-другому можно выразить как `(*pa).f1`.
   И это будет по факту эквивалентно `a.f1`.
   </details>

4. ```cpp
   #include <iostream>

   struct A
   {
       int f1;
       int f2;
   };

   int main()
   {
       A a;
       std::cout << sizeof(a) << std::endl;
       std::cout << sizeof(A) << std::endl;
   }
   ```
   <details>
   <summary>Ответ:</summary>

   `sizeof(a)` дает размер переменной в байтах.
   `sizeof(A)` дает размер переменной типа `A` в байтах, если такую создать.
   Обе записи эквивалентны.

   Результат будет 8, потому что в каждой структуре по 2 `int`, каждый из которых занимает 4 байта.
   </details>


4. ```cpp
   #include <iostream>

   struct A
   {
       int f1[4];
       int* f2;
   };

   int main()
   {
       std::cout << sizeof(A) << std::endl;
   }
   ```

   <details>
   <summary>Ответ:</summary>

   - `int f1[4]` - это 4 `int`, каждый по 4 байта - 16 байт;
   - `int* f2` - 8 байтов на 64-битном процессоре.

   В сумме 24 байта.
   </details>

5. (продвинутый уровень):
   ```cpp
   #include <iostream>

   struct A
   {
       uint8_t f1;
       int f2;
       uint8_t f3;
   };

   int main()
   {
       std::cout << sizeof(A) << std::endl;
   }
   ```

   <details>
   <summary>Ответ:</summary>

   Тут в силу входит alignment.
   alignment делает так, что между полями остаются пустые места.

   Сначала, находится поле с наибольшем размером, до 8 байтов.
   В данном примере, это `int` - 4 байта.

   Теперь, делим память на окошки по 4 байта.
   Если последующее поле не влезает целиком в оставшееся окошко по 4 байта,
   оно попадает в следующее.

   - `uint8_t f1` попадет в первый байт первого окошка;
   - `int f2` не влезает в первое окошко после `f1`, поэтому попадет в следующее.
     Оставшиеся 3 байта первого окошка будут пустовать (padding bytes);
   - `uint8_t f3` попадет в третье окошко.

   В сумме .
   </details>

## 2.2 Функции

В данных примерах, сколько 

1. 

