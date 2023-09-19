#include <iostream>
#include <assert.h>

// constexpr int BOARD_DIMENSION = 3;
#define BOARD_DIMENSIONS 3

char getSymbol(int value)
{
    if (value == 1)
    {
        return 'X';
    }
    else if (value == 2)
    {
        return 'O';
    }
    else
    {
        assert(false, "Should never happen");
    }
}

const char[2] axisName = { 'x', 'y' };
char getAxisName(int axisIndex)
{
    return axisName[axisIndex];
}

bool getCoordinateFromConsole(int* outCoordinate, char coordinateName)
{
    std::cout << coordinateName << ": ";
    std::cin >> *outCoordinate;
    if (!std::cin)
    {
        std::cout << "Invalid input.";
        std::cout << std::endl;
        return false;
    }
    else if (*outCoordinate < 0)
    {
        std::cout << "Position must be positive.";
        std::cout << std::endl;
        return false;
    }
    else if (*outCoordinate >= BOARD_DIMENSIONS)
    {
        std::cout << "Position must be less than ";
        std::cout << BOARD_DIMENSIONS;
        std::cout << ".";
        std::cout << std::endl;
        return false;
    }

    return true;
}

struct Board
{
    int elements[BOARD_DIMENSION][BOARD_DIMENSION];
}

struct Position
{
    union
    {
        int[2] coordinates;
        struct {
            int x;
            int y;
        }
    }
}

const Position INVALID_POSITION = { -1, -1 };

Position getFirstEmptyPosition(Board* board)
{
    for (int y = 0; y < BOARD_DIMENSION; y++)
    {
        for (int x = 0; x < BOARD_DIMENSION; x++)
        {
            if (board->elements[y][x] == 0)
            {
                Position p = { };
                p.x = x;
                p.y = y;
                return p;

                // return Position { x, y };

                // return { x, y };
            }
        }
    }
    return INVALID_POSITION;
}

bool checkRowOrColumnCombination(Board* board, Position* memory, int* changingValue)
{
    *changingValue = 0;
    int valueToCheck = board->elements[memory->y][memory->x];
    for (*changingValue = 1; *changingValue < BOARD_DIMENSION; (*changingValue)++)
    {
        if (board->elements[memory->y][memory->x] != valueToCheck)
            return false;
    }
    return true;
}

bool checkDiagonalCombination(Board* board, Position position, int xDirection)
{
    if (xDirection == 1 || xDirection == -1)
        assert(false, "Pass in either -1 or 1");

    int valueToCheck = board->elements[position.y][position.x];

    position.x += xDirection;
    position.y += 1;

    for (int i = 1; i < BOARD_DIMENSION; i++)
    {
        int value = board->elements[position.y][position.x];
        if (value != valueToCheck)
            return false;

        position.x += xDirection;
        position.y += 1;
    }
    return true;
}

int main()
{
    // 0 - empty
    // 1 - X
    // 2 - O
    Board board = {};
    int playerIndex = 0;

    // Game loop
    while (true)
    {
        int playerValue = playerIndex + 1;
        Position selectedPosition;

        switch (playerIndex)
        {
            case 0:
            {
                while (true)
                {
                    char playerSymbol = getSymbol(playerValue);
                    std::cout << "Select position to put ";
                    std::cout << playerSymbol;
                    std::cout << ": " << std::endl;

                    for (int coordIndex = 0; coordIndex < 2; coordIndex++)
                    {
                        int* coord = &selectedPosition->coordinates[coordIndex];
                        char axisName = getAxisName(coordIndex);
                        while (true)
                        {
                            bool savedValidNumber = getCoordinateFromConsole(coord, axisName)
                            if (savedValidNumber)
                                break;
                        }
                    }

                    int selectedValue = board->elements[selectedPosition.y][selectedPosition.x];
                    // Not empty
                    if (selectedValue != 0)
                    {
                        std::cout << "Input position not empty!";
                        std::cout << std::endl;
                        continue;
                    }
                }

                break;
            }
            case 1:
            {
                Position p = getFirstEmptyPosition(&board);
                assert(p == INVALID_POSITION,
                    "No empty positions, the game must have ended already.");

                // Find first empty position.
                break;
            }
        }

        board->elements[selectedPosition.y][selectedPosition.x] = playerValue;

        // Check row
        {
            int y = selectedPosition.y;
            bool hasFoundOtherValue = false;
            for (int x = 0; x < BOARD_DIMENSION; x++)
            {
                if (board->elements[y][x] != playerValue)
                {
                    hasFoundOtherValue = true;
                    break;
                }
            }

            if (!hasFoundOtherValue)
            {
                std::cout << "Player " << playerValue << " won!";
                break;
            }
        }
        for (int coordinateIndex = 0; coordinateIndex < BOARD_DIMENSION; coordinateIndex++)
        {
            Position memory = selectedPosition;
            int* changingValue = &memory->coordinates[coordinateIndex];
            bool hasWon = checkRowOrColumnCombination(&board, &memory, changingValue);
            if (hasWon)
                std::cout << "Player " << playerIndex << " won!";
        }

        // left to right diagonal
        if (selectedPosition.x - selectedPosition.y == 0)
        {
            int xDirection = 1;
            Position topLeft;
            topLeft.x = 0;
            topLeft.y = 0;
            bool hasWon = checkDiagonalCombination(&board, topLeft, xDirection);
            if (hasWon)
                std::cout << "Player " << playerIndex << " won!";
        }

        // right to left diagonal
        if (selectedPosition.x + selectedPosition.y == BOARD_DIMENSION - 1)
        {
            int xDirection = -1;
            Position topLeft;
            topLeft.x = 2;
            topLeft.y = 0;
            bool hasWon = checkDiagonalCombination(&board, topLeft, 1);
            if (hasWon)
                std::cout << "Player " << playerIndex << " won!";
        }
    }

    return 1;
}