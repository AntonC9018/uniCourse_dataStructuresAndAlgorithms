#include <cassert>

#include "common.h"

Direction getOppositeDirection(Direction d)
{
    return (d + 2) % directionCount;
}

Vector getDirectionAsVector(Direction d)
{
    switch (d)
    {
        case UP:
        {
            return {
                .x = 0,
                .y = -1,
            };
        }
        case RIGHT:
        {
            return {
                .x = 1,
                .y = 0,
            };
        }
        case LEFT:
        {
            return {
                .x = -1,
                .y = 0,
            };
        }
        case DOWN:
        {
            return {
                .x = 0,
                .y = 1,
            };
        }
        default:
        {
            assert(false);
        }
    }
}

