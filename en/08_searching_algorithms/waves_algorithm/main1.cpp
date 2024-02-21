#include <iostream>
#include <queue>
#include <cassert>
#include <fstream>
#include <sstream>

struct Cell
{
    int value;
};

const static inline Cell WALL = { INT_MAX };
const static inline Cell EMPTY = { 0 };
const static inline Cell WATER_SOURCE = { 1 };

struct Position
{
    size_t linearIndex;
};

struct Grid
{
    Cell* firstCell;
    size_t width;
    size_t height;
};

Grid createGridFromString(std::string_view str)
{
    size_t width;
    {
        size_t index = 0;
        while (index < str.size())
        {
            if (str[index] == '\n')
            {
                break;
            }
            index++;
        }
        width = index;
    }

    // Validate if each row has the same width
    {
        size_t currentRowWidth = 0;
        size_t index = width + 1;
        while (index < str.size())
        {
            char c = str[index];
            if (c == '\n')
            {
                assert(currentRowWidth == width);
                currentRowWidth = 0;
            }
            else
            {
                currentRowWidth++;
            }
            index++;
        }
    }

    size_t height = (str.size() + 1) / (width + 1);
    size_t cellCount = width * height;
    Cell* cells = new Cell[cellCount];

    {
        size_t stringIndex = 0;
        for (size_t i = 0; i < cellCount; i++)
        {
            // Detect new line
            if (i != 0 && i % width == 0)
            {
                assert(str[stringIndex] == '\n');
                stringIndex++;
            }
            // # -- wall
            // w -- water
            // ' ' -- undiscovered cell
            else
            {
                char c = str[stringIndex];
                switch (c)
                {
                    case '#':
                    {
                        cells[i] = WALL;
                        break;
                    }
                    case 'w':
                    {
                        cells[i] = WATER_SOURCE;
                        break;
                    }
                    case ' ':
                    {
                        cells[i] = EMPTY;
                        break;
                    }
                    default:
                    {
                        assert(false);
                        break;
                    }
                }
            }
            
            stringIndex++;
        }
    }

    Grid grid;
    grid.firstCell = cells;
    grid.width = width;
    grid.height = height;
    return grid;
}

void destroyGrid(Grid grid)
{
    delete[] grid.firstCell;
}

std::string readAllFile(const char* fileName)
{
    std::ifstream t;
    t.open(fileName);
    std::stringstream buffer;
    buffer << t.rdbuf();
    return buffer.str();
}


int main()
{
    std::string fileContent = readAllFile("maze.maze");
    Grid grid = createGridFromString(fileContent);

    for (size_t y = 0; y < grid.height; y++)
    {
        for (size_t x = 0; x < grid.width; x++)
        {
            size_t linearIndex = y * grid.width + x;
            Cell cell = grid.firstCell[linearIndex];
            std::cout << cell.value;
            if (cell.value == WALL.value)
            {
                std::cout << "#";
            }
            else if (cell.value == EMPTY.value)
            {
                std::cout << " ";
            }
            else
            {
                std::cout << "w";
            }
        std::cout << std::endl;
        }
        std::cout << std::endl;
    }

    std::queue<Position> waterPositionsToProcess;

    for (size_t i = 

    while (!waterPositionsToProcess.empty())
    {
        Position p = waterPositionsToProcess.front();
        waterPositionsToProcess.pop();
        std::cout << p.linearIndex << std::endl;

        if (p.linearIndex == 7)
        {
            waterPositionsToProcess.push({ 8 });
        }
    }
    
    return 0;
}
