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
  Чтобы положить «Атлас» в слот 2, нужны две проверки:
  индекс 2 в пределах массива, в слоте 2 нет значения —
  только тогда сохраняем книгу и возвращаем успех (`true`).
  Сам указатель не проверяется: функция ожидает, что он никогда не `nullptr`.
  В слоте 0 последняя проверка не проходит, поэтому возвращаем `false`, ничего не меняя:

  ```cpp
  #include <cassert>

  bool shelve_book(Bookshelf* shelf, std::size_t index, Book book)
  {
      assert(shelf != nullptr); // shelve_book ожидает, что shelf никогда не nullptr
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

  Ссылка не может быть `nullptr`, поэтому передача полки по `&` вместо `*`
  гарантирует, что она никогда не `nullptr`. Остальные примеры используют ссылки по этой причине.

  Взятие книги — зеркальный случай: в слоте 0 есть книга, поэтому очищаем его через `reset()`
  и возвращаем `true`; для пустого слота возвращаем `false`:

  ```cpp
  bool take_book(Bookshelf& shelf, std::size_t index)
  {
      if (index >= shelf.slots.size())
      {
          return false;
      }
      if (!shelf.slots[index].has_value())
      {
          return false;
      }
      shelf.slots[index].reset();
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
  take_book(shelf, 0);
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
  оба индекса в допустимых пределах,
  в источнике есть продукт, цель свободна.
  Затем два шага: копируем продукт на полку 0 морозилки,
  очищаем полку 1 холодильника через `reset()`.
  С этого момента пицца живет ровно в одном месте — в этом и состоит идея владения.
  Если хоть одна проверка не прошла, возвращаем `false` и ничего не трогаем:

  ```cpp
  bool move_food(Fridge& from, std::size_t fromIndex, Freezer& to, std::size_t toIndex)
  {
      if (fromIndex >= from.shelves.size())
      {
          return false;
      }
      if (toIndex >= to.shelves.size())
      {
          return false;
      }
      if (!from.shelves[fromIndex].has_value())
      {
          return false;
      }
      if (to.shelves[toIndex].has_value())
      {
          return false;
      }
      to.shelves[toIndex] = from.shelves[fromIndex];
      from.shelves[fromIndex].reset();
      return true;
  }
  ```

  Использование из `main`:
  ```cpp
  Fridge fridge{};
  fridge.shelves[1] = Food{ .name = "pizza" };
  Freezer freezer{};
  bool moved{ move_food(fridge, 1, freezer, 0) };
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
  bool put_meal(Microwave& m, Meal meal)
  {
      if (m.tray.has_value())
      {
          return false;
      }
      m.tray = meal;
      return true;
  }
  ```

  При разогреве внутри есть блюдо, поэтому меняем его состояние на горячее.
  При разогреве пустой микроволновки внутри ничего нет, поэтому возвращаем `false`:

  ```cpp
  bool heat_meal(Microwave& m)
  {
      if (!m.tray.has_value())
      {
          return false;
      }
      m.tray->warmth = Warmth::Hot;
      return true;
  }
  ```

  При доставании копируем горячий суп для вызывающей стороны,
  очищаем поддон и возвращаем копию:

  ```cpp
  std::optional<Meal> take_meal(Microwave& m)
  {
      if (!m.tray.has_value())
      {
          return std::nullopt;
      }
      std::optional<Meal> result{ m.tray };
      m.tray.reset();
      return result;
  }
  ```

  Использование из `main`:
  ```cpp
  Microwave mw{};
  put_meal(mw, Meal{ .name = "soup", .warmth = Warmth::Cold });
  heat_meal(mw);
  std::optional<Meal> lunch{ take_meal(mw) };
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
  ветка `switch` для `Red` добавляет 20 здоровья
  и возвращает `true` — теперь у героя 70 здоровья.
  Синее зелье идет в следующую ветку и добавляет 10 щита.
  Испорченное зелье идет в последнюю ветку и возвращает `false`,
  не меняя героя:

  ```cpp
  bool drink_potion(Hero& hero, Potion potion)
  {
      switch (potion.kind)
      {
          case PotionKind::Red:
              hero.health += 20;
              return true;
          case PotionKind::Blue:
              hero.shield += 10;
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
  drink_potion(hero, Potion{ .kind = PotionKind::Red });
  ```
  </details>

- **Замачивание белья.** Корзина вмещает 3 вещи.
  В прачечной 2 корзины.
  У каждой вещи есть метка и состояние: грязная, замоченная или чистая.
  Достаньте каждую чистую рубашку из корзины 0, затем замочите каждую грязную рубашку в корзине 0.
  Посчитайте, сколько достали и сколько замочили.

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
      std::array<Basket, 2> baskets;
  };
  ```

  Допустим, слоты 0 и 1 корзины 0 хранят грязные рубашки, а слот 2 хранит чистую рубашку.
  Сначала достаем чистые: цикл перебирает слоты по очереди по ссылке
  и очищает каждый слот с чистой вещью, засчитывая 1.
  Затем замачиваем грязные: второй цикл по тем же слотам
  помечает каждую грязную вещь замоченной, засчитывая 2.
  Пустой слот пропускается в обоих циклах.

  ```cpp
  int take_clean_shirts(Basket& basket)
  {
      int taken{ 0 };
      for (auto& slot : basket.slots)
      {
          if (!slot.has_value())
          {
              continue;
          }
          if (slot->state != ClothState::Clean)
          {
              continue;
          }
          slot.reset();
          taken++;
      }
      return taken;
  }

  int soak_basket(Basket& basket)
  {
      int soaked{ 0 };
      for (auto& slot : basket.slots)
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
  laundry.baskets[0].slots[0] = Cloth{
      .label = "shirt",
      .state = ClothState::Dirty,
  };
  int taken{ take_clean_shirts(laundry.baskets[0]) };
  int n{ soak_basket(laundry.baskets[0]) };
  ```
  </details>

- **Тюнинг машины.** Гараж вмещает 4 машины. У каждой машины есть модель, мощность и цена.
  Тюнингуйте машину 2: увеличьте мощность на 10, а цену — на 1000 за каждую добавленную единицу мощности.

- **Мойка машин.** Мойка вмещает 3 машины. Каждая машина бывает чистой или грязной.
  Помойте каждую грязную машину. Посчитайте, сколько было помыто.

- **Парковка.** На парковке 2 этажа по 4 места.
  Каждое место либо хранит машину, либо пусто.
  Поставьте новую машину на первое пустое место. Пройдите по местам с помощью арифметики указателей.

- **Двигатель машины.** В гараже 4 машины. У каждой машины свой двигатель. У двигателя есть износ от 0 до 100.
  Проверьте двигатель через машину 1 и отремонтируйте двигатель машины 1 до износа 0.

- **Рейлинг для чашек.** Рейлинг хранит 4 чашки. Некоторые крючки пусты.
  Повесьте новую чашку на первый пустой крючок и снимите чашку с крючка 1.
  Чашка перемещается с владением: скопируйте ее, затем очистите старое место.

- **Отряд героев.** Отряд вмещает 3 героев. У каждого героя есть здоровье и щит.
  Полечите героя 1 на 20 единиц здоровья. Посчитайте, скольким героям все еще нужно лечение.

- **Активный бафф.** Игрок хранит указатель на активный бафф. Отсутствие баффа означает пустой указатель.
  Дайте игроку 1 бафф на щит до боя и заберите его после боя.

- **Класс.** В комнате 2 ряда по 3 парты. Каждая парта либо хранит ученика, либо пуста.
  Посчитайте пустые парты. Посадите новичка за первую пустую парту.

- **Найти пиццу.** Холодильник вмещает 3 продукта с названиями.
  Найдите пиццу и переместите ее на полку 1 морозилки. Верните признак, была ли она найдена.
  Обращайтесь к полкам через `std::span`.

  <details>
  <summary>
  Возможное решение
  </summary>

  Тот же холодильник и морозилка, что и раньше, но поиск идет через `span` —
  вид на массив полок вместо самого массива.
  Имя то же, что у прошлого `move_food`, но параметры другие (перегрузка):
  что найти и куда положить сгруппированы в отдельную структуру запроса:

  ```cpp
  #include <array>
  #include <optional>
  #include <span>
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

  struct FoodMove
  {
      std::string_view name;
      std::size_t toIndex;
  };
  ```

  Допустим, на полке 1 холодильника лежит пицца, а полка 1 морозилки пуста.
  Вызывающая сторона упаковывает `"pizza"` и `1` в `FoodMove`.
  `span` перебирает слоты полки по очереди: в слоте 0 пиццы нет, поэтому пропускаем его;
  в слоте 1 есть пицца, поэтому копируем ее в морозилку и очищаем старый слот,
  затем сообщаем об успехе через `true`.
  Если ни в одном слоте нет продукта с таким именем, возвращаем `false` и ничего не трогаем:

  ```cpp
  bool move_food(Fridge& fridge, Freezer& to, FoodMove move)
  {
      if (move.toIndex >= to.shelves.size())
      {
          return false;
      }
      if (to.shelves[move.toIndex].has_value())
      {
          return false;
      }
      std::span<std::optional<Food>> shelf{ fridge.shelves };
      for (auto& slot : shelf)
      {
          if (!slot.has_value())
          {
              continue;
          }
          if (slot->name != move.name)
          {
              continue;
          }
          to.shelves[move.toIndex] = slot;
          slot.reset();
          return true;
      }
      return false;
  }
  ```

  Записи через `span` доходят до самого холодильника, потому что `span`
  хранит адрес полок, а не их копию.

  Использование из `main`:
  ```cpp
  Fridge fridge{};
  fridge.shelves[1] = Food{
      .name = "pizza",
  };
  Freezer freezer{};
  bool moved{ move_food(fridge, freezer, FoodMove{
      .name = "pizza",
      .toIndex = 1,
  }) };
  ```
  </details>

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

- **Барбершоп.** В салоне есть место для 4 ожидающих клиентов и 2 мастеров.
  У каждого клиента есть метка и волосы, которые осталось состричь, в минутах.
  Клиенты создаются отдельно в `main`, а салон их только заимствует.
  Добавьте каждого клиента на первое свободное место в очереди.
  Назначьте свободных мастеров ожидающим клиентам.
  Каждый тик каждый занятый мастер состригает 1 минуту.
  Когда клиент полностью пострижен, мастер освобождается.
  Симулируйте через цикл `while`, пока все клиенты не будут обслужены.

  <details>
  <summary>
  Возможное решение
  </summary>

  Клиенты живут в `main`, а салон их только заимствует —
  поэтому и очередь, и мастера хранят указатели, а не копии.
  Стрижка через указатель видна в самом клиенте,
  а один и тот же клиент сначала наблюдается из очереди, затем из мастера.

  ```cpp
  #include <array>
  #include <cassert>
  #include <string_view>

  struct MinutesLeft
  {
      int value;
  };

  struct Client
  {
      std::string_view label;
      MinutesLeft hairCompletion;
  };

  struct Worker
  {
      Client* assignedClient{ nullptr };
  };

  struct Shop
  {
      std::array<Client*, 4> queue{};
      std::array<Worker, 2> workers{};
  };

  enum class AddClientResult
  {
      Added,
      FailedQueueFull,
  };

  enum class TickResult
  {
      Unassigned,
      StillWorking,
      Done,
  };
  ```

  Добавление кладет указатель на первое свободное место в очереди.
  Клиент никогда не должен быть `nullptr`, поэтому это проверяется через assert;
  полная очередь это обычная неудача, о ней сообщается через результат:

  ```cpp
  AddClientResult add_client(Shop& shop, Client* client)
  {
      assert(client != nullptr); // add_client ожидает, что client никогда не nullptr
      for (auto& slot : shop.queue)
      {
          if (slot != nullptr)
          {
              continue;
          }
          slot = client;
          return AddClientResult::Added;
      }
      return AddClientResult::FailedQueueFull;
  }
  ```

  Взятие первого ожидающего клиента это отдельная функция:
  она находит первое занятое место в очереди, очищает его и отдает указатель.
  Назначение просто раздает каждому свободному мастеру то, что вернет эта функция —
  два отдельных цикла, один по мастерам, а внутри второй по очереди.
  Результат `nullptr` просто оставляет мастера свободным:

  ```cpp
  Client* take_first_waiting(Shop& shop)
  {
      for (auto& slot : shop.queue)
      {
          if (slot == nullptr)
          {
              continue;
          }
          Client* found{ slot };
          slot = nullptr;
          return found;
      }
      return nullptr;
  }

  void assign_workers(Shop& shop)
  {
      for (auto& worker : shop.workers)
      {
          if (worker.assignedClient != nullptr)
          {
              continue;
          }
          worker.assignedClient = take_first_waiting(shop);
      }
  }
  ```

  Стрижка пересоздает значение `MinutesLeft` вместо изменения на месте.
  Проверка готовности клиента это тоже отдельная функция:

  ```cpp
  void cut_one_minute(MinutesLeft* minutes)
  {
      assert(minutes != nullptr);
      assert(minutes->value > 0);
      *minutes = MinutesLeft{ minutes->value - 1 };
  }

  bool client_done(const Client& client)
  {
      return client.hairCompletion.value == 0;
  }

  TickResult tick_worker(Worker& worker)
  {
      Client* client{ worker.assignedClient };
      if (client == nullptr)
      {
          return TickResult::Unassigned;
      }
      if (client->hairCompletion.value > 0)
      {
          cut_one_minute(&client->hairCompletion);
      }
      if (client_done(*client))
      {
          worker.assignedClient = nullptr;
          return TickResult::Done;
      }
      return TickResult::StillWorking;
  }

  bool shop_done(const Shop& shop)
  {
      for (const auto& slot : shop.queue)
      {
          if (slot != nullptr)
          {
              return false;
          }
      }
      for (const auto& worker : shop.workers)
      {
          if (worker.assignedClient != nullptr)
          {
              return false;
          }
      }
      return true;
  }
  ```

  Симуляция это обычный цикл `while`: назначить, затем тикнуть каждого мастера, пока все не готово.
  Клиенты должны пережить салон, потому что салон их никогда не копирует:

  ```cpp
  int main()
  {
      Client alice{
          .label = "alice",
          .hairCompletion = { 2 },
      };
      Client bob{
          .label = "bob",
          .hairCompletion = { 3 },
      };

      Shop shop{};
      add_client(shop, &alice);
      add_client(shop, &bob);

      while (!shop_done(shop))
      {
          assign_workers(shop);
          for (auto& worker : shop.workers)
          {
              tick_worker(worker);
          }
      }
  }
  ```
  </details>

- **Дроны-барберы.** Работники теперь дроны-автоматы:
  несколько дронов могут обрабатывать одного клиента одновременно,
  каждый состригает по 1 минуте за тик.
  Когда клиент полностью пострижен, освобождается каждый дрон на нем.
  Симулируйте, пока все клиенты не будут обслужены.

  <details>
  <summary>
  Возможное решение
  </summary>

  Заберите структуры, `add_client`, `take_first_waiting`, `cut_one_minute`,
  `client_done` и `shop_done` из прошлой задачи как есть —
  меняются только правила.
  Клиент больше не эксклюзивен: свободный дрон, которому некого ждать,
  помогает тому, кого уже стригут.
  Совместная работа безопасна, потому что каждый дрон стрижет через указатель в одного клиента.

  Поиск первого уже обслуживаемого клиента это отдельная функция,
  рядом с `take_first_waiting`:

  ```cpp
  Client* first_busy_client(Shop& shop)
  {
      for (auto& worker : shop.workers)
      {
          if (worker.assignedClient != nullptr)
          {
              return worker.assignedClient;
          }
      }
      return nullptr;
  }

  void assign_drones(Shop& shop)
  {
      for (auto& worker : shop.workers)
      {
          if (worker.assignedClient != nullptr)
          {
              continue;
          }
          Client* next{ take_first_waiting(shop) };
          if (next == nullptr)
          {
              next = first_busy_client(shop);
          }
          worker.assignedClient = next; // остается свободным, когда вообще некого стричь
      }
  }
  ```

  Тик одного дрона не меняется; тик салона сначала стрижет всеми дронами,
  и только потом отпускает готовых — сразу со всех дронов.
  Стричь дважды за тик в этом и смысл,
  а проверка `value > 0` не дает общей последней минуте уйти в минус:

  ```cpp
  TickResult tick_drone(Worker& worker)
  {
      Client* client{ worker.assignedClient };
      if (client == nullptr)
      {
          return TickResult::Unassigned;
      }
      if (client->hairCompletion.value > 0)
      {
          cut_one_minute(&client->hairCompletion);
      }
      if (client_done(*client))
      {
          return TickResult::Done;
      }
      return TickResult::StillWorking;
  }

  void release_client(Shop& shop, Client* client)
  {
      assert(client != nullptr);
      for (auto& worker : shop.workers)
      {
          if (worker.assignedClient == client)
          {
              worker.assignedClient = nullptr;
          }
      }
  }

  void tick_shop(Shop& shop)
  {
      for (auto& worker : shop.workers)
      {
          tick_drone(worker);
      }
      for (auto& worker : shop.workers)
      {
          Client* client{ worker.assignedClient };
          if (client != nullptr && client_done(*client))
          {
              release_client(shop, client);
          }
      }
  }
  ```

  Допустим, alice нужно 4 минуты и ее взяли оба дрона:
  тик 1 стрижет дважды (с 4 до 2), тик 2 стрижет дважды (с 2 до 0),
  оба дрона сообщают `Done` и освобождаются вместе:

  ```cpp
  int main()
  {
      Client alice{
          .label = "alice",
          .hairCompletion = { 4 },
      };
      Client bob{
          .label = "bob",
          .hairCompletion = { 2 },
      };

      Shop shop{};
      add_client(shop, &alice);
      add_client(shop, &bob);

      while (!shop_done(shop))
      {
          assign_drones(shop);
          tick_shop(shop);
      }
  }
  ```
  </details>

- **Парк аттракционов.** В парке 3 аттракциона и очередь на 4 посетителя.
  Каждый посетитель ранжирует все 3 аттракциона по желанию, помнит последний посещенный
  и может посетить всего не больше 3 аттракционов.
  Каждый тик обслуженные посетители возвращаются в очередь —
  или покидают парк, когда квота исчерпана —
  а ожидающие занимают первый свободный аттракцион из своих предпочтений,
  кроме того, с которого только что сошли.
  Симулируйте, пока все не исчерпают квоту.

  <details>
  <summary>
  Возможное решение
  </summary>

  Здесь тоже никто никем не владеет: аттракционы, посетители и парк
  все живут в `main`, а каждая связь между ними это указатель.
  Аттракционы указывают на текущих посетителей (занятость меняется каждый тик,
  поэтому копия протухла бы в момент, когда кого-то отпускают),
  а посетители указывают на желанные аттракционы (стабильные желания,
  заданные раз в `main`) плюс на последний посещенный.
  Отпустить кого-то значит указать в другое место:
  обратно в очередь поиска или в никуда, когда квота исчерпана.

  ```cpp
  #include <array>
  #include <cassert>
  #include <string_view>

  struct Visitor; // аттракцион лишь заимствует occupant

  struct Attraction
  {
      std::string_view name;
      Visitor* occupant{ nullptr };
  };

  struct Visitor
  {
      std::string_view label;
      std::array<Attraction*, 3> preferences; // сначала самый желанный, каждый по разу
      Attraction* last{ nullptr };
      int visitsDone{ 0 };
  };

  struct Park
  {
      std::array<Attraction*, 3> attractions;
      std::array<Visitor*, 4> waiting{};
  };

  constexpr int MAX_VISITS{ 3 };

  enum class AddVisitorResult
  {
      Added,
      WaitingFull,
  };
  ```

  Добавление в очередь повторяет очередь салона.
  Посетитель никогда не должен быть `nullptr`, поэтому это проверяется через assert;
  полная очередь сообщается через результат:

  ```cpp
  AddVisitorResult add_visitor(Park& park, Visitor* visitor)
  {
      assert(visitor != nullptr); // add_visitor ожидает, что visitor никогда не nullptr
      for (auto& slot : park.waiting)
      {
          if (slot != nullptr)
          {
              continue;
          }
          slot = visitor;
          return AddVisitorResult::Added;
      }
      return AddVisitorResult::WaitingFull;
  }
  ```

  Выбор это отдельная функция: первое предпочтение, которое свободно
  и не является тем, с которого только что сошли.
  Предпочтения задаются в `main` и всегда валидны, поэтому null там проверяется через assert:

  ```cpp
  Attraction* first_free_choice(Visitor& visitor)
  {
      for (Attraction* choice : visitor.preferences)
      {
          assert(choice != nullptr);
          if (choice == visitor.last)
          {
              continue;
          }
          if (choice->occupant != nullptr)
          {
              continue;
          }
          return choice;
      }
      return nullptr;
  }

  void board_visitors(Park& park)
  {
      for (auto& slot : park.waiting)
      {
          Visitor* visitor{ slot };
          if (visitor == nullptr)
          {
              continue;
          }
          Attraction* choice{ first_free_choice(*visitor) };
          if (choice == nullptr)
          {
              continue; // все желанное занято: ждем дальше
          }
          choice->occupant = visitor;
          visitor->last = choice;
          slot = nullptr;
      }
  }
  ```

  Один тик завершает каждую идущую поездку — визит длится ровно один тик —
  затем рассаживает ожидающих.
  Обслуженный посетитель с остатком квоты возвращается в очередь;
  тот, чья квота исчерпана, просто уходит (его указатель выбрасывается).
  Возврат не может переполнить очередь:
  возвращается не больше посетителей, чем каталось:

  ```cpp
  void finish_rides(Park& park)
  {
      for (Attraction* attraction : park.attractions)
      {
          assert(attraction != nullptr);
          Visitor* visitor{ attraction->occupant };
          if (visitor == nullptr)
          {
              continue;
          }
          visitor->visitsDone++;
          attraction->occupant = nullptr;
          if (visitor->visitsDone >= MAX_VISITS)
          {
              continue; // квота исчерпана: из парка
          }
          AddVisitorResult back{ add_visitor(park, visitor) };
          assert(back == AddVisitorResult::Added);
      }
  }

  bool park_done(const Park& park)
  {
      for (const Attraction* attraction : park.attractions)
      {
          assert(attraction != nullptr);
          if (attraction->occupant != nullptr)
          {
              return false;
          }
      }
      for (const Visitor* visitor : park.waiting)
      {
          if (visitor != nullptr)
          {
              return false;
          }
      }
      return true;
  }
  ```

  Допустим, alice хочет сначала горку, а bob сначала колесо:
  тик 1 рассаживает обоих (каждый получает любимое),
  тик 2 завершает обе поездки (каждому засчитывается по визиту) и рассаживает снова —
  в этот раз каждый берет свободное мимо того, с которого только что сошел:

  ```cpp
  int main()
  {
      Attraction coaster{ .name = "coaster" };
      Attraction wheel{ .name = "wheel" };
      Attraction slides{ .name = "slides" };

      Visitor alice{
          .label = "alice",
          .preferences = { &coaster, &wheel, &slides },
          .last = nullptr,
          .visitsDone = 0,
      };
      Visitor bob{
          .label = "bob",
          .preferences = { &wheel, &coaster, &slides },
          .last = nullptr,
          .visitsDone = 0,
      };

      Park park{
          .attractions = { &coaster, &wheel, &slides },
      };
      add_visitor(park, &alice);
      add_visitor(park, &bob);

      while (!park_done(park))
      {
          finish_rides(park);
          board_visitors(park);
      }
  }
  ```
  </details>

- **Объятия в семье.** В семье 5 человек.
  Каждый хочет обнять каждого другого ровно один раз.
  Каждый человек хранит указатели на тех, кого уже обнял.
  Обнимите всех и посчитайте объятия.

  <details>
  <summary>
  Возможное решение
  </summary>

  Пять человек значит по четыре объятия на каждого, то есть всего десять пар (5 * 4 / 2).
  Заметьте, что для объятия вообще не нужен контейнер:
  достаточно двух людей и их списков указателей,
  потому что указатель уже точно говорит, кого обняли:

  ```cpp
  #include <array>
  #include <cassert>
  #include <string_view>

  struct Person
  {
      std::string_view name;
      std::array<Person*, 4> hugged{};
      int hugCount{ 0 };
  };

  bool has_hugged(const Person& person, const Person* other)
  {
      assert(other != nullptr);
      for (const Person* hugged : person.hugged)
      {
          if (hugged == other)
          {
              return true;
          }
      }
      return false;
  }

  bool hug(Person& a, Person& b)
  {
      assert(&a != &b);
      if (has_hugged(a, &b))
      {
          return false; // уже обнимались: ничего нового
      }
      assert(a.hugCount < 4 && b.hugCount < 4);
      a.hugged[a.hugCount] = &b;
      a.hugCount++;
      b.hugged[b.hugCount] = &a;
      b.hugCount++;
      return true;
  }

  bool all_hugged(const std::array<Person, 5>& family)
  {
      for (const Person& person : family)
      {
          if (person.hugCount < 4)
          {
              return false;
          }
      }
      return true;
  }
  ```

  Спаривание каждого `i` с каждым последующим `j` проходит каждую пару ровно раз.
  Массив семьи никуда не двигается, поэтому сохраненные указатели остаются валидны:

  ```cpp
  int main()
  {
      std::array<Person, 5> family{
          Person{ .name = "ann" },
          Person{ .name = "bob" },
          Person{ .name = "cid" },
          Person{ .name = "dan" },
          Person{ .name = "eva" },
      };
      int hugs{ 0 };
      for (int i = 0; i < 5; i++)
      {
          for (int j = i + 1; j < 5; j++)
          {
              if (hug(family[i], family[j]))
              {
                  hugs++;
              }
          }
      }
      assert(all_hugged(family));
      assert(hugs == 10);
  }
  ```
  </details>

- **Объятия в семье по индексам.** Те же 5 человек,
  но каждый хранит индексы обнятых (`std::array<int, 4>`) вместо указателей —
  теперь объятия имеют смысл только вместе с массивом семьи, в который указывают индексы.
  Обнимите всех по разу и посчитайте объятия.

- **Объятия в семье с битовым множеством.** Те же 5 человек,
  но каждый хранит `std::bitset<5>` обнятых.
  (Да, в C++ есть стандартное битовое множество: `<bitset>`.)
  Обнимите всех по разу и посчитайте объятия.

  <details>
  <summary>
  Возможное решение
  </summary>

  Бит `i` значит "обнял члена `i`".
  Свой бит никогда не ставится, поэтому у полностью обнявшегося 4 бита из 5.
  Те же десять пар, что и раньше, — меняется только хранение:

  ```cpp
  #include <array>
  #include <bitset>
  #include <cassert>
  #include <string_view>

  struct Person
  {
      std::string_view name;
      std::bitset<5> hugged{};
  };

  bool hug(std::array<Person, 5>& family, int i, int j)
  {
      assert(i != j);
      assert(i >= 0 && i < 5 && j >= 0 && j < 5);
      if (family[i].hugged.test(j))
      {
          return false; // уже обнимались: ничего нового
      }
      family[i].hugged.set(j);
      family[j].hugged.set(i);
      return true;
  }

  bool all_hugged(const std::array<Person, 5>& family)
  {
      for (const Person& person : family)
      {
          if (person.hugged.count() < 4) // все, кроме себя
          {
              return false;
          }
      }
      return true;
  }
  ```

  Использование из `main`:
  ```cpp
  int main()
  {
      std::array<Person, 5> family{
          Person{ .name = "ann" },
          Person{ .name = "bob" },
          Person{ .name = "cid" },
          Person{ .name = "dan" },
          Person{ .name = "eva" },
      };
      int hugs{ 0 };
      for (int i = 0; i < 5; i++)
      {
          for (int j = i + 1; j < 5; j++)
          {
              if (hug(family, i, j))
              {
                  hugs++;
              }
          }
      }
      assert(all_hugged(family));
      assert(hugs == 10);
  }
  ```
  </details>
