---
slug: ru/cpp/labs/advanced-practice
---
<!-- course-site-backlink:start -->
[Этот урок на сайте](https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms/ru/cpp/labs/advanced-practice/)
<!-- course-site-backlink:end -->
# Продвинутая практика

> Это продолжение [Практики по простым задачам](09_basic_practice.md).

## Что нужно развить в данной работе

- Более продвинутое моделирование предметной области;
- Хранение фиксированного количества элементов в `std::array`, включая массив внутри структуры;
- Использование `std::optional`;
- Идея владения;
- Задание названий через `std::string_view`;
- Изменение объектов через указатели и ссылки, а чтение — через `const`-ссылки и `std::span`;
- Написание маленьких функций, возвращающих `bool` или количество, с использованием `if` с ранними возвратами (guard clauses) и `switch` по `enum`;
- Перебор объектов в цикле, подсчет пустых мест, поиск первого пустого места.

## Инструменты, которые понадобятся

- `std::string_view` — это что-то вроде константной строки.
  Используйте его для названий и имен.

  Минимальный пример:
  ```cpp
  std::string_view s{ "Hello, world!" };
  std::cout << s << std::endl;
  ```

- `std::optional<T>` либо хранит `T`, либо пуст.

  Минимальный пример:
  ```cpp
  std::optional<int> slot{ std::nullopt };
  slot = 42;
  bool taken{ slot.has_value() };
  slot.reset();
  ```

## Задачи для практики

- **Книжная полка.** Полка вмещает 5 книг. У каждой книги есть название.
  Положите «Атлас» в слот 2 и уберите книгу из слота 0.
  Посчитайте, сколько слотов пустует.

  <details>
  <summary>
  Возможное решение
  </summary>

  Слот полки либо хранит книгу, либо пуст, поэтому тип слота —
  `std::optional<Book>` — пустой слот — это `std::nullopt`.
  Сами структуры нужны лишь для группировки, как в прошлой работе:

  ```cpp
  #include <array>
  #include <optional>
  #include <string_view>

  struct Book
  {
      std::string_view title;
  };

  struct Bookshelf
  {
      std::array<std::optional<Book>, 5> slots;
  };
  ```

  Допустим, слоты 0 и 3 хранят книги, а остальные пусты.
  Чтобы положить «Атлас» в слот 2, нужны три успешные проверки:
  указатель не `nullptr`, индекс 2 в пределах массива, в слоте 2 нет значения —
  только тогда сохраняем книгу и возвращаем успех (`true`).
  В слоте 0 последняя проверка не проходит, поэтому возвращаем `false`, ничего не меняя:

  ```cpp
  bool shelve_book(Bookshelf* shelf, std::size_t index, Book book)
  {
      if (shelf == nullptr)
      {
          return false;
      }
      if (index >= shelf->slots.size())
      {
          return false;
      }
      if (shelf->slots[index].has_value())
      {
          return false;
      }
      shelf->slots[index] = book;
      return true;
  }
  ```

  Взятие книги — зеркальный случай: в слоте 0 есть книга, поэтому очищаем его через `reset()`
  и возвращаем `true`; для пустого слота возвращаем `false`:

  ```cpp
  bool take_book(Bookshelf* shelf, std::size_t index)
  {
      if (shelf == nullptr)
      {
          return false;
      }
      if (index >= shelf->slots.size())
      {
          return false;
      }
      if (!shelf->slots[index].has_value())
      {
          return false;
      }
      shelf->slots[index].reset();
      return true;
  }
  ```

  Чтобы посчитать пустые, просто обходим каждый слот по очереди в цикле range-based `for` и прибавляем 1 за каждый слот без значения:

  ```cpp
  int empty_count(const Bookshelf& shelf)
  {
      int count{ 0 };
      for (const auto& slot : shelf.slots)
      {
          if (!slot.has_value())
          {
              count++;
          }
      }
      return count;
  }
  ```

  Использование из `main`:
  ```cpp
  Bookshelf shelf{};
  shelve_book(&shelf, 2, Book{ .title = "Atlas" });
  take_book(&shelf, 0);
  int free{ empty_count(shelf) };
  ```
  </details>

- **Из холодильника в морозилку.** Холодильник вмещает 3 продукта, морозилка вмещает 2 продукта.
  У каждого продукта есть название.
  Переместите пиццу с полки 1 холодильника на полку 0 морозилки.
  Старое место при этом освобождается.

  <details>
  <summary>
  Возможное решение
  </summary>

  Тот же принцип с полками, только контейнеров два: у холодильника 3 полки, у морозилки 2,
  каждая полка либо хранит продукт, либо пуста:

  ```cpp
  #include <array>
  #include <optional>
  #include <string_view>

  struct Food
  {
      std::string_view name;
  };

  struct Fridge
  {
      std::array<std::optional<Food>, 3> shelves;
  };

  struct Freezer
  {
      std::array<std::optional<Food>, 2> shelves;
  };
  ```

  Допустим, на полке 1 холодильника лежит пицца, а полка 0 морозилки пуста.
  При перемещении проходим проверки по порядку:
  оба указателя не `nullptr`, оба индекса в допустимых пределах,
  в источнике есть продукт, цель свободна.
  Затем два шага: копируем продукт на полку 0 морозилки,
  очищаем полку 1 холодильника через `reset()`.
  С этого момента пицца живет ровно в одном месте — в этом и состоит идея владения.
  Если хоть одна проверка не прошла, возвращаем `false` и ничего не трогаем:

  ```cpp
  bool move_food(Fridge* from, std::size_t fromIndex, Freezer* to, std::size_t toIndex)
  {
      if (from == nullptr || to == nullptr)
      {
          return false;
      }
      if (fromIndex >= from->shelves.size())
      {
          return false;
      }
      if (toIndex >= to->shelves.size())
      {
          return false;
      }
      if (!from->shelves[fromIndex].has_value())
      {
          return false;
      }
      if (to->shelves[toIndex].has_value())
      {
          return false;
      }
      to->shelves[toIndex] = from->shelves[fromIndex];
      from->shelves[fromIndex].reset();
      return true;
  }
  ```

  Использование из `main`:
  ```cpp
  Fridge fridge{};
  fridge.shelves[1] = Food{ .name = "pizza" };
  Freezer freezer{};
  bool moved{ move_food(&fridge, 1, &freezer, 0) };
  ```
  </details>

- **Разогрев супа.** Микроволновка либо вмещает одно блюдо, либо пуста.
  У каждого блюда есть название и состояние нагрева: холодное или горячее.
  Положите холодный суп внутрь, разогрейте до горячего состояния, затем достаньте.

  <details>
  <summary>
  Возможное решение
  </summary>

  Здесь всего один слот — поддон — плюс новый параметр, за которым нужно следить:
  состояние нагрева, которое бывает холодным или горячим:

  ```cpp
  #include <optional>
  #include <string_view>

  enum class Warmth
  {
      Cold,
      Hot,
  };

  struct Meal
  {
      std::string_view name;
      Warmth warmth;
  };

  struct Microwave
  {
      std::optional<Meal> tray;
  };
  ```

  Поддон изначально пуст. Когда кладем холодный суп внутрь, поддон свободен,
  поэтому сохраняем блюдо и возвращаем `true`;
  при второй попытке поддон уже занят, поэтому возвращаем `false`:

  ```cpp
  bool put_meal(Microwave* m, Meal meal)
  {
      if (m == nullptr)
      {
          return false;
      }
      if (m->tray.has_value())
      {
          return false;
      }
      m->tray = meal;
      return true;
  }
  ```

  При разогреве внутри есть блюдо, поэтому меняем его состояние на горячее.
  При разогреве пустой микроволновки внутри ничего нет, поэтому возвращаем `false`:

  ```cpp
  bool heat_meal(Microwave* m)
  {
      if (m == nullptr)
      {
          return false;
      }
      if (!m->tray.has_value())
      {
          return false;
      }
      m->tray->warmth = Warmth::Hot;
      return true;
  }
  ```

  При доставании копируем горячий суп для вызывающей стороны,
  очищаем поддон и возвращаем копию:

  ```cpp
  std::optional<Meal> take_meal(Microwave* m)
  {
      if (m == nullptr)
      {
          return std::nullopt;
      }
      if (!m->tray.has_value())
      {
          return std::nullopt;
      }
      std::optional<Meal> result{ m->tray };
      m->tray.reset();
      return result;
  }
  ```

  Использование из `main`:
  ```cpp
  Microwave mw{};
  put_meal(&mw, Meal{ .name = "soup", .warmth = Warmth::Cold });
  heat_meal(&mw);
  std::optional<Meal> lunch{ take_meal(&mw) };
  ```
  </details>

- **Выпить зелье.** У героя есть здоровье и щит.
  Зелье бывает красным, синим или испорченным.
  Дайте герою 1 красное зелье.
  Красное добавляет 20 здоровья, синее добавляет 10 щита, испорченное ничего не делает.

  <details>
  <summary>
  Возможное решение
  </summary>

  Вид зелья определяет эффект, поэтому оформляем его как `enum`.
  Герой и зелье — обычные структуры, нужные лишь для группировки данных:

  ```cpp
  enum class PotionKind
  {
      Red,
      Blue,
      Spoiled,
  };

  struct Potion
  {
      PotionKind kind;
  };

  struct Hero
  {
      int health;
      int shield;
  };
  ```

  Разберем случай красного зелья для героя с 50 единицами здоровья и 0 щита:
  указатель не `nullptr`, ветка `switch` для `Red` добавляет 20 здоровья
  и возвращает `true` — теперь у героя 70 здоровья.
  Синее зелье идет в следующую ветку и добавляет 10 щита.
  Испорченное зелье идет в последнюю ветку и возвращает `false`,
  не меняя героя:

  ```cpp
  bool drink_potion(Hero* hero, Potion potion)
  {
      if (hero == nullptr)
      {
          return false;
      }
      switch (potion.kind)
      {
          case PotionKind::Red:
              hero->health += 20;
              return true;
          case PotionKind::Blue:
              hero->shield += 10;
              return true;
          case PotionKind::Spoiled:
              return false;
      }
      return false;
  }
  ```

  Использование из `main`:
  ```cpp
  Hero hero{ .health = 50, .shield = 0 };
  drink_potion(&hero, Potion{ .kind = PotionKind::Red });
  ```
  </details>

- **Замачивание белья.** Корзина вмещает 3 вещи.
  В прачечной 2 корзины.
  У каждой вещи есть метка и состояние: грязная, замоченная или чистая.
  Замочите каждую грязную рубашку в корзине 0. Посчитайте, сколько было замочено.

  <details>
  <summary>
  Возможное решение
  </summary>

  Новая идея здесь — вложенность: `Basket` хранит массив,
  а `Laundry` хранит корзины:

  ```cpp
  #include <array>
  #include <optional>
  #include <string_view>

  enum class ClothState
  {
      Dirty,
      Soaked,
      Clean,
  };

  struct Cloth
  {
      std::string_view label;
      ClothState state;
  };

  struct Basket
  {
      std::array<std::optional<Cloth>, 3> slots;
  };

  struct Laundry
  {
      std::array<Basket, 2> tubs;
  };
  ```

  Допустим, слоты 0 и 1 корзины 0 хранят грязные рубашки, а слот 2 пуст.
  Цикл перебирает слоты по очереди по ссылке (`auto&`, см. лабу про ссылки):
  слот 0 грязный, поэтому помечаем его замоченным и засчитываем 1;
  слот 1 грязный, поэтому помечаем его замоченным и засчитываем 2;
  слот 2 пуст, поэтому пропускаем его.
  Функция возвращает 2:

  ```cpp
  int soak_basket(Basket* basket)
  {
      if (basket == nullptr)
      {
          return 0;
      }
      int soaked{ 0 };
      for (auto& slot : basket->slots)
      {
          if (!slot.has_value())
          {
              continue;
          }
          if (slot->state != ClothState::Dirty)
          {
              continue;
          }
          slot->state = ClothState::Soaked;
          soaked++;
      }
      return soaked;
  }
  ```

  Использование из `main`:
  ```cpp
  Laundry laundry{};
  laundry.tubs[0].slots[0] = Cloth{ .label = "shirt", .state = ClothState::Dirty };
  int n{ soak_basket(&laundry.tubs[0]) };
  ```
  </details>

- **Тюнинг машины.** Гараж вмещает 4 машины. У каждой машины есть модель, мощность и цена.
  Тюнингуйте машину 2: увеличьте мощность на 10, а цену — на 1000 за каждую добавленную единицу мощности.

- **Мойка машин.** Мойка вмещает 3 машины. Каждая машина бывает чистой или грязной.
  Помойте каждую грязную машину. Посчитайте, сколько было помыто.

- **Парковка.** На парковке 2 этажа по 4 места.
  Каждое место либо хранит машину, либо пусто.
  Поставьте новую машину на первое пустое место. Пройдите по местам с помощью арифметики указателей.

- **Двигатель машины.** Машина хранит указатель на свой двигатель. У двигателя есть износ от 0 до 100.
  Отсутствие двигателя означает пустой указатель.
  Проверьте двигатель через машину и отремонтируйте двигатель машины 1 до износа 0.

- **Рейлинг для чашек.** Рейлинг хранит указатели на 4 чашки. Некоторые крючки пусты.
  Повесьте новую чашку на первый пустой крючок и снимите чашку с крючка 1.
  Указатель движется вместе с чашкой.

- **Отряд героев.** Отряд вмещает 3 героев. У каждого героя есть здоровье и щит.
  Полечите героя 1 на 20 единиц здоровья. Посчитайте, скольким героям все еще нужно лечение.

- **Активный бафф.** Игрок хранит указатель на активный бафф. Отсутствие баффа означает пустой указатель.
  Дайте игроку 1 бафф на щит до боя и заберите его после боя.

- **Класс.** В комнате 2 ряда по 3 парты. Каждая парта либо хранит ученика, либо пуста.
  Посчитайте пустые парты. Посадите новичка за первую пустую парту.

- **Найти пиццу.** Холодильник вмещает 3 продукта с названиями.
  Найдите пиццу и переместите ее на полку 1 морозилки. Верните признак, была ли она найдена.
  Обращайтесь к полкам через `std::span`.

- **Замочить посуду.** На кухне 2 сушилки по 3 тарелки. Каждая тарелка бывает грязной или замоченной.
  Замочите каждую грязную тарелку в сушилке 0.

- **Комнаты библиотеки.** В библиотеке 2 комнаты по 3 слота. Каждый слот либо хранит книгу, либо пуст.
  Положите «Атлас» в первый пустой слот комнаты 1.

- **Светофор.** На перекрестке 3 светофора. Каждый светофор бывает красным, желтым или зеленым.
  Переключите светофор 2 на следующий цвет через `switch`.

- **Аптечка.** Шкафчик вмещает 4 коробки. Каждая коробка бывает свежей или просроченной.
  Верните признак, можно ли использовать коробку 1. Выбросите коробку 1, если она просрочена.

- **Столовая.** Столовая хранит 3 супа и 3 хлеба.
  Подайте суп 1 с хлебом 1. При подаче оба забираются.

- **Горячая цепочка.** На кухне есть холодильник, морозилка и микроволновка.
  Положите пиццу с полки 0 холодильника в микроволновку, разогрейте ее,
  затем переместите на полку 1 морозилки. Каждый шаг возвращает признак, получилось ли его выполнить.
