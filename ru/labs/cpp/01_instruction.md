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

Функция `main` автоматически запустится при запуске этой программы.

Сама функция не содержит инструкций в теле (пустые фигурные скобки).
По этой причине, при выполнении `main` ничего не будет напечатано.
</details>

### 2. Пустая функция `A`

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

### 3. Функция `A`

```cpp
void A()
{
    std::cout << "Hello World." << std::endl;
}
```

<!-- Ничего, A, void, 0, Hello World, ошибка компиляции, ошибка при выполнении -->

<details>
<summary>Ответ</summary>

Произойдет ошибка компиляции по той причине, что не включен хедер `<iostream>`.
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

### 4. Исправленная функция `A`

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

### 5. Функция `main`

```cpp
#include <iostream>

void main()
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

### 6. Функция `Main`

```cpp
#include <iostream>

void Main()
{
    std::cout << "Hello World." << std::endl;
}
```

<!-- Ничего, A, void, 0, Hello World, ошибка компиляции, ошибка при выполнении -->

<details>
<summary>Ответ</summary>

C++ чувствителен к заглавности букв в именах функций и в именах других сущностей.
Функции `main` нет, как и [во втором вопросе](#2-пустая-функция-A).
</details>

### 7. Коммент

```cpp
#include <iostream>

void main()
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

### 8. Коммент всего

```cpp
void main()
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

### 9. Функция вызывает функцию

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

### 10. `main` вызывает функцию вызывает функцию

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
void main()
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

### 11. Почти та же ситуация

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
void main()
{
    B();
}
```

<details>
<summary>Ответ</summary>

Теперь программа не скомпилируется.
`A` должны быть объявлена до того в исходном файле, как ее вызывает `B`.
</details>
