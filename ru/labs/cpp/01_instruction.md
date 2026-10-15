---
slug: ru/cpp/labs/instruction
---
<!-- course-site-backlink:start -->
[Этот урок на сайте](https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms/ru/cpp/labs/instruction/)
<!-- course-site-backlink:end -->
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
<summary>С чего начинается программа</summary>

Программа начинает работу с функции `main`. Код внутри её фигурных скобок — это тело функции. Здесь оно пустое, поэтому печатать нечего.
</details>

<details>
<summary>Ответ</summary>

Успешно компилируется и ничего не печатает.
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
<summary>Печать текста</summary>

`std::cout <<` отправляет текст в консоль. Перед использованием добавьте `#include <iostream>` в начале файла. В этом примере этой строки нет.
</details>

<details>
<summary>Ответ</summary>

Не компилируется.
</details>

<details>
<summary>Откуда имя cout</summary>

`std` — сокращение от «standard»; `std::` указывает на имя из стандартной библиотеки. В `cout` буква `c` означает «console» (консоль), а `out` — «output» (вывод). Можно представлять, что `<<` отправляет следующее значение в `std::cout`.
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
<summary>Перевод строки</summary>

`std::cout` печатает текст, а `std::endl` завершает строку, как нажатие Enter. Здесь эти два действия выполняются по порядку внутри `main`.
</details>

<details>
<summary>Ответ</summary>

Компилируется и печатает `Hello world` с переводом строки.
</details>

<details>
<summary>Ещё о endl</summary>

`endl` — сокращение от «end line» (конец строки). Он также сразу отправляет на экран накопленный вывод.
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
<summary>Несколько операций вывода в одной инструкции</summary>

В одной инструкции можно записать несколько операций `<<`. Вывод идёт по порядку. Здесь это то же самое, что:
```cpp
std::cout << "Hello world";
std::cout << std::endl;
```
</details>

<details>
<summary>Ответ</summary>

Компилируется и печатает `Hello world` с переводом строки.
</details>

### 5. Пустая функция `A`
```cpp
void A()
{
}
```

<!-- Ничего, A, void, 0, ошибка компиляции, ошибка при выполнении -->

<details>
<summary>Программе нужна функция main</summary>

Определение `A` не указывает программе, с чего начать работу. Готовой программе нужна функция с именем `main`. Здесь определена только `A`.
</details>

<details>
<summary>Ответ</summary>

Не удаётся собрать готовую программу: нет `main`.
</details>

<details>
<summary>Если в ошибке упоминается ld</summary>

При сборке программы есть этап, который называется компоновкой. Именно на нём обнаруживается отсутствие `main`. `ld` — имя инструмента, который выполняет этот этап. Подробнее компоновка рассматривается позже.
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
<summary>Подключение iostream</summary>

Чтобы компилятор распознал `std::cout` и `std::endl`, перед ними нужно написать `#include <iostream>`. Здесь этой строки нет. После её добавления для готовой программы также понадобится `main`.
</details>

<details>
<summary>Ответ</summary>

Не компилируется.
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
<summary>Функция не запускается сама</summary>

Подключение `<iostream>` позволяет компилятору распознать код печати, но не запускает `A`. Программе по-прежнему нужна функция `main`, из которой можно вызвать `A`.
</details>

<details>
<summary>Ответ</summary>

Не удаётся собрать готовую программу: нет `main`.
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
<summary>Выполнение кода в main</summary>

Теперь `<iostream>` подключён и `main` определена. При запуске программы инструкция внутри `main` печатает текст и завершает строку.
</details>

<details>
<summary>Ответ</summary>

Компилируется и печатает `Hello World.` с переводом строки.
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
<summary>Заглавные и строчные буквы различаются</summary>

В C++ `Main` и `main` — разные имена. Программе нужна `main` со строчной `m`; определение `Main` её не заменяет.
</details>

<details>
<summary>Ответ</summary>

Не удаётся собрать готовую программу: нет `main`.
</details>

### 10. `COUT` вместо `cout`
```cpp
#include <iostream>

int main()
{
    std::COUT << "Hello World." << std::endl;
}
```

<!-- Ничего, A, void, 0, Hello World, ошибка компиляции, ошибка при выполнении -->

<details>
<summary>Имя нужно писать точно</summary>

Для печати используется имя `std::cout`, строчными буквами. `std::COUT` — другое имя, которое компилятор не распознаёт.
</details>

<details>
<summary>Ответ</summary>

Не компилируется.
</details>

### 11. Коммент
```cpp
#include <iostream>

int main()
{
    // std::cout << "Hello" << std::endl;
    std::cout << "World" << std::endl;
}
```

<details>
<summary>Комментарии игнорируются</summary>

`//` начинает комментарий до конца строки. Компилятор игнорирует этот текст. Здесь строка с печатью `Hello` закомментирована, поэтому выполняется только строка с печатью `World`.
</details>

<details>
<summary>Ответ</summary>

Печатает только `World` с переводом строки.
</details>

### 12. Коммент всего
```cpp
int main()
{
    // std::cout << "Hello" << std::endl;
    // std::cout << "World" << std::endl;
}
```

<details>
<summary>Закомментированный код не проверяется</summary>

Обе строки печати закомментированы. Компилятор видит пустую `main`, поэтому для этого кода не нужен `<iostream>`.
</details>

<details>
<summary>Ответ</summary>

Компилируется и ничего не печатает.
</details>

### 13. Функция вызывает функцию
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
<summary>Вызовам функций нужна точка начала</summary>

`B` может вызвать `A`, но ни одна из этих функций не запускается автоматически. Без `main` программе не с чего начать работу.
</details>

<details>
<summary>Ответ</summary>

Не удаётся собрать готовую программу: нет `main`.
</details>

### 14. `main` вызывает функцию вызывает функцию
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
<summary>Что происходит при вызове функции</summary>

Инструкции выполняются по порядку. Когда одна функция вызывает другую, она ждёт её завершения, а затем продолжает работу после вызова. Здесь `main` вызывает `B`; та печатает `B-before`, вызывает `A`, затем печатает `B-after`.
</details>

<details>
<summary>Ответ</summary>

Компилируется и печатает:
```text
B-before
A
B-after
```
</details>

### 15. Почти та же ситуация
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
<summary>Поместите функцию до её вызова</summary>

Компилятор читает файл сверху вниз. До вызова функции ему уже должно быть известно о ней. Здесь `B` вызывает `A` до её определения. Если перенести `A` выше `B`, ошибка исчезнет.
</details>

<details>
<summary>Ответ</summary>

Не компилируется.
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
