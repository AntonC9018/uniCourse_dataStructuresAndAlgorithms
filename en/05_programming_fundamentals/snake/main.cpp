#include "graphic.h"
#include "logic.h"
#include <iostream>

int main()
{
    const BoardDimensions dimensions = createBoardDimensions(5, 5);
    GameState state = createInitialGameState(dimensions);
    BoardText boardText = createBoardText(dimensions);

    printBoard(boardText, state);

    while (true)
    {
        std::cout << "Hello" << std::endl;
        {
            char key = getPressedSymbol();
            if (key == 10)
            {
                continue;
            }

            Direction desiredDirection = getDirectionFromKey(key);
            if (desiredDirection != INVALID_DIRECTION)
            {
                state.snakeDirection = getNextDirection(
                    state.snakeDirection,
                    desiredDirection);
            }
        }

        const bool isGameOver = doGameLogic(dimensions, state);

        printBoard(boardText, state);

        if (isGameOver)
        {
            break;
        }
    }

    freeBoardText(boardText);
    freeGameState(state);
}
