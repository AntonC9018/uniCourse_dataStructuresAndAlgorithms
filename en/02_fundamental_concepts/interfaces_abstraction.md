# Fundamental concepts in programming: interfaces and abstraction

## Interface

An **interface** is a general term which represents how one can interact with a **system**, or how different systems can interact with each other.

### Example: computer system

<!-- diagram here -->

For example, take computers.
The user perceives the fact that a computer, which represents the computer system, can function as magical, which is to say, they don't know or care how it works.
They use the keyboard and mouse to send signals to the computer, and look at the computer screen to view responses from the system
(e.g. clicking the mouse button opens a program, 
while typing on the keyboard translates the key presses into the text editor software).
These two components, namely the input and the output, represent the interface of a computer system.
The user may very well be completely oblivious to the inner workings of the computer system, 
they might not even be aware of its existence, because all they ever interact with is its interface.
In other words, the system can be treated as a **black box**.

To be clear, the computer system is never considered part of the interface, 
the interface of a computer is comprised of just the input and the output devices, 
which help the user to interact with the computer system.
Anything used to interact with the computer is considered part of its interface, 
even USB ports on the computer box, or the power switch.

In general terms, the user of a system that does actions is often called an **actor**, 
while the details of the system in question are often referred to as the **implementation**, 
especially in programming contexts.

These terms are often used in the design of software systems.

### Example: video game

<!-- diagram here -->

Let's take another example -- a video game.
It's common and good practice to separate the game components into the underlying game logic part, 
the user input part, and the **view** part, which includes stuff like graphics and sound effects.

The **view** is what the user would see on the screen, aka the character animations, buttons, damage numbers, etc. 
It effectively represents the output component of the game system.

The user input part, often named **controller**, is the part of the system responsible for converting user input,
like clicking buttons on the screen or keys on the keyboard, 
into commands that can be interpreted by the game logic, 
like moving the character, or zooming the camera, or using an ability.
It effectively represents the input component of the game system.

The game logic part, also named **model**, applies the commands from the controller and displays the results via the view to the user.
It represents the implementation of the game system.

So the interface of a game consists of the controller and the view.

> Now, strictly speaking it's not entirely true, because the actual part facing the user in the view is not the whole view,
> it might very well have a lot of other logic, not visible to the user, that e.g. help to set up the widgets
> on the screen.
> 
> Same with the controller, it's not just the input handling, it might also have some logic that helps it to interpret,
> preprocess or transform the input, before passing it to the game logic.

### Breaking the system down into individual parts

The difference between an interface and a **user interface** is that the latter is designed specifically
for interaction with humans, while simply an interface is a more general thing.
It's possible for one interface to interact with another.

For example, a keyboard has its own interface.
A keyboard has an input part (the physical keys), 
the implementation or the **"black box"** system part (how key presses are converted into electric waves) 
and the output part (the wire that connects to the computer).
The input and the output parts make up the interface of a keyboard.
The input is manipulated by humans, while the output is interpreted by the computer.
An observation is that in an interface, the actor is not necessarily the **observer** of the effects.
In case of computers, the effect eventually reaches the actor via the graphical interface,
but in the scope of a keyboard it's not necessarily the case.

Likewise, a computer screen has its own interface.
It's got the actual screen that's visible to the user,
it's got the input wire that receives signals from the computer,
and it's got some system that knows which LEDs to light up.
In this case, the actor of this system is the computer,
while the observer is the person looking at the screen.

Any part of e.g. the computer is its own little system and has its own little interface.
One of the reasons this is done this way is to enable any part to be substituted for any other compatible part,
making the entire system highly **modular** and flexible.
Being compatible can be defined as having the same interface, but potentially a completely different implementation.
For example, you can connect any keyboard or any screen to a computer, as long as it has a kind of wire that the *output* (screen) or *input* (keyboard) *interface* of a computer supports.

The second benefit of interfaces is that they allow part designers to **implement** the parts in isolation,
as long as these parts comply with the interface specification that the part **consumers** 
(the interfaces that will allow connection to these parts / use them) require.

To sum up, interfaces are the outward facing components of things.
They enable connecting multiple components via their interfaces,
such that the inputs of one correspond to the outputs of the other, 
or vice-versa (they match each other's expections).


## Abstraction

The concepts of **abstraction** and **level of abstraction** go hand in hand with the concept of interfaces.
You will come across these concepts constantly in programming, so it's important to understand them.

**Abstraction** refers to the idea that actors interact with the system via its interface,
without caring about the implementation details.
For example, the keyboard is an abstraction for inputting text,
because to input text the user would just use the interface (keyboard) that's designed for that purpose,
without worrying how their key presses get converted into the text on the screen (implementation details).

The **level of abstraction** is about how complex or simple the system you're dealing with is.
The more individual components a thing is made up of, the more complex it is, the higher its level.
The fewer individual components it has, the simpler it is, the lower its level.

In our computer example, interacting with the computer system as a whole,
using a keyboard and looking at the screen, is a high level interaction.

The interaction of a keyboard and the computer is a slightly lower level interaction,
because the keyboard and the interface of the computer 
that supports keyboard input is a smaller part of the entire computer system.

The smaller the part is, the lower the level.
For example, a key on the keyboard would be a very low level interaction,
because it essentially just physically presses the button.
The lowest level interaction on a computer would be sending an electric wave through a wire, 
or flipping a physical bit from 0 to 1.


### The abstraction paradox

Now even though the computer as a whole is easy to interact with for the user,
it's actually a very complex system with hundreds of individual components,
made up of even smaller components.
So even though its structure is complicated, 
it is simple to understand how it works enough to be able to use it.

On the other hand, even though RAM (Random Access Memory) is a singular component of the computer,
so it's relatively low level and simple, most people don't understand how it works,
and it would be generally harder for them to learn that than to learn how to use a computer.
So even though its structure is simple, understanding it is complicated.

This is just something to kind of think about.


### How does this relate to programming?

Programmers abstract processes and algorithms.
Code is the essential tool that allows us programmers to create said abstractions.
When broken down, these abstractions come down to sequences of simple fundamental operations, 
like addition of two numbers or writing a number into some location in memory.

Abstraction is ofter considered a synonym for "simplification" by programmers.
The idea is that abstraction helps simplify interactions with a system by offering a simple interface, 
which allows the user to not care about the implementation details of the system.
You don't have to undertand RAM to be able to use a computer.
