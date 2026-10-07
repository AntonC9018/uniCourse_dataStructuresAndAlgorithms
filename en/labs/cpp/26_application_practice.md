---
slug: en/cpp/labs/application-practice
---
<!-- course-site-backlink:start -->
[This lesson on the website](https://AntonC9018.github.io/uniCourse_dataStructuresAndAlgorithms/en/cpp/labs/application-practice/)
<!-- course-site-backlink:end -->
# Building a complete application

## Worked example: Snake

[Full Snake game tutorial (in Russian)](https://youtu.be/2tp1cWS77lM).

## Practice

Choose a game and build a complete, playable application. These tasks have no supplied solutions.

If you are making a game, use a graphics library to display it.

Use your domain modeling skills to represent the game's state with appropriate structures. Use procedural programming:
pass the state into functions that implement the game's rules. Organize the program into headers (`.h`) and
implementation files (`.cpp`), and use a build system to build the application.

**Do not use global variables.** Keep the game's state in local variables and pass it to functions through parameters.

### 1. Tic-tac-toe

Make a game for two players. Detect wins and draws, and allow a new game to start.

### 2. Connect Four

Make a game for two players who drop pieces into columns. Detect four connected pieces and draws.

### 3. Memory matching

Make a game where the player reveals pairs of cards and tries to find all matching pairs.

### 4. Minesweeper

Make a game where the player uncovers cells, marks suspected mines, and wins by uncovering every safe cell.

### 5. Pong

Make a game with two paddles and a bouncing ball. Keep score and allow the match to restart.
