#pragma once

#include "common.h"
#include "logic.h"
#include <span>

struct BoardText
{
    std::span<char> span;
    size_t rowLen;
};

void printBoard(BoardText& boardText, GameState& state);
BoardText createBoardText(const BoardDimensions& dimensions);
void freeBoardText(BoardText& boardText);
