#include <iostream>
#include <cassert>

// constexpr int BOARD_DIMENSION = 3;
#define BOARD_DIMENSION 3

enum class CellValue
{
	empty = 0,
	x = 1,
	o = 2,
	// NOTE:
	// This is a non-standard thing that I do sometimes.
    // You can define a standalone constant, or name this something different.
	_count = 3,
};


// Struct declarations have to go up top, because they're referenced
// in the function declarations.
struct Board
{
    CellValue elements[BOARD_DIMENSION][BOARD_DIMENSION];
};

#define COORDINATE_COUNT 2
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
        int coordinates[COORDINATE_COUNT];
    };
};

const Position INVALID_POSITION = { -1, -1 };

enum class Diagonal
{
    leftToRight = 0,
    rightToLeft = 1,
};

enum class PlayerKind
{
    human = 0,
    computer = 1,
};

enum CoordinateAxisIndex
{
    x = 0,
    y = 1,
};

// Putting functions declarations up top is a good practice,
// because then you can either move the definitions to another file,
// linking them from another implementation file, or just define them
// after the main function.
// I argue you should do this after you've defined and used the function,
// because if you change e.g. the function parameters, you'll have to change
// these declarations as well, which adds a maintainability cost (how easily you can change things).
// Split them off after you've decided on the interface
// (what they take as parameters, and what they return).
char getSymbol(CellValue value);
char getAxisName(CoordinateAxisIndex axisIndex);
bool getCoordinateFromConsole(int* outCoordinate, char coordinateName);
bool checkIsInvalidPosition(Position p);
Position getFirstEmptyPosition(Board* board);
bool checkRowOrColumnCombination(Board* board, Position position, CoordinateAxisIndex coordinateIndexToVary);
bool checkDiagonalCombination(Board* board, Diagonal diagonal);
bool checkIfPlayerWonByMakingMove(Board* board, Position move);
int checkBoardFullyOccupied(Board* board);
void printGameState(Board* board);
CellValue& valueAt(Board* board, Position position);

// Main doesn't need a split declaration, because it's not supposed
// to be called from anywhere else.
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
        CellValue playerValue = (CellValue)(playerIndex + 1);
		assert(playerValue < CellValue::_count);

        Position selectedPosition = INVALID_POSITION;

		PlayerKind playerKind = playerIndex == 0
			? PlayerKind::human
			: PlayerKind::computer;

        switch (playerKind)
        {
			// Player turn.
            case PlayerKind::human:
            {
                while (true)
                {
                    char playerSymbol = getSymbol(playerValue);
					// Calling `cout << string` returns back the `cout` object itself.
					// This is why we can chain multiple `<<` operators.
                    // The next calls will call `<<` on the `cout` object,
					// returned from the previous `<<` call.
                    std::cout
						<< "Select position to put "
						<< playerSymbol
						<< ": "
						<< std::endl;

					// NOTE:
					// It's problematic to do these loops in C++ with enums.
					// I actually don't know what the best way would be
					// (trying to avoid casts as much as possible).
                    for (int coordIndex = 0; coordIndex < COORDINATE_COUNT; coordIndex++)
                    {
                        int* coord = &selectedPosition.coordinates[coordIndex];
                        char axisName = getAxisName((CoordinateAxisIndex) coordIndex);
                        while (true)
                        {
                            bool savedValidNumber = getCoordinateFromConsole(coord, axisName);
                            if (savedValidNumber)
                                break;
                        }
                    }

                    CellValue selectedValue = valueAt(&board, selectedPosition);
                    if (selectedValue != CellValue::empty)
                    {
                        std::cout
							<< "Input position not empty!"
                        	<< std::endl;
                        continue;
                    }

					// Input selected.
					break;
                }

                break;
            }
			// Computer turn.
            case PlayerKind::computer:
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
        // We've returned a reference, so we can assign without dereferencing the pointer.
		valueAt(&board, selectedPosition) = playerValue;

		// Print out the updated game state.
		printGameState(&board);

        if (checkIfPlayerWonByMakingMove(&board, selectedPosition))
        {
			std::cout
				<< "Player "
			    << playerIndex
			    << " won."
			    << std::endl;

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
char getSymbol(CellValue value)
{
	switch (value)
    {
		case CellValue::empty:
			return '_';
		case CellValue::x:
			return 'X';
		case CellValue::o:
			return 'O';
		default:
        {
            assert(false);
			return '\0';
        }
    }
}

// Here we use a lookup. It's better than if-else.
const char axisName[COORDINATE_COUNT] = {
    'x',
	'y',
	// This better syntax is not available in C++ by default (needs a C99 extension).
	// [(int) CoordinateAxisIndex::x] = 'x', // element 0 = 'x'
    // [(int) CoordinateAxisIndex::y] = 'y', // element 1 = 'y'
};
char getAxisName(CoordinateAxisIndex axisIndex)
{
    return axisName[(int) axisIndex];
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
        std::cout << "Invalid input." << std::endl;
        return false;
    }
    else if (*outCoordinate < 0)
    {
        std::cout << "Position must be positive." << std::endl;
        return false;
    }
    else if (*outCoordinate >= BOARD_DIMENSION)
    {
        std::cout
			<< "Position must be less than "
            << BOARD_DIMENSION
            << "."
            << std::endl;
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
			// Can also call it like this:
			//
			// if (valueAt(board, { x, y }) == CellValue::empty)
			//
			// This creates a position with x and y
			// (it knows it needs to create a Position and not anything else,
			// because it has the information on the function parameter types)

            if (board->elements[y][x] == CellValue::empty)
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

bool checkRowOrColumnCombination(
	Board* board,
	Position position,
	CoordinateAxisIndex coordinateIndexToVary)
{
	int* changingValue = &position.coordinates[(int) coordinateIndexToVary];

	// Here, the dereferencing operator also effectively converts it to a reference.
	// It doesn't read from that memory, it writes to it.
	*changingValue = 0;

    CellValue valueToCheck = valueAt(board, position);
    for (*changingValue = 1; *changingValue < BOARD_DIMENSION;
		// NOTE:
		// We increment the value in the memory, not the pointer.
		// So this increments either x or y by 1.
		(*changingValue)++)
    {
        if (valueAt(board, position) != valueToCheck)
            return false;
    }
    return true;
}

bool checkDiagonalCombination(Board* board, Diagonal diagonal)
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
    if (diagonal == Diagonal::leftToRight)
	{
		position.x = 0;
		position.y = 0;
        // x increases each iteration
		xDirection = 1;
	}
	else if (diagonal == Diagonal::rightToLeft)
    {
		position.x = 2;
		position.y = 0;
		// x descreases each iteration
		xDirection = -1;
    }
    else
	{
		assert(false);
    }


    CellValue valueToCheck = valueAt(board, position);
    position.x += xDirection;
    position.y += 1;

    for (int i = 1; i < BOARD_DIMENSION; i++)
    {
        CellValue value = valueAt(board, position);
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
	if (diagonal == Diagonal::leftToRight)
    {
		CellValue v = board->elements[0][0];
		if (v != board->elements[1][1])
			return false;
		if (v != board->elements[2][2])
			return false;
		return true;
    }
    else
	{
		CellValue v = board->elements[0][2];
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
        bool hasWon = checkRowOrColumnCombination(
			board,
			move,
			(CoordinateAxisIndex) coordinateIndex);
        if (hasWon)
            return true;
    }

    // left to right diagonal
    if (move.x - move.y == 0)
    {
        bool hasWon = checkDiagonalCombination(board, Diagonal::leftToRight);
        if (hasWon)
			return true;
    }

    // right to left diagonal
    if (move.x + move.y == BOARD_DIMENSION - 1)
    {
        bool hasWon = checkDiagonalCombination(board, Diagonal::rightToLeft);
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
            CellValue valueAtPosition = board->elements[y][x];
            char valueAsCharacter = getSymbol(valueAtPosition);
            std::cout << valueAsCharacter << ' ';
        }
        std::cout << std::endl;
    }
}

// We return a reference (which is a pointer in disguise),
// in order to be able to easily set the value.
CellValue& valueAt(Board* board, Position position)
{
	// Note, than even though we return the address of the cell here,
	// we don't need to use the & (it's done implicitly when converting to a reference).
    return board->elements[position.y][position.x];
}