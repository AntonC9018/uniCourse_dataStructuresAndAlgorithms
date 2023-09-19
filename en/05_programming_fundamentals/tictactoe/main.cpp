#include <iostream>
#include <cassert>

// constexpr int BOARD_DIMENSION = 3;
#define BOARD_DIMENSION 3

// Struct declarations have to go up top, because they're referenced
// in the function declarations.
struct Board
{
    int elements[BOARD_DIMENSION][BOARD_DIMENSION];
};

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
        };
        int coordinates[2];
    };
};

const Position INVALID_POSITION = { -1, -1 };
#define COORDINATE_COUNT 2

// Putting functions declarations up top is a good practice,
// because then you can either move the definitions to another file,
// linking them from another implementation file, or just define them
// after the main function.
// I argue you should do this after you've defined and used the function,
// because if you change e.g. the function parameters, you'll have to change
// these declarations as well, which adds a maintainability cost (how easily you can change things).
// Split them off after you've decided on the interface
// (what they take as parameters, and what they return).
char getSymbol(int value);
char getAxisName(int axisIndex);
bool getCoordinateFromConsole(int* outCoordinate, char coordinateName);
bool checkIsInvalidPosition(Position p);
Position getFirstEmptyPosition(Board* board);
bool checkRowOrColumnCombination(Board* board, Position position, int coordinateIndexToVary);
bool checkDiagonalCombination(Board* board, bool leftToRightDiagonal);
bool checkIfPlayerWonByMakingMove(Board* board, Position move);
int checkBoardFullyOccupied(Board* board);
void printGameState(Board* board);

int main()
{
    // 0 - empty
    // 1 - X
    // 2 - O
    Board board = {};
    int playerIndex = 0;
	int playerCount = 2;

	printGameState(&board);

    // Game loop
    while (true)
    {
        int playerValue = playerIndex + 1;
        Position selectedPosition = INVALID_POSITION;

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

                    for (int coordIndex = 0; coordIndex < COORDINATE_COUNT; coordIndex++)
                    {
                        int* coord = &selectedPosition.coordinates[coordIndex];
                        char axisName = getAxisName(coordIndex);
                        while (true)
                        {
                            bool savedValidNumber = getCoordinateFromConsole(coord, axisName);
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

					// Input selected.
					break;
                }

                break;
            }
			// Computer turn.
            case 1:
            {
				// Just find the first empty position (for now).
                selectedPosition = getFirstEmptyPosition(&board);
                break;
            }
			default:
			{
				assert(false);
				break;
            }
        }

        assert(!checkIsInvalidPosition(selectedPosition));

		// Make the move.
        board.elements[selectedPosition.y][selectedPosition.x] = playerValue;

		// Print out the updated game state.
		printGameState(&board);

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
		if (checkBoardFullyOccupied(&board))
		{
			std::cout << "It's a tie...";
			break;
		}

		playerIndex += 1;
		playerIndex %= playerCount;
    }

    return 1;
}

// const char[3] symbols = { ' ', 'X', 'O' };
// if-else is not the best way to do this,
// the best way would be a lookup.
char getSymbol(int value)
{
	switch (value)
    {
		case 0:
			return '_';
		case 1:
			return 'X';
		case 2:
			return 'O';
		default:
        {
            assert(false);
			return '\0';
        }
    }
}

// Here we use a lookup. It's better than if-else.
const char axisName[2] = { 'x', 'y' };
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
    else if (*outCoordinate >= BOARD_DIMENSION)
    {
        std::cout << "Position must be less than ";
        std::cout << BOARD_DIMENSION;
        std::cout << ".";
        std::cout << std::endl;
        return false;
    }

    return true;
}

bool checkIsInvalidPosition(Position p)
{
	return p.x < 0 || p.y < 0;
}

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

bool checkRowOrColumnCombination(Board* board, Position position, int coordinateIndexToVary)
{
	int* changingValue = &position.coordinates[coordinateIndexToVary];

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
#if false
	// 0 _ _
	// _ 0 _
	// _ _ 0
    //
	// _ _ 0
	// _ 0 _
	// 0 _ _
	Position position;
	int xDirection;
    if (leftToRightDiagonal)
	{
		position.x = 0;
		position.y = 0;
        // x increases each iteration
		xDirection = 1;
	}
	else
    {
		position.x = 2;
		position.y = 0;
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
#else
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
    for (int coordinateIndex = 0; coordinateIndex < COORDINATE_COUNT; coordinateIndex++)
    {
        bool hasWon = checkRowOrColumnCombination(board, move, coordinateIndex);
        if (hasWon)
            return true;
    }

    // left to right diagonal
    if (move.x - move.y == 0)
    {
        bool isLeftToRightDiagonal = true;
        bool hasWon = checkDiagonalCombination(board, isLeftToRightDiagonal);
        if (hasWon)
			return true;
    }

    // right to left diagonal
    if (move.x + move.y == BOARD_DIMENSION - 1)
    {
        bool isLeftToRightDiagonal = false;
        bool hasWon = checkDiagonalCombination(board, isLeftToRightDiagonal);
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
    int* elementsAsLinearBuffer = (int*) board->elements;
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

#if false
	// Another idea is to just use an existing function for this.
	Position p = getFirstEmptyPosition(board);
	return checkIsInvalidPosition(p);
#endif
}

void printGameState(Board* board)
{
    for (int y = 0; y < BOARD_DIMENSION; y++)
    {
        for (int x = 0; x < BOARD_DIMENSION; x++)
        {
            int valueAtPosition = board->elements[y][x];
            char valueAsCharacter = getSymbol(valueAtPosition);
            std::cout << valueAsCharacter;
            std::cout << ' ';
        }
        std::cout << std::endl;
    }
}
