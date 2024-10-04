#pragma once

#include "../common/common.h"
#include "../common/logic.h"
#include <span>

struct BoardText
{
    std::span<char> span;
    size_t rowLen;
};

void printBoard(BoardText& boardText, GameState& state);
BoardText createBoardText(const BoardDimensions& dimensions);
void freeBoardText(BoardText& boardText);
