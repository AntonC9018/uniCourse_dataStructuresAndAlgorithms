#include <iostream>
#include <cassert>
#include <queue>
#include <array>

struct Cell
{
    int value;
};

constexpr static inline Cell WALL = {INT_MAX};
constexpr static inline Cell EMPTY = {INT_MAX - 1};
constexpr static inline Cell WATER_SOURCE = {0};

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

// #### 
// # ## 
// #w #
// # ##
// #   
// ####
Grid createGridFromString(std::string_view str)
{
    size_t width = 0;
    {
        for (size_t i = 0; i < str.size(); ++i)
        {
            if (str[i] == '\n')
            {
                break;
            }
            ++width;
        }
    }

    size_t height = 1;
    {
        size_t currentWidth = 0;
        for (size_t i = width + 1; i < str.size(); ++i)
        {
            bool isEndOfLine = str[i] == '\n';
            bool isEndOfRow = currentWidth == width;

            if (isEndOfRow || isEndOfLine)
            {
                height += 1;
            }

            if (isEndOfRow && !isEndOfLine)
            {
                std::cerr << "Row too long at position " << i << std::endl;
                assert(false);
            }

            if (!isEndOfLine)
            {
                currentWidth += 1;
            }
            else
            {
                currentWidth = 0;
            }
        }

        if (currentWidth != 0 && currentWidth != width)
        {
            height += 1;
        }
    }

    Grid grid;
    grid.width = width;
    grid.height = height;
    grid.firstCell = new Cell[width * height];

    {
        size_t linearIndex = 0;
        for (size_t stringIndex = 0; stringIndex < str.size(); stringIndex++)
        {
            char ch = str[stringIndex];
            switch (ch)
            {
                case '\n':
                {
                    size_t cellCountToCompleteRow = linearIndex % width;
                    while (cellCountToCompleteRow % width != 0)
                    {
                        grid.firstCell[linearIndex] = EMPTY;
                        linearIndex += 1;
                        cellCountToCompleteRow += 1;
                    }
                    continue;
                }
                case '#':
                {
                    grid.firstCell[linearIndex] = WALL;
                    break;
                }
                case 'w':
                {
                    grid.firstCell[linearIndex] = WATER_SOURCE;
                    break;
                }
                case ' ':
                {
                    grid.firstCell[linearIndex] = EMPTY;
                    break;
                }
                default:
                {
                    assert(false);
                }
            }
            linearIndex += 1;
        }
        assert(linearIndex == getCellCount(grid));
    }

    return grid;
}

void printGrid(std::ostream& out, const Grid& grid)
{
    for (size_t y = 0; y < grid.height; y++)
    {
        for (size_t x = 0; x < grid.width; x++)
        {
            Cell cell = grid.firstCell[y * grid.width + x];
            if (cell.value == WALL.value)
            {
                out << "# ";
            }
            else if (cell.value == WATER_SOURCE.value)
            {
                out << "w ";
            }
            else if (cell.value == EMPTY.value)
            {
                out << "  ";
            }
            else
            {
                out << cell.value;
            }
        }
        out << std::endl;
    }
}

const static inline int NEIGHBOR_COUNT = 4;

std::array<size_t, NEIGHBOR_COUNT> getNeighborLinearIndices(const Grid& grid, size_t linearIndex)
{
    size_t topNeighbor = linearIndex - grid.width;
    size_t bottomNeigbor = linearIndex + grid.width;
    size_t leftNeighbor = linearIndex - 1;
    size_t rightNeighbor = linearIndex + 1;
    std::array neighbors =
    {
        topNeighbor,
        bottomNeigbor,
        leftNeighbor,
        rightNeighbor,
    };
    return neighbors;
}

std::array<bool, NEIGHBOR_COUNT> getEdgeMask(const Grid& grid, size_t linearIndex)
{
    bool isTopRow = linearIndex < grid.width;
    bool isBottomRow = linearIndex >= (grid.height - 1) * grid.width;
    bool isLeftColumn = linearIndex % grid.width == 0;
    bool isRightColumn = linearIndex % grid.width == grid.width - 1;
    std::array isEdge =
    {
        isTopRow,
        isBottomRow,
        isLeftColumn,
        isRightColumn,
    };
    return isEdge;
}

bool isOnEdge(std::array<bool, NEIGHBOR_COUNT> edgeMask)
{
    // for (bool isEdge : edgeMask)
    for (size_t i = 0; i < edgeMask.size(); i++)
    {
        if (edgeMask[i])
        {
            return true;
        }
    }
    return false;
}

void backtrack(const Grid& grid, size_t lastLinearIndex)
{
    std::vector<size_t> trace{};

    size_t linearIndex = lastLinearIndex;
    while (true)
    {
        trace.push_back(linearIndex);

        Cell cell = grid.firstCell[linearIndex];
        if (cell.value == WATER_SOURCE.value)
        {
            break;
        }

        std::array neighbors = getNeighborLinearIndices(grid, linearIndex);
        std::array edgeMask = getEdgeMask(grid, linearIndex);
        int minValue = INT_MAX;
        size_t linearIndexOfMinNeighbor = 0;
        for (size_t i = 0; i < neighbors.size(); i++)
        {
            bool isOnEdge = edgeMask[i];
            if (isOnEdge)
            {
                continue;
            }

            size_t neighborLinearIndex = neighbors[i];
            Cell neighborCell = grid.firstCell[neighborLinearIndex];
            if (neighborCell.value < minValue)
            {
                minValue = neighborCell.value;
                linearIndexOfMinNeighbor = neighborLinearIndex;
            }
        }

        linearIndex = linearIndexOfMinNeighbor;
    }

    std::cout << "Trace: ";
    {
        std::cout << trace[0];
    }
    for (size_t i = 1; i < trace.size(); i++)
    {
        std::cout << " -> " << trace[i];
    }
    std::cout << std::endl;
}

int main()
{
    std::string_view gridString = 
        "####\n"
        "# ##\n"
        "#w #\n"
        "#   \n"
        "####\n";
    std::cout << gridString << std::endl;
    Grid grid = createGridFromString(gridString);
    printGrid(std::cout, grid);

    std::queue<size_t> nextCellLinearIndicesToProcess;
    for (size_t linearIndex = 0; linearIndex < getCellCount(grid); linearIndex++)
    {
        if (grid.firstCell[linearIndex].value == WATER_SOURCE.value)
        {
            nextCellLinearIndicesToProcess.push(linearIndex);
        }
    }

    bool foundExit = false;
    while (!nextCellLinearIndicesToProcess.empty())
    {
        size_t linearIndex = nextCellLinearIndicesToProcess.front();
        nextCellLinearIndicesToProcess.pop();

        std::array edgeMask = getEdgeMask(grid, linearIndex);
        if (isOnEdge(edgeMask))
        {
            backtrack(grid, linearIndex);
            foundExit = true;
            break;
        }

        std::array neighbors = getNeighborLinearIndices(grid, linearIndex);
        Cell currentCell = grid.firstCell[linearIndex];
        for (size_t i = 0; i < neighbors.size(); i++)
        {
            size_t neighborLinearIndex = neighbors[i];
            Cell& neighborCell = grid.firstCell[neighborLinearIndex];
            if (neighborCell.value != EMPTY.value)
            {
                continue;
            }

            neighborCell.value = currentCell.value + 1;
            nextCellLinearIndicesToProcess.push(neighborLinearIndex);
        }
    }

    if (!foundExit)
    {
        std::cout << "The maze has no exit " << std::endl;
    }
}
