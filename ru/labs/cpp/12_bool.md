# `bool`

Тема: `bool`, flow control.

Видео:
- [`bool`, flow control](https://www.youtube.com/watch?v=21m4VfonFnA&list=PL4sUOB8DjVlWUcSaCu0xPcK7rYeRwGpl7&index=10)

## Концепты

- Логические значения (`true`, `false`)
- Логические выражения
- Операторы сравнения чисел `>`, `<`, `>=`, `<=`, `==`, `!=`
- Логические операторы `&&`, `||`, `==`, `!`, `!=`
- Lazy evaluation операндов операторов `&&` и `||`
- Неявное преобразование в `bool` из `int` и указателей
- Макро `NULL`
- Особое значение `nullptr`

## Примеры на понимание

### 1. `true`
```cpp
bool a { true };
std::cout << a << std::endl;
```

<details>
<summary>Ответ</summary>

Тип `bool` принимает только два значения: `true` и `false`.  
При выводе в консоль, напечатается `1` для `true` и `0` для `false`.
</details>

### 2. `0` и `1` как `bool`
```cpp
bool a { 0 };
bool b { 1 };
```

<details>
<summary>Ответ</summary>

Вместо `false` можно также сохранить `0`, а вместо `true` можно сохранить `1`.
Это с успехом компилируется.
</details>

### 3. Конверсия `int` в `bool`
```cpp
bool c { static_cast<bool>(123) };
```

<details>
<summary>Ответ</summary>

`static_cast<bool>` для `int` дает `true`, если число не `0`, иначе `false`.
В `c` будет `true`.
</details>

### 4. Размер `bool`
```cpp
std::cout << sizeof(bool) << std::endl;
```

<details>
<summary>Ответ</summary>

`bool` занимает 1 байт, несмотря на то, что для представления 2-х значений, 
0 или 1, достаточно всего одного бита.
Если хотите, сохранить несколько `bool` значений в отдельные биты
в один и тот же байт, необходимо использовать побитовые маски.
</details>

### 5. `bool` выражение (1)
```cpp
bool a = 1 == 2;
std::cout << a << std::endl;
```

<details>
<summary>Ответ</summary>

Оператор `==` применяется к 2 выражениям и возвращает результат проверки на равенство, как логическое значение.
Результат `false`.
</details>

### 6. `bool` выражение (2)
```cpp
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

### 7. `bool` выражение (3)
```cpp
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

### 8. `bool` выражение (4)
```cpp
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

### 9. Перезапись `bool` переменной
```cpp
bool a = 1 > 2;
a = 3 == 3;
std::cout << a << std::endl;
```

<details>
<summary>Ответ</summary>

Здесь, `a` перезапишется с `false` на другое значение (`true`).
</details>

### 10. Функция с `bool` параметром из переменной
```cpp
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

### 11. Функция с `bool` параметром из выражения
```cpp
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

### 12. Функция перезаписывающая `bool` параметр
```cpp
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

### 13. `bool` `return`
```cpp
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

### 14. Пример логической функции
```cpp

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

### 15. Сравнение логических переменных
```cpp
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

### 16. Оператор `!`
```cpp
bool a = false;
bool b = !a;
std::cout << b << std::endl;
```

<details>
<summary>Ответ</summary>

Оператор `!` делает из `false` `true` (и наоборот).
</details>

### 17. Оператор `&&`
```cpp
bool a = true;
bool b = false;
bool c = a && b;
std::cout << c << std::endl;
```

<details>
<summary>Ответ</summary>

`a && b` -> `true && false` -> `false`, потому что оба операнда должны быть `true`.
</details>

### 18. Тонкости оператора `&&` (1)
```cpp
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

### 19. Тонкости оператора `&&` (2)
```cpp
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

### 20. Тонкости оператора `&&` (3)
```cpp
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

### 21. Тонкости оператора `&&` (4)
```cpp
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

### 22. Функция перезаписывает переменную из выражения параметра
```cpp
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

