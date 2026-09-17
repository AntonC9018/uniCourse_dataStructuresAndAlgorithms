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
  Putting the Atlas at slot 2 has to pass two checks:
  2 is inside the array, slot 2 has no value —
  only then store the book and report success.
  The shelf itself is not checked: the function expects it to never be null.
  At slot 0 the last check fails, so refuse with `false` and touch nothing:

  ```cpp
  #include <cassert>

  bool shelve_book(Bookshelf* shelf, std::size_t index, Book book)
  {
      assert(shelf != nullptr); // shelve_book expects shelf to never be null
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

  A reference cannot be null, so taking the shelf by `&` instead of by `*`
  enforces that it is never null. The rest of the examples use references for this reason.

  Taking a book is mirrored: slot 0 has a book, so clear it with `reset()`
  and return `true`; an empty slot refuses:

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
  take_book(shelf, 0);
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
  both indices are inside,
  the source has food, the target is free.
  Then two steps: copy the food into freezer shelf 0,
  clear fridge shelf 1 with `reset()`.
  From then on the pizza lives in exactly one place —
  that is the whole ownership idea.
  Any failed check returns `false` and nothing is touched:

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

  Usage from `main`:
  ```cpp
  Fridge fridge{};
  fridge.shelves[1] = Food{ .name = "pizza" };
  Freezer freezer{};
  bool moved{ move_food(fridge, 1, freezer, 0) };
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

  Heating finds a meal inside, so flip its warmth to hot.
  Heating an empty microwave finds nothing and returns `false`:

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

  Taking out copies the hot soup for the caller,
  clears the tray, and returns the copy:

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

  Usage from `main`:
  ```cpp
  Microwave mw{};
  put_meal(mw, Meal{ .name = "soup", .warmth = Warmth::Cold });
  heat_meal(mw);
  std::optional<Meal> lunch{ take_meal(mw) };
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
  the `switch` sees `Red`, adds 20 health,
  and returns `true` — the hero is now at 70.
  A blue potion would take the next branch and add 10 shield instead.
  A spoiled potion takes the last branch and returns `false`
  without touching the hero:

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

  Usage from `main`:
  ```cpp
  Hero hero{ .health = 50, .shield = 0 };
  drink_potion(hero, Potion{ .kind = PotionKind::Red });
  ```
  </details>

- **Soak laundry.** A basket holds 3 pieces of clothing.
  A laundry has 2 baskets.
  Each piece has a label and is dirty, soaked, or clean.
  Take out every clean shirt from basket 0, then soak every dirty shirt in basket 0.
  Count how many were taken and how many were soaked.

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
      std::array<Basket, 2> baskets;
  };
  ```

  Say slots 0 and 1 of basket 0 hold dirty shirts and slot 2 holds a clean shirt.
  First take out the clean ones: the loop borrows each slot in turn
  and clears every slot that holds a clean piece, counting 1.
  Then soak the dirty ones: a second loop over the same slots
  marks every dirty piece soaked, counting 2.
  An empty slot is skipped in both loops.

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

  Usage from `main`:
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

- **Tune car.** A garage holds 4 cars. Each car has a model, power, and price.
  Tune car 2: add 10 power, add 1000 to the price for each added power.

- **Wash cars.** A car wash holds 3 cars. Each car is clean or dirty.
  Wash every dirty car. Count how many were washed.

- **Parking lot.** A parking lot has 2 floors with 4 spots each.
  Each spot holds a car or is empty.
  Put the new car on the first empty spot. Walk the spots with pointer arithmetic.

- **Car engine.** A garage holds 4 cars. Each car has its own engine. The engine has wear from 0 to 100.
  Check the engine through car 1 and repair the engine of car 1 to wear 0.

- **Cup rail.** A rail holds 4 cups. Some hooks are empty.
  Put a new cup on the first empty hook and take the cup from hook 1.
  The cup moves with ownership: copy it over, then clear the old spot.

- **Hero party.** A squad holds 3 heroes. Each hero has health and shield.
  Heal hero 1 by 20. Count how many heroes still need healing.

- **Active buff.** A player holds a pointer to the active buff. No buff means an empty pointer.
  Give the player 1 shield buff before the fight and take it away after.

- **Classroom.** A room has 2 rows with 3 desks each. Each desk holds a pupil or is empty.
  Count empty desks. Seat the newcomer at the first empty desk.

- **Find pizza.** A fridge holds 3 foods with names.
  Find the pizza and move it to freezer shelf 1. Return if it was found.
  Look at the shelves through a span.

  <details>
  <summary>
  Possible solution
  </summary>

  Same fridge and freezer as before, but the search goes through a `span` —
  a view over the shelves array instead of the array itself.
  Same name as the earlier `move_food`, but different parameters (an overload):
  what to find and where to put it are grouped into their own request struct:

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

  Say fridge shelf 1 holds the pizza and freezer shelf 1 is free.
  The caller packs `"pizza"` and `1` into a `FoodMove`.
  The `span` borrows each shelf slot in turn: slot 0 has no pizza, so skip it;
  slot 1 has the pizza, so copy it into the freezer and clear the old slot,
  then report success with `true`.
  If no slot holds a food with that name, report `false` and touch nothing:

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

  Writes through the span reach the fridge itself, because the span
  stores the address of the shelves, not a copy of them.

  Usage from `main`:
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

- **Barbershop.** A shop has room for 4 waiting clients and 2 workers.
  Each client has a label and hair left to cut, in minutes.
  Clients are created separately in `main` and only referenced by the shop.
  Add each client to the first free spot in the queue.
  Assign idle workers to waiting clients.
  Each tick every busy worker cuts 1 minute.
  When a client is fully cut, the worker becomes free.
  Simulate with a `while` loop until all clients are done.

  <details>
  <summary>
  Possible solution
  </summary>

  Clients live in `main`, the shop only borrows them —
  that is why both the queue and the workers store pointers, not copies.
  A cut through a pointer is visible in the client itself,
  and the same client is first referenced from the queue, then from a worker.

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

  Adding puts the pointer into the first free queue spot.
  The client must never be `nullptr`, so it is enforced with an assert;
  a full queue is a normal failure reported through the result:

  ```cpp
  AddClientResult add_client(Shop& shop, Client* client)
  {
      assert(client != nullptr); // add_client expects client to never be null
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

  Taking the first waiting client is its own function:
  it finds the first taken queue spot, clears it, and hands the pointer over.
  Assigning then just gives every idle worker whatever that function returns —
  two separate loops, one over the workers and one over the queue inside.
  A `nullptr` result simply leaves the worker idle:

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

  Cutting recreates the `MinutesLeft` value instead of mutating it in place.
  Whether the client is done is its own function too:

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

  The simulation is a plain `while` loop: assign, then tick every worker, until done.
  Clients must outlive the shop, because the shop never copies them:

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
