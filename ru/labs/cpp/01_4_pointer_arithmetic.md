## 4. pointer arithmetic

1. ```cpp
   int arr[2]{};
   arr[0] = 1;
   arr[1] = 2;

   std::cout << arr[0];
   std::cout << std::endl;

   std::cout << arr[1];
   std::cout << std::endl;
   ```

   <details>

   <summary>

   Что значит `int arr[2]{}`?

   </summary>

   Типа группы из 2 переменных (массив), по умолчанию равным нулю (благодаря {}).
   </details>

   <details>
   <summary>Что такое массив?</summary>

   Массив это как бы несколько переменных в одной. 
   В данном случае, переменных как бы 2: `arr[0]` и `arr[1]`.

   Выражение "как бы" тут нарочно, потому что по факту `arr[0]` и `arr[1]` — это объекты,
   а не переменные, но это в другом уроке.
   </details>

   <details>
   <summary>Ответ</summary>

   `arr[0]` и `arr[1]` как бы эквивалентны именам переменных.
   То есть напечатается 1 и 2.
   </details>

2. ```cpp
   int arr1[2]{ 21, 32 };

   std::cout << arr1[0];
   std::cout << std::endl;

   std::cout << arr1[1];
   std::cout << std::endl;
   ```

   <details>
   <summary>Что значит этот синтаксис?</summary>

   Здесь элементы массива заданы при создании, в том же порядке (0, 1).
   </details>

3. ```cpp
   int arr1[3]{ 1, 2, 3 };
   int arr2[]{ 1, 2, 3, 4 };

   std::cout << sizeof(arr1);
   std::cout << std::endl;

   std::cout << sizeof(arr2);
   std::cout << std::endl;
   ```

   <details>

   <summary>

   Что такое `sizeof`?

   </summary>

   Это оператор, выполняющийся во время компиляции, который дает размер всего массива в байтах.
   В данном примере, в массиве `arr1` 3 инта, каждый по 4 байта, поэтому общий размер будет 12.
   </details>

   <details>

   <summary>

   Какой размер у `arr2`?

   </summary>

   У `arr2` не задан размер, он определится автоматически из элементов.
   </details>

   <details>

   <summary>

   Что значит `[]`?

   </summary>

   Это заменится во время компиляции на количество элементов справа 
   (то есть 4, в этом примере) в качестве длины.
   </details>

   <details>
   <summary>Ответ</summary>

   3 инта по 4 байта — это 12.

   4 инта по 4 байта — это 16.
   </details>

3. ```cpp
   int arr[3]{ 1, 2, 3 };
   size_t index { 2 };
   int it { arr[index] };
   std::cout << it;
   std::cout << std::endl;
   ```

   <details>
   <summary>Ответ</summary>

   Можно использовать "номер переменной" (индекс) 
   из другой переменной или выражения.

   Ответ будет 3.
   </details>

3. ```cpp
   int arr[3]{};
   size_t index { 2 };
   arr[index] = 5;
   std::cout << arr[2];
   std::cout << std::endl;
   ```

   <details>
   <summary>Ответ</summary>

   Запись по индексу тоже можно делать исходя из индекса,
   произошедшего из выражения.
   </details>

3. ```cpp
   int arr[3]{};
   size_t index { 1 };
   arr[index + 1] = 5;
   std::cout << arr[2];
   std::cout << std::endl;
   ```

   <details>
   <summary>Ответ</summary>

   Здесь демонстрируется использование более сложного выражения
   для получения индекса.
   </details>

3. ```cpp
   int arr[3]{ 0, 2, 1 };
   size_t index { 2 };
   int it { arr[index] };
   arr[index] = 5;
   std::cout << it;
   std::cout << std::endl;
   ```

   <details>
   <summary>Ответ</summary>

   В `it` на строчке `int it { arr[index] }` будет скопировано *значение `5`*,
   а не ссылка на элемент в массиве, поскольку тип `it` это `int`.
   Так как это просто `int`, изменяя переменную, из которой произошло его значение,
   после присваивания, не воздействует на `it`.
   </details>

3. ```cpp
   int a = 1;
   int b = 2;
   int* arr[]{ &a, &b };
   *arr[0] = 3;
   *arr[1] = *arr[0];

   std::cout << arr[0] << std::endl;
   std::cout << arr[1] << std::endl;

   std::cout << *arr[0] << std::endl;
   std::cout << *arr[1] << std::endl;
   ```

   <details>
   <summary>Ответ</summary>

   В массивах можно хранить данные, отличные от `int`.
   В данном примере, в массиве были сохранены указатели на `int` (`int*`).

   - `arr[0]` содержит адрес переменной `a`.
   - `arr[1]` содержит адрес переменной `b`.
   - `a`, эквивалентно `*arr[0]`, равно `3`.
   - `b`, эквивалентно `*arr[1]`, равно `3`.
   </details>

3. ```cpp
   int arr[2]{};
   int* p = arr;
   *arr = 1;

   std::cout << *p;
   std::cout << std::endl;

   std::cout << arr[0];
   std::cout << std::endl;

   std::cout << arr[1];
   std::cout << std::endl;
   ```

   <details>
   <summary>Ответ</summary>

   Когда `arr` используется в качестве выражения в `int* p = arr`,
   он деградирует (decays) в указатель на первый элемент из массива.
   `arr` тут эквивалентно `&arr[0]` или `&(arr[0])`.

   И `*p`, и `*arr`, и `arr[0]` ссылаются на ту же переменную.

   Выведется 1 дважды.
   </details>

4. ```cpp
   int a = 5;
   int* b{&a};
   ```

   <details>
   <summary>Ответ</summary>

   Это как с `int`, эквивалентно `int* b = &a`.
   </details>

4. ```cpp
   int arr[2]{};
   int* p = arr;
   p = p + 1;
   *p = 2;

   std::cout << arr[1];
   std::cout << std::endl;
   ```

   <details>
   <summary>Ответ</summary>

   `p + 1` перемещает указатель на 1 базовый элемент, то есть на 1 `int`, то есть на 4.

   `p` в конце функции равен `&arr[1]`.
   Считывание из `*p` эквивалетно считыванию из `arr[1]`.
   </details>

4. ```cpp
   int arr[2]{};
   int* p = arr;
   *(p + 1) = 6;

   std::cout << *p << std::endl;
   std::cout << arr[1] << std::endl;
   ```

   <details>
   <summary>Ответ</summary>

   С указателем, полученным из выражения, можно работать как и с указателем из обычной переменной.

   Еще важно заметить, что `*(p + 1)` *не изменяет `p`*, а создает *временный измененный адрес*.
   `*p` считает `0` из первой ячейки массива.
   </details>

4. ```cpp
   int arr[2]{};
   int* pStart = &arr[0];
   int* p = pStart + 1;

   ptrdiff_t x = p - pStart;
   std::cout << x;
   std::cout << std::endl;

   ptrdiff_t x1 = pStart - p;
   std::cout << x1;
   std::cout << std::endl;
   ```

   <details>
   <summary>Ответ</summary>

   Оператор `-` между указателями дает количество базовых элементов между ними.
   Результат может быть и отрицательным.

   Выведется 1, а потом -1.
   </details>
   
4. (продвинутый уровень):
   ```cpp
   #include <cstdint>
   #include <iostream>

   int main()
   {
       int arr[2]{};
       int* a = &arr[0];
       int* b = &arr[1];
       uintptr_t a1 = reinterpret_cast<uintptr_t>(a);
       uintptr_t b1 = reinterpret_cast<uintptr_t>(b);
       ptrdiff_t x = static_cast<ptrdiff_t>(b1 - a1);

       std::cout << x;
       std::cout << std::endl;
   }
   ```

   <details>
   <summary>Ответ</summary>

   `uintptr_t` это число, занимающее столько же байтов, сколько и `int*` (вероятно, 8 байтов).

   `b1 - a1` применяется между адресами как числами. 
   Это выражение уже не имеет информацию о том, какого типа указатели были вначале.
   Оно работает на числовых значениях указателя.

   Ответ будет 4 — разница указателей в байтах.
   </details>

4. (продвинутый уровень):
   ```cpp
   int a = 5;
   int b = 6;
   int* pa = &a;
   int* pb = pa + 1;

   std::cout << *pb;
   std::cout << std::endl;
   ```

   <details>
   <summary>Ответ</summary>

   Технически, это считается UB (undefined behavior).
   Но концептуально, выведется 6 из переменной `b`.
   </details>

4. (продвинутый уровень):
   ```cpp
   int a[2]{};
   int b = 6;
   int* p = &a[2];
   *p = 7;

   std::cout << b;
   std::cout << std::endl;
   ```

   <details>
   <summary>Ответ</summary>

   Технически это такая же ситуация, как и выше.
   Запомните, что выходя за пределы массива, 
   вы технически можете добраться до памяти другой переменной.
   Выход за пределы массива не является ошибкой в C
   и никак не ограничивается во время выполнения программы.

   Здесь выведется 7.
   </details>

1. ```cpp
   int arr1[2]{ 1, 2 };
   int arr2[2]{ 3, 4 };
   arr1 = arr2;
   ```
   <details>
   <summary>Ответ</summary>

   Несмотря на то, что логически это должно скопировать каждый элемент
   из `arr2` в `arr1`, программа не скомпилируется.
   Такой синтаксис просто не работает в C++.
   </details>

1. ```cpp
   int arr1[2]{ 1, 2 };
   int arr2[2]{ 3, 4 };
   *arr1 = *arr2;
   ```
   <details>
   <summary>Ответ</summary>

   В `*arr1 = *arr2`, имена массивов взяты как выражения.
   В этом случае, они воспринимаются как указатели на первый элемент.
   Соответственно, это перезапишет `arr1[0]` на `arr2[0]`, то есть `3`.
   </details>
