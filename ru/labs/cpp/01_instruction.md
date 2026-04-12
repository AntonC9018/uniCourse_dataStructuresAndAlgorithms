# Базовый синтаксис: инструкции

- [Видео про инструкции](https://www.youtube.com/watch?v=Z8AFpeE7hOo&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=5)

## Концепты

- Исходный файл
- Компилирование и запуск программы
- Инструкции программы
- Порядок выполнения инструкций
- Инструкция печати в консоль
- Функции без параметров
- Особая функция `main`
- Тело функции
- Пустая функция
- Комментарии
- Порядок определения инструкции программы

## Задачи на анализ

Что произойдет при компилировании этих отрезков кода? А при выполнении?

### 1. Пустой `main`

```cpp
int main()
{
}
```

<!-- Ничего, main, int, 1, ошибка компиляции, ошибка при выполнении -->

<details>
<summary>Ответ</summary>

Эта программа успешно скомпилируется.

Функция `main` автоматически запустится при запуске этой программы.

Сама функция не содержит инструкций в теле (пустые фигурные скобки).
По этой причине, при выполнении `main` ничего не будет напечатано.
</details>

### 2. Печать строки
```cpp
int main()
{
    std::cout << "Hello world";
    std::cout << std::endl;
}
```

<details>
<summary>Интуиция для <code>std::cout &lt;&lt;</code></summary>

`std` — это сокращение для *standard*. 
Можете запомнить, что `std::` указывает, что функция из стандартной библиотеки.

Слово `cout` состоит из 
- `c` обозначает слово "console", консоль;
- `out` это сокращение для "output", как вывод в консоль.

`<<` как бы **запихивает** следующую за собой строку в `std::cout`.
</details>

<details>
<summary>Ответ</summary>

Эта программа не скомпилируется.
Произойдет ошибка компиляции по той причине, 
что нет строки `#include <iostream>` перед `int main()` 
(не включен хедер `<iostream>`).
Без этой строки, компилятор не знает о существовании инструкции печати.
</details>

### 3. Исправленный код печати строки
```cpp
#include <iostream>

int main()
{
    std::cout << "Hello world";
    std::cout << std::endl;
}
```

<details>
<summary>Ответ</summary>

Эта программа скомпилируется.
При запуске выполнятся инструкции из функции `main`,
печатая "Hello world".
</details>

### 4. Печать на той же строке
```cpp
#include <iostream>

int main()
{
    std::cout << "Hello world" << std::endl;
}
```

<details>
<summary>Ответ</summary>

Этот код эквивалентен следующему:
```cpp
std::cout << "Hello world";
std::cout << std::endl;
```
</details>

### 5. Пустая функция `A`
```cpp
void A()
{
}
```

<!-- Ничего, A, void, 0, ошибка компиляции, ошибка при выполнении -->

<details>
<summary>Ответ</summary>

Программа ожидает, что существует функция `main` для удачной компиляции.
Поскольку `main` нет, программа не скомпилируется 
(дав ошибку на фазе линкинга, о чем будет подробнее в одном из дальнейших уроков).

```
(.text+0x1b): undefined reference to `main'
collect2: error: ld returned 1 exit status
```

`ld` это название программы линкера.
</details>

### 6. Функция `A`
```cpp
void A()
{
    std::cout << "Hello World." << std::endl;
}
```

<!-- Ничего, A, void, 0, Hello World, ошибка компиляции, ошибка при выполнении -->

<details>
<summary>Ответ</summary>

Произойдет ошибка компиляции по той причине, что не включен хедер `<iostream>`
(нет строки `#include <iostream>`).
Компилятор не знает о существовании инструкции печати.

```
test.cpp: In function ‘void A()’:
test.cpp:3:10: error: ‘cout’ is not a member of ‘std’
    3 |     std::cout << "Hello World";
      |          ^~~~
test.cpp:1:1: note: ‘std::cout’ is defined in header ‘<iostream>’; did you forget to ‘#include <iostream>’?
  +++ |+#include <iostream>
    1 | void A()
```

Чтобы решить, нужно добавить `#include <iostream>` как первую строку.
</details>

### 7. Исправленная функция `A`
```cpp
#include <iostream>

void A()
{
    std::cout << "Hello World." << std::endl;
}
```

<!-- Ничего, A, void, 0, Hello World, ошибка компиляции, ошибка при выполнении -->

<details>
<summary>Ответ</summary>

Произойдет ошибка компиляции, потому что нет функции `main`. [см. 1](#1-пустой-main)
</details>

### 8. Функция `main`
```cpp
#include <iostream>

int main()
{
    std::cout << "Hello World." << std::endl;
}
```

<!-- Ничего, A, void, 0, Hello World, ошибка компиляции, ошибка при выполнении -->

<details>
<summary>Ответ</summary>

Программа успешно скомпилируется:
- функция `main` определена;
- до использования `std::cout <<` была включена `iostream`.

При запуске напечатается "Hello World.".
</details>

### 9. Функция `Main`
```cpp
#include <iostream>

int Main()
{
    std::cout << "Hello World." << std::endl;
}
```

<!-- Ничего, A, void, 0, Hello World, ошибка компиляции, ошибка при выполнении -->

<details>
<summary>Ответ</summary>

C++ чувствителен к заглавности букв в именах функций и в именах других сущностей.
Функции `main` нет, как и [во втором вопросе](#5-пустая-функция-A).
</details>

### 10. Коммент
```cpp
#include <iostream>

int main()
{
    // std::cout << "Hello" << std::endl;
    std::cout << "World" << std::endl;
}
```

<details>
<summary>Ответ</summary>

Напечатается лишь World.
Строка с печатью Hello "откомменчена" (`//` в начале) и не выполнится.
</details>

### 11. Коммент всего
```cpp
int main()
{
    // std::cout << "Hello" << std::endl;
    // std::cout << "World" << std::endl;
}
```

<details>
<summary>Ответ</summary>

Скомпилируется без проблем.
Комментарии не участвуют в компиляции, следовательно, 
компилятор даже не будет искать функцию `std::cout <<`.

При запуске ничего не выведется.
</details>

### 12. Функция вызывает функцию
```cpp
#include <iostream>

void A()
{
    std::cout << "Hello World" << std::endl;
}
void B()
{
    A();
}
```

<details>
<summary>Ответ</summary>

Программа не скомпилируется, потому что функции `main` нет.
</details>

### 13. `main` вызывает функцию вызывает функцию
```cpp
#include <iostream>

void A()
{
    std::cout << "A" << std::endl;
}
void B()
{
    std::cout << "B-before" << std::endl;
    A();
    std::cout << "B-after" << std::endl;
}
int main()
{
    B();
}
```

<details>
<summary>Ответ</summary>

Программа скомпилируется с успехом.

Порядок выполнения строк:
```
B(); // функцию вызвали
std::cout << "B-before" << std::endl;
A(); // функцию вызвали
std::cout << "A" << std::endl;
// A завершилась
std::cout << "B-after" << std::endl;
// B завершилась
```
</details>

### 14. Почти та же ситуация
Выявите, в чем отличие этого примера и предыдущего.
Что изменилось, и изменится ли от этого исход?

```cpp
#include <iostream>

void B()
{
    std::cout << "B-before" << std::endl;
    A();
    std::cout << "B-after" << std::endl;
}
void A()
{
    std::cout << "A" << std::endl;
}
int main()
{
    B();
}
```

<details>
<summary>Ответ</summary>

Теперь программа не скомпилируется.
`A();` в функции `B` находится **в файле с кодом до определения функции `A`**.

Вызов `B();` в функции `main` не вызовет таких проблем, потому что 
**определение функции `B` находится в файле до ее вызова**.

`A` должна быть определена в исходном файле до того, как ее вызывает `B`.
</details>

## Практика

- Сделайте программу, которая печатает `"Jello"` в консоль.

- *Определите* функцию `A` которая печатает `A`. Вызовите ее в функции `main`.
  <details>
  <summary>Подсказка</summary>

  Определение функции подразумевает следующий синтаксис.

  ```cpp
  void A()
  {
  }
  ```

  Вызов функции выглядит вот так:
  ```cpp
  A();
  ```

  Определение функции должно находится до вызова функции.
  Следующий код не сработает:

  ```cpp
  int main()
  {
      A()
  }
  void A()
  {
  }
  ```

  Правильный код:

  ```cpp
  void A()
  {
      std::cout << "A";
      std::cout << std::endl;
  }
  int main()
  {
      A()
  }
  ```
  </details>

- Определите 3 функции: `A`, `B`, `C`.
  `A` должна вызывать функции `B` и `C`.
  `A`, `B`, `C` все должны печатать сообщение,
  что они вызываются (то есть, для `A`, будет `"called A"`)

