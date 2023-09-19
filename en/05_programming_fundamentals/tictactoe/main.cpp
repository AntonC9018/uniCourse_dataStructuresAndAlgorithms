#include <iostream>
#include <assert.h>

// constexpr int BOARD_DIMENSION = 3;
#define BOARD_DIMENSIONS 3

// const char[3] symbols = { ' ', 'X', 'O' };
// if-else is not the best way to do this,
// the best way would be a lookup.
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

// Here we use a lookup. It's better than if-else.
const char[2] axisName = { 'x', 'y' };
char getAxisName(int axisIndex)
{
    return axisName[axisIndex];
}

bool getCoordinateFromConsole(int* outCoordinate, char coordinateName)
{
    std::cout << coordinateName << ": ";

    // NOTE:
    // Here, the dereference operator converts from int* into a int&.
    // It doesn't actually dereference (read from that memory).
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
	// Each coordinate has two names.
	// x is the same as coordinates[0]
	// y is the same as coordinates[1]
    // It is important to have both ways for generalizations.
	// `union` means they refer to the same memory.
	// In total, the size of this struct is 2 ints = 2 * 4 bytes = 8 bytes.
    union
    {
        struct {
            int x;
            int y;
        }
        int[2] coordinates;
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

bool checkRowOrColumnCombination(Board* board, Position position, int coordinateIndexToFix)
{
	int otherCoordinateIndex = 1 - coordinateIndexToFix;
	int* changingValue = &position.coordinates[otherCoordinateIndex];

	// Here, the dereferencing operator also effectively converts it to a reference.
	// It doesn't read from that memory, it writes to it.
	*changingValue = 0;

    int valueToCheck = board->elements[position.y][position.x];
    for (*changingValue = 1; *changingValue < BOARD_DIMENSION;
		// NOTE:
		// We increment the value in the memory, not the pointer.
		// So this increments either x or y by 1.
		(*changingValue)++)
    {
        if (board->elements[position.y][position.x] != valueToCheck)
            return false;
    }
    return true;
}

bool checkDiagonalCombination(Board* board, bool leftToRightDiagonal)
{
	// 0 _ _
	// _ 0 _
	// _ _ 0
    //
	// _ _ 0
	// _ 0 _
	// 0 _ _
	Position p;
	int xDirection;
    if (leftToRightDiagonal)
	{
		p.x = 0;
		p.y = 0;
        // x increases each iteration
		xDirection = 1;
	}
	else
    {
		p.x = 2;
		p.y = 0;
		// x descreases each iteration
		xDirection = -1;
    }

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

	// The code above really only makes sense if you have bigger boards.
	// If you know the size will always be 3x3, you could (and honestly should)
	// use the version below.
	// The version above is just a generalized version of the one below.
	// In this case the generalization isn't very useful, since it's hard to understand.
    // Another implementation could be like this:
#if false
	if (leftToRightDiagonal)
    {
		int v = board->elements[0][0];
		if (v != board->elements[1][1])
			return false;
		if (v != board->elements[2][2])
			return false;
		return true;
    }
    else
	{
		int v = board->elements[0][2];
		if (v != board->elements[1][1])
			return false;
		if (v != board->elements[2][0])
			return false;
		return true;
	}
#endif
}

bool checkIfPlayerWonByMakingMove(Board* board, Position move)
{
    for (int coordinateIndex = 0; coordinateIndex < BOARD_DIMENSION; coordinateIndex++)
    {
        bool hasWon = checkRowOrColumnCombination(&board, selectedPosition, coordinateIndex);
        if (hasWon)
            return true;
    }

    // left to right diagonal
    if (selectedPosition.x - selectedPosition.y == 0)
    {
        bool isLeftToRightDiagonal = true;
        bool hasWon = checkDiagonalCombination(&board, isLeftToRightDiagonal);
        if (hasWon)
			return true;
    }

    // right to left diagonal
    if (selectedPosition.x + selectedPosition.y == BOARD_DIMENSION - 1)
    {
        bool isLeftToRightDiagonal = false;
        bool hasWon = checkDiagonalCombination(&board, isLeftToRigthDiagonal);
        if (hasWon)
			return true;
    }

	return false;
}

// We know that `elements` is an inline fixed-size array, that is,
// it represents a contiguos piece of memory.
// Each cell has a consecutive position in this contiguos memory, so we can just
// loop through the memory and check if each cell is not the empty cell.
int checkBoardFullyOccupied(Board* board)
{
    int* elementsAsLinearBuffer = (int*) board->coordinates;
    size_t numCells = (size_t)(BOARD_DIMENSION * BOARD_DIMENSION);
    for (int cellIndex = 0; cellIndex < numCells; cellIndex++)
    {
        // 0 means empty.
        // 0 here is a "magical constant".
        // See the next commit to view how to get rid of them.
        if (elementsAsLinearBuffer[cellIndex] != 0)
            return false;
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
			// Player turn.
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
                        int* coord = &selectedPosition.coordinates[coordIndex];
                        char axisName = getAxisName(coordIndex);
                        while (true)
                        {
                            bool savedValidNumber = getCoordinateFromConsole(coord, axisName)
                            if (savedValidNumber)
                                break;
                        }
                    }

                    int selectedValue = board.elements[selectedPosition.y][selectedPosition.x];
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
			// Computer turn.
            case 1:
            {
                Position p = getFirstEmptyPosition(&board);
                assert(p == INVALID_POSITION,
                    "No empty positions, the game must have ended already.");

                // Find first empty position.
                break;
            }
        }

        board.elements[selectedPosition.y][selectedPosition.x] = playerValue;

        if (checkIfPlayerWonByMakingMove(&board, selectedPosition))
        {
			std::cout << "Player ";
			std::cout << playerIndex;
			std::cout << " won.";
			std::cout << std::endl;

			// Stop the game loop.
			break;
        }

		// Also need to check if there are no empty spaces on the board.
		if (isBoardEmpty(&board))
		{
			std::cout << "It's a tie...";
			break;
		}
    }

    return 1;
}