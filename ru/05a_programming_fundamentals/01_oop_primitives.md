# Ссылки (\&)

Ссылка - это по сути указатель, адрес которого
не может быть изменен, и имеет упрощенный синтаксис.

Вы также можете считать его псевдонимом для переменной (адреса в памяти).

```cpp
int main()
{
    int a = 5;
    
    int* pointer = &a;
    int& reference = a;
    
    *pointer = 10; // a = 10
    reference = 15; // a = 15
    
    int b = 20;
    // Нельзя перенаправить `reference` на `b`.
    // Следующий код запишет значение `b` (20) в `a`.
    reference = b; // a = 20
    reference = 10; // a = 10
    
    return 0;
}
```

Ссылки можно передавать в функции.
Они скрытно передадутся как указатели.

```cpp
void foo(int& a)
{
    a = 10;
    a = a + 5;
}

int main()
{
    int a = 5;
    foo(a); // a = 15
    return 0;
}
```

Та же программа, но с использованием указателя:

```cpp
void foo(int* a)
{
    *a = 10;
    *a = *a + 5;
}

int main()
{
    int a = 5;
    foo(&a); // a = 15
    return 0;
}
```

Вы можете применить `&` к ссылке, чтобы получить указатель на переменную.

Ссылка - это более ограниченная версия указателя, отлично подходящая для аргументов функций.
Считается хорошей практикой использовать ссылки вместо указателей при передаче аргументов в функции.


# Методы

Рассмотрим функцию, которая принимает переменную структуры.

> Не беспокойтесь о том, как работает `std::string` пока,
> просто концептуально думайте о ней как о строке.

```cpp
#include <iostream>

struct Person
{
    int age;
    std::string name;
};

void printAge(Person* person)
{
    std::cout << person->age;
}

int main()
{
    Person person;
    person.age = 20;
    person.name = "Джон";
    
    printAge(&person);
    
    return 0;
}
```

## `static` методы

Мы можем преобразовать эту функцию в функцию-член, также называемый методом.
Давайте сначала сделаем его статическим методом, чтобы увидеть, как работает концепция *пространств имен* (namespace).

> Обратите внимание, что методы существуют только в C++ и не в C.

> *Член* означает что-то, объявленное в `struct` или `class`.
> Это может быть как метод, так и поле.

```cpp
#include <iostream>

struct Person
{
    int age;
    std::string name;
    
    // Ключевое слово `static` на самом деле не делает его статическим,
    // оно просто требует вызывать эту функцию с использованием оператора разрешения области видимости (::).
    static void printAge(Person* person)
    {
        std::cout << person->age;
    }
};

int main()
{
    Person person;
    person.age = 20;
    person.name = "John";
    
    // Вот как вызывать статический метод объекта.
    // `Person` здесь пространство имен, а `printAge` - метод.
    // Идея заключается в том, что мы способны ассоциировать операции,
    // выполняемые с объектом `Person`, с пространством имен `Person` этой структуры.
    Person::printAge(&person);
    
    return 0;
}
```

Вы можете разделить объявление от определения, так же, как и с обычными функциями.
Обратите внимание, что нет другого синтаксиса для этого, 
вам придется указать имя структуры в определении.

```cpp
struct Person
{
    int age;
    std::string name;
    
    static void printAge(Person* person);
};

// Можете считать `Person::printAge` именем этой функции.
void Person::printAge(Person* person)
{
    std::cout << person->age;
}
```

## Экземпляры и объекты

Объект означает некоторую память, будь то переменная, элемент массива или любое другое хранилище, которое содержит данные определенного типа. Например, если у вас есть структура `Person`, и код выглядит так:

```cpp
Person person;
```

Мы можем сказать, что переменная `person` ссылается на объект типа `Person`. Другими словами, объект — это значение, которое находится в какой-то области памяти, и сама память, в которой оно находится.

Экземпляр означает практически то же самое, что и объект, но смещает акцент с памяти на тип данных, хранящихся в этой памяти. Таким образом, можно сказать, что `person` является экземпляром `Person`.

## Не статические (instance) методы

Теперь давайте сделаем его методом объекта, который не является статическим.
Метод объекта без статического характера имеет более простой синтаксис вызова,
и автоматически передает указатель на экземпляр как первый скрытый параметр с именем `this`.

```cpp
struct Person
{
    int age;
    std::string name;
    
    // Метод объекта.
    void printAge()
    {
        // `this` - это указатель на экземпляр (`Person*`).
        std::cout << this->age;
    }
};

int main()
{
    Person person;
    person.age = 20;
    person.name = "John";
    
    // Вот как вызывать метод объекта.
    // Компилятор автоматически передает указатель на экземпляр как первый параметр.
    person.printAge();
    
    return 0;
}
```

Это позволяет нам объединить функциональность с типом данных
и получить семантику "объект.глагол".


> `this->` можно не указывать.

```cpp
struct Person
{
    // ...
    void printAge()
    {
        // `age` ссылается на `this->age`.
        std::cout << age;
    }
};
```
Вы можете разделить определение от объявления так же, как с методами объекта.


# Доступность (accessibility) и `class`

По умолчанию, все члены структуры являются `public`.
Это означает, что они могут быть доступны в экземпляре структуры.
Вы можете сделать их явно `private`, чтобы запретить доступ.

Сначала это может показаться абсолютно бесполезным. 
В чем смысл запрета доступа к некоторой памяти?
Одна из идей заключается в том, чтобы ограничить способы доступа
и изменения данных, чтобы стало очевидным, какой из них является правильным, используя методы.

Это не есть что-то уникальное для ООП, это возможно и на уровне модуля, путем объявления функции как `static`.
(видимые только внутри компиляционной единицы, в которой они были определены).
Однако *модификаторы доступности* являются исключительно ООП фичей.

```cpp
struct Person
{
private:
    int age;
    std::string name;

public:
    void setAge(int age)
    {
        this->age = age;
    }

    void printAge()
    {
        std::cout << this->age;
    }

    void printName()
    {
        std::cout << this->name;
    }
};

int main()
{
    Person person;
    person.age = 15; // ошибка компиляции: невозможно получить доступ к закрытому полю.
    person.name = "John"; // та же ошибка

    person.setAge(15); // компилируется
    person.printAge(); // компилируется
    person.printName(); // компилируется

    return 0;
}
```

Вы можете сделать некоторые поля `private`, а другие - `public`.

```cpp
struct Person
{
private:
    int age;

public:
    std::string name;
}

int main()
{
    Person person;
    person.age = 10; // ошибка компиляции: невозможно получить доступ к закрытому полю.
    person.name = "John"; // работает
    return 0;
}
```


## `class`

`class` эквивалентен `struct`, единственное различие
заключается в том, что у него есть неявное `private:` в начале.
Таким образом, все члены по умолчанию являются публичными в `struct`, но приватными в `class`.

> `class` - это ключевое слово, которое обычно используется в контексте ООП.
> Считается хорошим тоном использовать `class` вместо `struct`, если вы объявляете методы,
> которые инкапсулируют (предоставляют конкретные способы доступа) данные (поля).

```cpp
struct Person
{
private:
    int age;
    std::string name;
}

// эквивалентно

class Person
{
    int age;
    std::string name;
}

// и наоборот ...

class Person
{
public:
    int age;
    std::string name;
}

// эквивалентно

struct Person
{
    int age;
    std::string name;
}
```
