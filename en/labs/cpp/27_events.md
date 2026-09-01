# Polymorphism

- [My notes with examples](../../../en/05a_programming_fundamentals/11_polymorphism.md)

## Event system

1. Implement a simple event system.
   The interface should be as follows:

* An `EventSystem` structure that stores a list of event handlers
  for each event type.

* An `EventHandler` structure that stores a handler identifier (a number)
  and the handler function itself.

* Define the handler function type `EventHandlerFunc` with `using`.
  It can be one of the following; choose whichever you prefer:

  - A function pointer, but in that case be aware that you will not be able to preserve context with it.

  - `std::function`. In my opinion, this is the simplest yet still flexible option.

  - `EventHandlerAbstractBase*`, where `EventHandlerAbstractBase` is an abstract base class
    that declares the virtual function `handleEvent(EventInfo* event)`.
    This will let you preserve context in derived classes.
    In this case, do not forget to delete the handler when unsubscribing.

    ```cpp
    class EventHandlerAbstractBase
    {
    public:
        virtual void handleEvent(EventInfo* event) = 0;
    };

    class MyHandler : public HandlerAbstractBase
    {
        MyContext* context;

    public:
        void handleEvent(EventInfo* event) override
        {
            // ...
        }
    };
    ```

* An `EventHandle` structure that stores an event identifier (a number).

* An `EventInfo` structure that will be passed to event handlers.
  You may decide exactly what data to pass and how:

  - You can use type erasure by storing a `void*` pointing to additional data
    and casting it to the required type in the handlers.

    ```cpp
    struct EventInfo
    {
        void* context;

        // ...
    };

    // ...

    void handleEvent(EventInfo* event)
    {
        auto context = static_cast<MyContext*>(event->context);
        // ...
    }
    ```

  - You can simply use some fixed, generic data, but then you will probably not be able
    to pass more specific context when handling the event.

    ```cpp
    struct EventInfo
    {
        int someData1;
        int someData2;
    };

    void handleEvent(EventInfo* event)
    {
        std::cout << event->someData1 << std::endl;
    }
    ```

  - You can add a `template` parameter to this structure for the payload type.
    This is the most complex option, which will also require you to add templates
    to `EventSystem` itself, but it is also the most flexible.

    ```cpp
    template<typename Payload>
    struct EventInfo
    {
        Payload payload;

        // ... some more generic info
    };

    template<typename Payload>
    void dispatchEvent(
        EventSystem& eventSystem,
        size_t eventId,
        EventInfo<Payload>* event)
    {
        std::span<EventHandler<Payload>> handlers = getEventHandlersById<Payload>(eventSystem, eventId);
        for (const auto& handler : handlers)
        {
            handler.func(event);
        }
    }
    ```

* A function `EventHandle createEvent(EventSystem& eventSystem)`
  or `EventHandle<T> createEvent(EventSystem& eventSystem)`.

  It returns an event identifier that can be used
  to subscribe handlers later.
  Each subsequent identifier should be 1 greater than the previous one.

  To simplify debugging, you can store the event name in `EventSystem`.
  You can also use an `std::unordered_map` with user-provided strings
  as event identifiers.

* A function `EventHandlerHandle subscribe(EventSystem& eventSystem, EventHandle eventId, EventHandlerFunc&& func);`,
  which adds a handler to the specified event.
  It returns an `EventHandlerHandle` structure containing a handler identifier,
  which can be used for unsubscribing.
  Each subsequent identifier should be 1 greater than the previous one.

* A function `bool unsubscribe(EventSystem& eventSystem, EventHandle eventId, EventHandlerHandle handle);`,
  which removes the handler with the specified identifier
  from the specified event (you may assume that handlers cannot unsubscribe other handlers).
  It returns `false` if the handler was not found.

* A function `void dispatch(EventSystem& eventSystem, EventHandle eventId, EventInfo* event);`,
  which calls all handlers for the event with the specified identifier.


2. Create a menu that demonstrates its use.
   The menu must have the following options:

   * Create a new event, initially without subscriptions.
     If you chose the `template` option,
     the user must be able to select a `Payload` type
     from known types (at least 2).

   * Subscribe one of the predefined handlers to a specific event.
     The user must be able to choose one of several functions
     defined beforehand in the program (at least 6).
     If a function expects additional context, let the user enter it before binding the function
     (for example, the function “add N to the number in the payload” expects a number N).
    
   * Unsubscribe a handler by providing the event and handler identifiers.

   * Print the identifiers of all events and their handlers.

   * Invoke an event by providing its identifier
     and, if needed, data for the handlers.


3. Possible ideas for events and handlers:

- An event for applying filters when selecting a color.
  Handlers that combine, override, or transform the color
  passed in the event context.
  Finally, print the selected color after processing.

- A mathematical pipeline for numbers.
  Handlers that add to, multiply, or take the square root of the number
  passed in the event context.

- Events in the context of a game.
  You can imagine that one event is invoked when a player presses a button.
  Its effect could be a monetary bonus awarded to the player at random,
  a dynamite explosion and the player's death, an increase in score, etc.

Any ideas are welcome.

**Do not use global variables!**
