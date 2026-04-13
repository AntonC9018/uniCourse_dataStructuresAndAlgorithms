# Ссылки

## Концепты

- rvalue, lvalue
- Ссылка

## Вопросы на понимание

Что произойдет при запуске этого кода? Почему?

> Там, где `main` не был расписан, код помещается в типичный основной файл:
> ```cpp
> #include <iostream>
> #include <array> // надо для std::array
>
> int main()
> {
>     // сюда
> }
> ```

### 1. Присваивание числа к числу
```cpp
5 = 6;
```

<details>
<summary>Ответ</summary>

`5` это rvalue, ему нельзя присваивать значение, потому что оно не является объектом (lvalue).
</details>

### 2. Адрес числа
```cpp
int* a = &5;
```

<details>
<summary>Ответ</summary>

Нельзя брать адрес rvalue. 
Можно брать адрес памяти только от lvalue (выражений, результат которого есть объект),
поскольку числа сами по себе не хранятся в памяти.
</details>

### 3. Адрес выражения
```cpp
int* a = &(5 + 6);
```

<details>
<summary>Ответ</summary>

Аналогичная ситуация, `(5 + 6)` это rvalue.
Невозможно взять адрес rvalue.
</details>

### 4. Ссылка из числа
```cpp
int& a = 5;
```

<details>
<summary>Ответ</summary>

В ссылочную переменную можно записать только lvalue (ссылку на объект),
поскольку `a` должна будет ссылаться по итогу на *ячейку* памяти (объект),
а не просто на значение.
</details>

### 5. Ссылка из переменной
```cpp
int a = 5;
int& b = a;
std::cout << a << std::endl;
std::cout << b << std::endl;
```

<details>
<summary>Ответ</summary>

Здесь, в `b` сохраняется *ссылка* на `a`.
Под капотом, компилятор либо определит `b` как просто другое имя для `a`,
либо по факту сохранит в `b` указатель на `a`. 

При считывании, использование имени `b` аналогично использованию имени `a` 
— они обе ссылаются на тот же объект.
Их отличие в том, что `a` для создасться и *хранилище* при выполнении инструкции,
то есть выделится стековая память под объект.

Напечатается `5` 2 раза.
</details>

### 6. Присваивание числа к ссылке
```cpp
int a = 5;
int& b = a;
b = 6;
std::cout << a << std::endl;
```

<details>
<summary>Ответ</summary>

`a` тут перезапишется на `6` через имя `b`.
</details>

### 7. Перезапись переменной, на которую существует ссылка
```cpp
int a = 5;
int& b = a;
a = 6;
std::cout << b << std::endl;
```

<details>
<summary>Ответ</summary>

`a` перезаписывается напрямую. 

Поскольку `b` является *ссылкой* на `a` (например, хранит в себе адрес `a`)
считывание из `b` считает из `a`.
</details>


### 8. Ссылка из выражения
```cpp
int a = 5;
int& b = a + 7;
std::cout << a << std::endl;
std::cout << b << std::endl;
```

<details>
<summary>Ответ</summary>

`a + 7` это rvalue, а не lvalue.
Поскольку нельзя получить ссылку на rvalue, данный код не скомпилируется.
</details>

### 9. Оператор с перезаписью примененный на ссылку
```cpp
int a = 5;
int& b = a;
b += 7;
std::cout << a << std::endl;
std::cout << b << std::endl;
```

<details>
<summary>Ответ</summary>

`b` как бы заменяется на `a`.
Здесь обновится `a`.

Так как `b` ссылается на `a`, напечатается то же для обеих переменных (12).
</details>

### 10. Присваивание переменной ссылке
```cpp
int a = 1;
int b = 2;
int& c = a;
c = b;
std::cout << a << std::endl;
std::cout << b << std::endl;
std::cout << c << std::endl;
```

<details>
<summary>Ответ</summary>

`c = b` не перезаписывает ссылку. Ссылку невозможно перезаписать.

В `c = b` вы как бы вставляете вместо `c` то, на что она ссылается (`a`),
получая `a = b`, что перезаписывает `a` на значение из `b`, `2`.

Выведется:
```
2
2
2
```

</details>

### 11. Перезапись ссылки на число после присвоения ей переменной
```cpp
int a = 1;
int b = 2;
int& c = a;
c = b;
c = 3;
std::cout << a << std::endl;
std::cout << b << std::endl;
std::cout << c << std::endl;
```

<details>
<summary>Ответ</summary>

Ссылки, в контраст с указателями, невозможно "перенаправить".

Здесь иллюстрируется тот факт, что `c` продолжает ссылаться на `a`,
даже после строчки `c = b`.

Выведется:
```
3
2
3
```
</details>

### 12. Ссылка из dereference-а
```cpp
int a = 1;
int* pa = &a;
int& b = *pa;
*pa = 2;
b = 3;
std::cout << a << std::endl;
std::cout << b << std::endl;
std::cout << *pa << std::endl;
```

<details>
<summary>Ответ</summary>

`int& b = *pa;` здесь ссылка происходит из указателя.
Все 3 имени теперь указывают на `a`.

Выведется `3` 3 раза.
</details>

### 13. Перезапись указателя на адрес ссылки
```cpp
int a = 1;
int b = 2;
int* p = &a;
int& r = *p;
p = &b;
r = 3;
std::cout << a << std::endl;
std::cout << b << std::endl;
```

<details>
<summary>Ответ</summary>

Изменится `a`, а не `b`. Выведется:
```
3
2
```
</details>

### 15. Перезапись переменной через адрес и ссылка
```cpp
int a = 1;
int& b = a;
int* c = &b;
*c = 2;
std::cout << a << std::endl;
```

<details>
<summary>Ответ</summary>

Из ссылки можно также получать адрес.
Здесь, `*c = 2;` перезапишет `a`.
</details>


### 19. Ссылки на поля
```cpp
#include <iostream>

struct Position
{
   int x;
   int y;
};

int main()
{
   Position a{ .x = 1, .y = 2 };

   Position& ra = a;

   int& rx = ra.x;
   ra.x = 3;

   ra.y = 4;
   int& ry = ra.y;

   std::cout << rx << std::endl;
   std::cout << ry << std::endl;

   std::cout << ra.x << std::endl;
   std::cout << ra.y << std::endl;

   std::cout << a.x << std::endl;
   std::cout << a.y << std::endl;
}
```

<details>
<summary>Ответ</summary>

Ссылки можно создавать на объекты внутри бОльших объектов.

Тут везде напечатается `3` и `4`.
</details>

### 21. Ссылка на адрес (1)
```cpp
int a = 1;
int b = 2;
int* pa = &a;
int*& rpa = pa;
pa = &b;
*rpa = 3;
std::cout << a << std::endl;
std::cout << b << std::endl;
```

<details>
<summary>Ответ</summary>

Можно создавать ссылки на указатели, потому что указатели тоже объекты (адреса в ячейках памяти).

Тут мы перезаписывает адрес сохраненный в `pa` напрямую, 
а считывает *адрес* по ссылке.

`*rpa` -> `*pa` -> `*(&b)` -> `b`

В `a` будет `1`, а в `b` будет `3`.
</details>

### 22. Ссылка на адрес (2)
```cpp
int a = 1;
int b = 2;
int* pa = &a;
int*& rpa = pa;
pa = &b;
int& rb = *rpa;
rb = 3;

std::cout << a << std::endl;
std::cout << b << std::endl;
```

<details>
<summary>Ответ</summary>

Здесь иллюстрируется тот факт, что можно создавать ссылки исходя 
из любых выражений, которые по итогу дают ссылку.

`rb = 3` впишет `3` в `b`.
</details>

### 26. Размер ссылки

Возможно ли у ссылки взять размер? Какой размер у ссылки?

```cpp
#include <iostream>

int main()
{
   int a = 6;
   int& b = a;
   std::cout << sizeof(b) << std::endl;
}
```

<details>
<summary>Ответ</summary>

`sizeof(b)` сработает, но даст размер `int`-а, а не ссылки.

Размер ссылки получить невозможно, это скрыто компилятором.

Однако, если ссылка передается параметром в функцию, 
по факту передастся адрес, размер которого 8 байт.

> Адрес необходимо передать, потому что функция не сможет 
> получить доступ к той что надо переменной без внешнего контекста.
> Самый простой способ получить доступ к переменной, определенной извне — это передать ее адрес.
</details>

### 24. Пример использования ссылок (1)
```cpp
#include <iostream>

void resetAmount(int& amount)
{
   amount = 0;
}
int main()
{
   int appleAmount = 6;
   resetAmount(appleAmount);
   std::cout << appleAmount << std::endl;
}
```

<details>
<summary>Ответ</summary>

`appleAmount` перезапишется на `0`, так как функции передастся ссылка на нее.

Под капотом, передается *адрес* переменной `appleAmount`, но это скрывается компилятором.
</details>

### 25. Пример использования ссылок (2)
```cpp
#include <iostream>

struct Arm
{
   int power;
};

void increasePower(Arm& arm)
{
   arm.power += 1;
}

int main()
{
   Arm arm { 1 };
   increasePower(arm);
   std::cout << arm.power << std::endl;
}
```

<details>
<summary>Ответ</summary>

В функции можно передавать ссылки на объекты типа структуры.
Здесь, задача функции — увеличить силу.
</details>

