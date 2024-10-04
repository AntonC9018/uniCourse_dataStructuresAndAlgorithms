#include "graphic.h"

#include <iostream>

static size_t getBoardTextIndexFromPosition(Vector position, size_t boardTextRowLen)
{
    size_t textIndex = static_cast<size_t>(position.x)
        + static_cast<size_t>(position.y) * boardTextRowLen;
    return textIndex;
}

void printBoard(
    BoardText& boardText,
    GameState& state)
{
    // memset(boardText, '_', boardTextSize);
    for (size_t i = 0; i < boardText.span.size(); i++)
    {
        boardText.span[i] = '_';
    }
    for (size_t i = boardText.rowLen - 1; i < boardText.span.size(); i += boardText.rowLen)
    {
        boardText.span[i] = '\n';
    }

    SnakePositionsStorage& snake = state.snakePositions;
    for (size_t offset = 1; offset < snake.snakeLength; offset += 1)
    {
        size_t m = snake.bodyPositions.size();
        size_t bodyPartIndex = (snake.headIndex + m - offset) % m;
        Vector snakePosition = snake.bodyPositions[bodyPartIndex];
        size_t textIndex = getBoardTextIndexFromPosition(snakePosition, boardText.rowLen);
        boardText.span[textIndex] = '*';
    }

    {
        Vector headPosition = getHeadPosition(snake);
        size_t textIndex = getBoardTextIndexFromPosition(headPosition, boardText.rowLen);
        boardText.span[textIndex] = '@';
    }

    {
        size_t textIndex = getBoardTextIndexFromPosition(
                state.applePosition,
                boardText.rowLen);
        boardText.span[textIndex] = 'o';
    }

    std::string_view s{
        boardText.span.data(),
        boardText.span.size(),
    };
    std::cout << s << std::endl;
}

BoardText createBoardText(
    const BoardDimensions& dimensions)
{
    size_t boardTextRowLen = dimensions.col + 1;
    size_t boardTextSize = boardTextRowLen * dimensions.row;
    char* boardText = new char[boardTextSize];
    std::span<char> boardSpan = { boardText, boardTextSize };
    return {
        .span = boardSpan,
        .rowLen = boardTextRowLen,
    };
}

void freeBoardText(BoardText& boardText)
{
    delete[] boardText.span.data();
}

