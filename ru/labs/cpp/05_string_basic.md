# Лабораторная работа 5

Тема: *основы строк.*

Сопровождающие [видео](https://www.youtube.com/watch?v=3aXFuiHxb9k&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=11&t=639):

## Задание 1

Сделайте функцию, которая считает сколько символов `1` в строке (`std::string_view`).

Сделайте несколько тестов для всех случаев (ни одной 1, несколько 1, все 1) используя `assert`.

<details>
<summary>Пример</summary>
```
void runTests()
{
    assert(countOnes("001100") == 2);
    // ...
}
```
</details>

## Задание 2

Сделайте функцию, которая находит в строке ` `,
и выдает кусок строки от позиции после этой позиции до следующего ` `.
Если следующего нет, пускай выдает остальную часть строки.

Сделайте тесты, как в прошлом задании.

Примеры: 
```
secondWord("Hello world") == "world"
secondWord("Hello my dear") == "my"
secondWord("") == ""
secondWord(" ") == ""
secondWord(" a ") == "a"
secondWord("a  ") == ""
```
