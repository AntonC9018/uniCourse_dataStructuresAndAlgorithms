#include <iostream>
#include <queue>
#include <cassert>
#include <fstream>
#include <sstream>
#include <array>

struct Cell
{
    int value;
};

constexpr static inline Cell WALL = { INT_MAX };
constexpr static inline Cell EMPTY = { 0 };
constexpr static inline Cell WATER_SOURCE = { 1 };

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

size_t getCellCount(const Grid& grid)
{
    return grid.width * grid.height;
}

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

const size_t MAX_NEIGHBOR_COUNT = 4;

struct EdgeMask
{
    std::array<bool, MAX_NEIGHBOR_COUNT> values;
};

EdgeMask getEdgeMask(const Grid& grid, size_t currentIndex)
{
    std::array<bool, MAX_NEIGHBOR_COUNT> isOnEdge
    {
        // Left column
        (currentIndex % grid.width) == 0,

        // Right column
        (currentIndex % grid.width) == grid.width - 1,

        // Top row
        currentIndex < grid.width,

        // Bottom row
        currentIndex >= getCellCount(grid) - grid.width,
    };
    return { isOnEdge };
}

bool isAnyEdge(const EdgeMask& edgeMask)
{
    for (size_t i = 0; i < MAX_NEIGHBOR_COUNT; i++)
    {
        if (edgeMask.values[i])
            return true;
    }
    return false;
}

std::array<size_t, MAX_NEIGHBOR_COUNT> getNeighborIndices(const Grid& grid, size_t currentIndex)
{
    std::array<size_t, MAX_NEIGHBOR_COUNT> neighborIndices
    {
        // Left neighbor
        currentIndex - 1,

        // Right neighbor
        currentIndex + 1,

        // Top neighbor
        currentIndex - grid.width,

        // Bottom neighbor
        currentIndex + grid.width,
    };
    return neighborIndices;
}

void printGrid(const Grid& grid)
{
    for (size_t y = 0; y < grid.height; y++)
    {
        for (size_t x = 0; x < grid.width; x++)
        {
            size_t linearIndex = y * grid.width + x;
            Cell cell = grid.firstCell[linearIndex];
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
                std::cout << cell.value;
            }
        }
        std::cout << std::endl;
    }
}

void computeAndPrintBacktrace(const Grid& grid, size_t currentIndex)
{
    std::vector<size_t> trace{};

    size_t backtrackIndex = currentIndex;
    while (true)
    {
        const Cell& cell = grid.firstCell[backtrackIndex];
        trace.push_back(backtrackIndex);
        if (cell.value == WATER_SOURCE.value)
            break;

        EdgeMask edgeMask = getEdgeMask(grid, backtrackIndex);
        std::array neighbors = getNeighborIndices(grid, backtrackIndex);
        int minValue = INT_MAX;
        size_t minPosition = 0;
        for (size_t neighborIndex = 0; neighborIndex < neighbors.size(); neighborIndex++)
        {
            if (edgeMask.values[neighborIndex])
                continue;

            size_t neighborPosition = neighbors[neighborIndex];
            const Cell& neighbor = grid.firstCell[neighborPosition];
            if (neighbor.value == EMPTY.value)
                continue;

            if (neighbor.value < minValue)
            {
                minValue = neighbor.value;
                minPosition = neighborPosition;
            }
        }

        backtrackIndex = minPosition;
    }

    std::cout << "The path to exit is: " << std::endl;
    size_t traceIndex = trace.size() - 1;

    std::cout << trace[traceIndex];
    // Here we have to work around the fact that size_t is unsigned.
    while (true)
    {
        if (traceIndex == 0)
            break;
        traceIndex -= 1;

        std::cout << " --> " << trace[traceIndex];
    }
}

void doWaterAlgorithm(Grid& grid)
{
    std::queue<Position> waterPositionsToProcess;

    size_t cellCount = getCellCount(grid);
    for (size_t i = 0; i < cellCount; i++)
    {
        Cell cell = grid.firstCell[i];
        if (cell.value != WALL.value
            && cell.value != EMPTY.value)
        {
            waterPositionsToProcess.push({ i });
        }
    }

    while (!waterPositionsToProcess.empty())
    {
        Position p = waterPositionsToProcess.front();
        waterPositionsToProcess.pop();

        Cell& cell = grid.firstCell[p.linearIndex];
        EdgeMask edgeMask = getEdgeMask(grid, p.linearIndex);
        bool isOnEdge = isAnyEdge(edgeMask);

        if (isOnEdge)
        {
            // backtrack
            computeAndPrintBacktrace(grid, p.linearIndex);
            return;
        }

        std::array neighborIndices = getNeighborIndices(grid, p.linearIndex);
        for (size_t i = 0; i < MAX_NEIGHBOR_COUNT; i++)
        {
            size_t neighborIndex = neighborIndices[i];
            Cell& neighbor = grid.firstCell[neighborIndex];
            if (neighbor.value != EMPTY.value)
                continue;

            neighbor.value = cell.value + 1;
            waterPositionsToProcess.push({ neighborIndex });
        }
    }
}

int main()
{
    std::string fileContent = readAllFile("maze.maze");
    Grid grid = createGridFromString(fileContent);
    printGrid(grid);
    doWaterAlgorithm(grid);
    destroyGrid(grid);

    return 0;
}
