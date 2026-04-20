# Строки

- Сопровождающие [видео](https://www.youtube.com/watch?v=3aXFuiHxb9k&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=11&t=639):
- [Видео про виды памяти](https://www.youtube.com/watch?v=jAr_jicQv4Y&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=22)

## Концепты

- Кодировки, код символа, ASCII
- C-строки, null-termination
- Расположение строковых литералов в памяти
- `std::string_view`

## Примеры на анализ

### 1. Размер `char`
```cpp
std::cout << sizeof(char) << std::endl;
```

### 2. Печать символа
```cpp
char a { '1' };
std::cout << a << std::endl;
```

### 3. Символ как число
```cpp
char a { '1' };
std::cout << static_cast<int>(a) << std::endl;
```

### 4. Число как символ
```cpp
char a { 98 };
std::cout << a << std::endl;
```

### 5. Печать адреса массива символов с 0 на конце
```cpp
std::array<char, 2> s{ 'a', 0 };
char* p{ s.data() };
std::cout << p << std::endl;
```

### 6. Печать адреса массива символов с 0 в середине
```cpp
std::array<char, 5> s{ 'a', 'b', 0, 'c', 'd' };
std::cout << s.data() << std::endl;
```

### 7. Печать массива после модификации
```cpp
std::array<char, 5> s{ 'a', 'b', 'c', 'd', 0 };
std::cout << s.data() << std::endl;
s[1] = 'e';
std::cout << s.data() << std::endl;
s[2] = 0;
std::cout << s.data() << std::endl;
```

<!-- ab, a, ab0cd, cd, адрес s, UB -->
### 8. Код символа `\0`
```cpp
char z{ '\0' };
std::cout << static_cast<int>(z) << std::endl;
```

### 9. `\0` в массиве
```cpp
std::array<char, 5> s{ 'a', 'b', '\0', 'c', 'd' };
std::cout << s.data() << std::endl;
```

### 10. Silencing warnings about unused variables

Скомпилируйте эту программу с флагом `-Wunused` и интерпретируйте результат.

```cpp
int main()
{
    [[maybe_unused]] int a{ 1 };

    int b{ 2 };
    (void) b;

    int c{ 3 };
}
```

<details>
<summary>Результат компиляции</summary>

Компилятор определяет, что переменные не были нигде использованы, 
но дает ошибку только для `c`.
```
❯ g++ -std=c++20 -Wall -Wconversion -Wextra -Wunused -pedantic test.cpp
test.cpp: In function ‘int main()’:
test.cpp:7:5: warning: unused variable ‘c’ [-Wunused-variable]
    7 | int c{ 3 };
      |     ^
```
</details>

### 11. Печать адреса массива символов без 0 на конце
```cpp
std::array<char, 2> s{ 'a', 'b' };
std::array<char, 2> s1{ '1', '\0' };
(void) s1;
std::cout << s.data() << std::endl;
```

<details>
<summary>Ответ</summary>

Это UB, но компилятор не определяет этого при компиляции, 
не давая никаких предупреждений.

Вероятно, переменные будут расположены друг за другом в памяти:

<table>
    <tr>
        <th><b>Переменная</b></th>
        <th colspan="2">s</th>
        <th colspan="2">s1</th>
    </tr>
    <tr>
        <th><b>Символ</b></th>
        <th>a</th>
        <th>b</th>
        <th>1</th>
        <th>'\0'</th>
    </tr>
    <tr>
        <th><b>Код</b></th>
        <th>97</th>
        <th>98</th>
        <th>49</th>
        <th>0</th>
    </tr>
</table>

Поскольку печать указателя напечатает все символы от заданного адреса (первый адрес `s`)
до первого 0, напечатается и `1` из массива `s1` до `\0` из массива `s1`.
Если бы в `s1` не было `\0` на конце, печать бы продолжилась 
до первого нулевого байта после памяти переменной `s1`,
что печатало бы данные оставшиеся там от предыдущего использования этой памяти.
</details>

### 12. Строка как массив
```cpp
char s[]{ "12" };
size_t count{ sizeof(s) }; // sizeof(char) == 1
std::cout << count << std::endl;
std::cout << s << std::endl;
std::cout << static_cast<int>(s[count - 1]) << std::endl;
```

<details>
<summary>Ответ</summary>

`s` будет состоять из 3 символов, а не 2!
Когда строковый литерал используется для инициализации массива,
он автоматически включает `\0` на конце.
</details>

### 13. Строка с `\0` как массив
```cpp
char s[]{ "12\0" };
std::cout << sizeof(s) << std::endl;
```

<details>
<summary>Ответ</summary>

`s` будет состоять из 4 символов!
Немотря на то, что на конце у `s` уже и так есть нулевой байт, компилятор добавит еще один.
</details>

<details>
<summary>Ответ</summary>

`s` будет состоять из 3 символов, а не 2!
Когда строковый литерал используется для инициализации массива,
он автоматически включает `\0` на конце.
</details>

### 14. `\0` pitfalls
```cpp
char arr[]{ "1\023" };
std::cout << sizeof(arr) << std::endl;
```

<details>
<summary>Объяснение</summary>

Здесь `\0` воспринимается вместе с `23` как одно целое, 
представляя код символа в 8-чной системе счисления.

Чтобы вставить  `\0` здесь во вторую позицию, 
можно использовать конкатенацию строковых литералов:
```cpp
char arr[]{ "1\0" "23" };
```
</details>

### 15. `std::to_array` (1)
```cpp
auto s{ std::to_array("abc") };
std::cout << s.size() << std::endl;
```

### 16. `std::to_array` (2)
```cpp
auto s{ std::to_array("a\0bc") };
std::cout << s.size() << std::endl;
```

### 17. `const char*`

- Где хранятся символы строки?
- Почему необходим `const`?
- Как получить длину строки?

```cpp
const char* s{ "123" };
std::cout << s << std::endl;
```

<details>
<summary>Где хранятся символы</summary>

Символы попадают в статическую память.
Указатель на начало этого блока памяти с символами 
строки хранится в стеке в переменной `s`.
</details>

<details>
<summary>Почему <code>const</code>?</summary>

Зачастую, строки попадают в readonly память, 
которую программе не позволительно изменять.
Это так сделано специально, потому что строки литералов фиксированы, поскольку они **общие**.
Чтобы гарантировано работать с ожидаемой строкой при использовании литерала,
они должны быть защищены от модификаций.

В следующем примере, адреса в `a` и `b` будут те же:
```cpp
const char* a{ "123" };
const char* b{ "123" };
std::cout << static_cast<void*>(a) << std::endl;
std::cout << static_cast<void*>(b) << std::endl;
```
</details>

<details>
<summary>Длина строки</summary>

`sizeof(s)` здесь дает размер объекта `s`, смотря на его тип, `const char*`.
А любой указатель занимает 8 байтов.

`sizeof(s)` здесь **не даст длину строки**, 
потому что буфер с символами **это не объект** 
(не имеет длину, известную во время компиляции).

Чтобы получить длину строки, нужно пройтись по ее байтам 
в поиске конца строки (нулевого символа), 
ведя счет по ходу ее прохождения.
Однако это может не дать реальную длину строки, если в середине строки есть нулевой символ.
Поэтому в C++ **невозможно получить реальную длину строки из `const char*`**.

Можно получить длину литерала, если создать ссылку на него 
до того, как прозошел decay в `const char*`:
```cpp
// Размер есть в типе, можно использовать как указатель.
const char(&s)[4]{"123"};

// Сам определяет тип const char(&)[4] из строки.
auto& s{"123"};
```
</details>

### 18. Сравнение строк (1)

```cpp
const char* a{ "123" };
auto b{ std::to_array("123") };
const char* bp{ b.data() };
if (a == bp)
{
    std::cout << "Equal" << std::endl;
}
else
{
    std::cout << "Not Equal" << std::endl;
}
```

### 18. Сравнение строк (2)
```cpp
#include <iostream>
#include <array>
#include <cstring>

int main()
{
    const char* a{ "123" };
    auto b{ std::to_array("123") };
    const char* bp{ b.data() };
    if (std::strcmp(a, b) == 0)
    {
        std::cout << "Equal" << std::endl;
    }
    else
    {
        std::cout << "Not Equal" << std::endl;
    }
}
```

### 18. `std::string_view` после модификации источника
```cpp
std::array<char, 4> arr{ "123" };
std::string_view v{ arr.data(), 3 };
arr[0] = 'a';
std::cout << v << std::endl;
```

### 19. `std::string_view` применим для любой памяти

```cpp
#include <iostream>
#include <string_view>
#include <array>

void usage(std::string_view v)
{
    std::cout << v.size() << std::endl;
    std::cout << v << std::endl;
}

int main()
{
    {
        std::array<char, 3> s{ 'a', 'b', 'c' };
        usage({ s.data(), s.size() });
    }
    {
        auto s{ std::to_array("abc") };
        usage({ s.data() });
    }
    {
        char s[]{ "abc" };
        usage({ s });
    }
    {
        auto& s{ "abc" };
        usage({ s });
    }
    {
        const char* s{ "abc" };
        usage({ s });
    }
}
```

### 20. `std::string_view` определяет длину при создании

Если длина строки не задана вручную,
`std::string_view` при создании попытается ее определить,
проходя по строке до обнаружения нулевого байта,
даже если тип передаваемого параметра содержит эту информацию.

Этого не произойдет только при создании `std::string_view` из другого `std::string_view`.

```cpp
#include <iostream>
#include <string_view>
#include <array>

void usage(std::string_view v)
{
    std::cout << v.size() << std::endl;
    std::cout << v << std::endl;
}

int main()
{
    {
        std::array<char, 3> s{ 'a', '\0', 'c' };
        usage({ s.data(), s.size() });
    }
    {
        auto s{ std::to_array("a\0c") };
        usage({ s.data() });
    }
    {
        char s[]{ "a\0c" };
        usage({ s });
    }
    {
        auto& s{ "a\0c" };
        usage({ s });
    }
    {
        const char* s{ "a\0c" };
        usage({ s });
    }
    {
        std::string_view s{ "a\0c", 3 };
        usage({ s }); // 3
    }
}
```

### 20. Сравнение строк через `std::string_view`

```cpp
auto s1{ std::to_array("abc") };
auto& s2{ "abc" };

std::string_view v1{ s1.data(), s1.size() - 1 };
std::string_view v2{ s2, sizeof(s2) - 1 };

if (v1 == v2)
{
    std::cout << "Equal" << std::endl;
}
else
{
    std::cout << "Not Equal" << std::endl;
}
```

## Подсчет символа 1

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

## Получение слова

Сделайте функцию, которая находит в строке ` `,
и выдает кусок строки от позиции после этой позиции до следующего ` `.
Если следующего нет, пускай выдает остальную часть строки.

Сделайте тесты, как в прошлом задании.

Примеры: 
```
secondWord("Hello world") == "world"
secondWord("Hello my dear") == "my"
secondWord("Hello") == ""
secondWord("") == ""
secondWord(" ") == ""
secondWord(" a ") == "a"
secondWord("a  ") == ""
secondWord("a  b") == ""
secondWord("hello     world    dear") == ""
```
