#include "logic.h"
#include "common.h"
#include "raylib.h"
#include <iostream>

Direction getDesiredDirection()
{
    // get inputs
    while (true)
    {
        int pressedKey = GetKeyPressed();
        if (pressedKey == 0)
        {
            break;
        }

        switch (pressedKey)
        {
            case KEY_W:
            {
                return UP;
            }
            case KEY_A:
            {
                return LEFT;
            }
            case KEY_D:
            {
                return RIGHT;
            }
            case KEY_S:
            {
                return DOWN;
            }
            default:
            {
                break;
            }
        }
    }
    return INVALID_DIRECTION;
}

struct CellStyle
{
    int width;
    int gap;
};

Vector getCellScreenPosition(CellStyle style, Vector gamePos)
{
    int y = style.gap + gamePos.y * (style.width + style.gap);
    int x = style.gap + gamePos.x * (style.width + style.gap);
    return {
        .x = x,
        .y = y,
    };
}

struct SnakeStyle
{
    int width;
    int gap;
};

Vector getSnakeScreenPosition(
    CellStyle cellStyle,
    SnakeStyle snakeStyle,
    Vector gamePos)
{
    Vector screenPos = getCellScreenPosition(cellStyle, gamePos);
    screenPos.x += snakeStyle.gap;
    screenPos.y += snakeStyle.gap;
    return screenPos;
}

int main()
{
	SetConfigFlags(FLAG_VSYNC_HINT | FLAG_WINDOW_HIGHDPI);
	InitWindow(1280, 800, "Snake");

    const BoardDimensions dimensions = createBoardDimensions(5, 5);
    GameState state = createInitialGameState(dimensions);

    float timeSinceLogicUpdate = 0.0f;
    float secondsPerLogicUpdate = 0.5f;
    Direction currentInput = INVALID_DIRECTION;
    bool isGameOver = false;
	
	while (true)
	{
        if (WindowShouldClose())
        {
            break;
        }
        if (isGameOver)
        {
            break;
        }

        {
            Direction newInput = getDesiredDirection();
            if (newInput != INVALID_DIRECTION)
            {
                currentInput = newInput;
            }
        }


        timeSinceLogicUpdate += GetFrameTime();

        if (timeSinceLogicUpdate > secondsPerLogicUpdate)
        {
            if (currentInput != INVALID_DIRECTION)
            {
                state.snakeDirection = getNextDirection(
                    state.snakeDirection,
                    currentInput);
                currentInput = INVALID_DIRECTION;
            }

            isGameOver = doGameLogic(dimensions, state);
            timeSinceLogicUpdate -= secondsPerLogicUpdate;
        }

		BeginDrawing();
		ClearBackground(BLACK);
        
        CellStyle cellStyle{
            .width = 100,
            .gap = 5,
        };
        for (size_t rowIndex = 0; rowIndex < dimensions.row; rowIndex += 1)
        {
            for (size_t colIndex = 0; colIndex < dimensions.col; colIndex += 1)
            {
                Vector screenPos = getCellScreenPosition(cellStyle, {
                    .x = static_cast<int>(rowIndex),
                    .y = static_cast<int>(colIndex),
                });
                DrawRectangle(screenPos.x, screenPos.y, cellStyle.width, cellStyle.width, WHITE);
            }
        }

        SnakeStyle snakeStyle;
        {
            int snakeGap = 10;
            snakeStyle = {
                .width = cellStyle.width - 2 * snakeGap,
                .gap = snakeGap,
            };
        }

        {
            SnakePositionsStorage& snake = state.snakePositions;

            for (size_t offset = 1; offset < snake.snakeLength; offset += 1)
            {
                size_t m = snake.bodyPositions.size();
                size_t bodyPartIndex = (snake.headIndex + m - offset) % m;
                Vector snakePosition = snake.bodyPositions[bodyPartIndex];

                Vector snakeScreenPos = getSnakeScreenPosition(cellStyle, snakeStyle, snakePosition);
                DrawRectangle(snakeScreenPos.x, snakeScreenPos.y, snakeStyle.width, snakeStyle.width, GREEN);
            }

            {
                Vector headGamePos = getHeadPosition(snake);
                Vector headScreenPos = getSnakeScreenPosition(cellStyle, snakeStyle, headGamePos);
                DrawRectangle(headScreenPos.x, headScreenPos.y, snakeStyle.width, snakeStyle.width, BLUE);
            }
        }

        {
            Vector applePosition = state.applePosition;
            int appleWidth = cellStyle.width / 2 - 5; 
            Vector centerPos = getCellScreenPosition(cellStyle, applePosition);
            centerPos.x += (cellStyle.width / 2);
            centerPos.y += (cellStyle.width / 2);

            DrawCircle(centerPos.x, centerPos.y, static_cast<float>(appleWidth), { 255, 0, 0, 255 });
        }

		EndDrawing();
	}

	CloseWindow();
	return 0;
}
