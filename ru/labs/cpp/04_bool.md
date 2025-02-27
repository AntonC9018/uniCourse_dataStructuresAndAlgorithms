# Лабораторная работа 4

Тема: `bool`, flow control.

Сопровождающие видео:
- [`bool`, flow control](https://www.youtube.com/watch?v=21m4VfonFnA&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=10)
- [span](https://www.youtube.com/watch?v=3aXFuiHxb9k&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=11) (до строк)

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


## Цикл

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
