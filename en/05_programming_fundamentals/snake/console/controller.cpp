#include "controller.h"
#include <iostream>

Direction getDirectionFromKey(char ch)
{
    switch (ch)
    {
        case 'W':
        case 'w':
        {
            return UP;
        }
        case 'S':
        case 's':
        {
            return DOWN;
        }
        case 'A':
        case 'a':
        {
            return LEFT;
        }
        case 'D':
        case 'd':
        {
            return RIGHT;
        }
        default:
        {
            return INVALID_DIRECTION;
        }
    }
}

// raylib
char getPressedSymbol()
{
    int ch = std::cin.get();
    const int asciiMask = 0x7F;
    if ((ch & asciiMask) == ch)
    {
        return static_cast<char>(ch);
    }
    else
    {
        return 0;
    }
}
