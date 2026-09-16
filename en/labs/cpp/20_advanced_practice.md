---
slug: en/cpp/labs/advanced-practice
---
<!-- course-site-backlink:start -->
[This lesson on the website](https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms/en/cpp/labs/advanced-practice/)
<!-- course-site-backlink:end -->
# Advanced Practice

> This is a continuation of [Practice with Simple Problems](09_basic_practice.md).

## What you will develop in this assignment

- More advanced domain modeling;
- Storing a fixed number of items in `std::array`, including an array inside a struct;
- Using `std::optional`;
- The idea of ownership;
- Naming things with `std::string_view`;
- Changing objects through pointers and references, reading them through `const` references and `std::span`;
- Writing small functions that return `bool` or a count, using `if` with guard clauses and `switch` on `enum`;
- Looping over objects, counting empty places, finding the first empty place.

## Tools you'll need

- `std::string_view` kind of represents a constant string.
  Use it for titles and names.

  Minimal example:
  ```cpp
  std::string_view s{ "Hello, world!" };
  std::cout << s << std::endl;
  ```

- `std::optional<T>` either holds a `T` or is empty.

  Minimal example:
  ```cpp
  std::optional<int> slot{ std::nullopt };
  slot = 42;
  bool taken{ slot.has_value() };
  slot.reset();
  ```

## Practice tasks

- **Bookshelf.** A shelf holds 5 books. Each book has a title.
  Put the Atlas at shelf 2 and remove the book from shelf 0.
  Count how many shelves are empty.

  <details>
  <summary>
  Possible solution
  </summary>

  A shelf slot either holds a book or is empty, so the slot type is
  `std::optional<Book>` — an empty shelf is `std::nullopt`.
  The structs themselves are just grouping, as in the previous lab:

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

  Say slots 0 and 3 hold books and the rest are empty.
  Putting the Atlas at slot 2 has to pass three checks:
  the pointer is set, 2 is inside the array, slot 2 has no value —
  only then store the book and report success.
  At slot 0 the last check fails, so refuse with `false` and touch nothing:

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

  Taking a book is mirrored: slot 0 has a book, so clear it with `reset()`
  and return `true`; an empty slot refuses:

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

  Counting empties just visits each slot in turn with a range-based `for`
  and adds 1 for each slot without a value:

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

  Usage from `main`:
  ```cpp
  Bookshelf shelf{};
  shelve_book(&shelf, 2, Book{ .title = "Atlas" });
  take_book(&shelf, 0);
  int free{ empty_count(shelf) };
  ```
  </details>

- **Fridge to freezer.** A fridge holds 3 foods, a freezer holds 2 foods.
  Each food has a name.
  Move the pizza from fridge shelf 1 to freezer shelf 0.
  The old place becomes empty.

  <details>
  <summary>
  Possible solution
  </summary>

  Same shelf idea, two containers: the fridge has 3 shelves, the freezer 2,
  each slot either holds food or is empty:

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

  Say fridge shelf 1 holds the pizza and freezer shelf 0 is empty.
  Moving it goes down the checks:
  both pointers are set, both indices are inside,
  the source has food, the target is free.
  Then two steps: copy the food into freezer shelf 0,
  clear fridge shelf 1 with `reset()`.
  From then on the pizza lives in exactly one place —
  that is the whole ownership idea.
  Any failed check returns `false` and nothing is touched:

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

  Usage from `main`:
  ```cpp
  Fridge fridge{};
  fridge.shelves[1] = Food{ .name = "pizza" };
  Freezer freezer{};
  bool moved{ move_food(&fridge, 1, &freezer, 0) };
  ```
  </details>

- **Heat soup.** A microwave holds one meal or is empty.
  Each meal has a name and warmth: cold or hot.
  Put the cold soup in, heat it to hot, then take it out.

  <details>
  <summary>
  Possible solution
  </summary>

  Here there is only one slot — the tray — plus a new thing to track:
  warmth, which is either cold or hot:

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

  The tray starts empty. Putting the cold soup in finds a free tray,
  so store the meal and return `true`;
  a second put would find a busy tray and refuse:

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

  Heating finds a meal inside, so flip its warmth to hot.
  Heating an empty microwave finds nothing and returns `false`:

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

  Taking out copies the hot soup for the caller,
  clears the tray, and returns the copy:

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

  Usage from `main`:
  ```cpp
  Microwave mw{};
  put_meal(&mw, Meal{ .name = "soup", .warmth = Warmth::Cold });
  heat_meal(&mw);
  std::optional<Meal> lunch{ take_meal(&mw) };
  ```
  </details>

- **Drink potion.** A hero has health and shield.
  A potion is red, blue, or spoiled.
  Give the hero 1 red potion.
  Red adds 20 health, blue adds 10 shield, spoiled does nothing.

  <details>
  <summary>
  Possible solution
  </summary>

  The potion kind decides the effect, so it becomes an `enum`.
  Hero and potion are plain grouping:

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

  Walk through a red potion on a hero with 50 health and 0 shield:
  the pointer is set, the `switch` sees `Red`, adds 20 health,
  and returns `true` — the hero is now at 70.
  A blue potion would take the next branch and add 10 shield instead.
  A spoiled potion takes the last branch and returns `false`
  without touching the hero:

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

  Usage from `main`:
  ```cpp
  Hero hero{ .health = 50, .shield = 0 };
  drink_potion(&hero, Potion{ .kind = PotionKind::Red });
  ```
  </details>

- **Soak laundry.** A basket holds 3 pieces of clothing.
  A laundry has 2 baskets.
  Each piece has a label and is dirty, soaked, or clean.
  Soak every dirty shirt in basket 0. Count how many were soaked.

  <details>
  <summary>
  Possible solution
  </summary>

  The new shape here is nesting: a `Basket` holds an array,
  a `Laundry` holds baskets:

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

  Say slots 0 and 1 of basket 0 hold dirty shirts and slot 2 is empty.
  The loop borrows each slot in turn (`auto&`, see the references lab):
  slot 0 is dirty, so mark it soaked and count 1;
  slot 1 is dirty, so mark it soaked and count 2;
  slot 2 is empty, so skip it.
  The function returns 2:

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

  Usage from `main`:
  ```cpp
  Laundry laundry{};
  laundry.tubs[0].slots[0] = Cloth{ .label = "shirt", .state = ClothState::Dirty };
  int n{ soak_basket(&laundry.tubs[0]) };
  ```
  </details>

- **Tune car.** A garage holds 4 cars. Each car has a model, power, and price.
  Tune car 2: add 10 power, add 1000 to the price for each added power.

- **Wash cars.** A car wash holds 3 cars. Each car is clean or dirty.
  Wash every dirty car. Count how many were washed.

- **Parking lot.** A parking lot has 2 floors with 4 spots each.
  Each spot holds a car or is empty.
  Put the new car on the first empty spot. Walk the spots with pointer arithmetic.

- **Car engine.** A car holds a pointer to its engine. The engine has wear 0 to 100.
  No engine means an empty pointer.
  Check the engine through the car and repair the engine of car 1 to 0.

- **Cup rail.** A rail holds pointers to 4 cups. Some hooks are empty.
  Put a new cup on the first empty hook and take the cup from hook 1.
  The pointer moves with the cup.

- **Hero party.** A squad holds 3 heroes. Each hero has health and shield.
  Heal hero 1 by 20. Count how many heroes still need healing.

- **Active buff.** A player holds a pointer to the active buff. No buff means an empty pointer.
  Give the player 1 shield buff before the fight and take it away after.

- **Classroom.** A room has 2 rows with 3 desks each. Each desk holds a pupil or is empty.
  Count empty desks. Seat the newcomer at the first empty desk.

- **Find pizza.** A fridge holds 3 foods with names.
  Find the pizza and move it to freezer shelf 1. Return if it was found.
  Look at the shelves through a span.

- **Soak dishes.** A kitchen has 2 racks with 3 plates each. Each plate is dirty or soaked.
  Soak every dirty plate in rack 0.

- **Library rooms.** A library has 2 rooms with 3 slots each. Each slot holds a book or is empty.
  Put the Atlas in the first empty slot of room 1.

- **Traffic light.** A crossing has 3 lights. Each light is red, yellow, or green.
  Step light 2 to the next color with switch.

- **Medicine cabinet.** A cabinet holds 4 boxes. Each box is fresh or expired.
  Return if box 1 can be used. Throw box 1 away if expired.

- **Canteen.** A canteen holds 3 soups and 3 breads.
  Serve soup 1 with bread 1. The serving takes both out.

- **Hot chain.** A kitchen has a fridge, a freezer, and a microwave.
  Put the pizza from fridge shelf 0 into the microwave, heat it,
  then move it to freezer shelf 1. Each step returns if it worked.
