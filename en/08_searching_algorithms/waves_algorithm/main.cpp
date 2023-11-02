#include <string>
#include <span>
#include <iostream>
#include <assert.h>
#include <vector>
#include <array>
#include <unordered_set>

struct Cell
{
    int value;
};

bool isCellWall(Cell* cell)
{
    return cell->value == INT_MAX;
}

bool isCellEmpty(Cell* cell)
{
    return cell->value == 0;
}

bool isWaterCell(Cell* cell)
{
    if (isCellWall(cell))
        return false;
    if (isCellEmpty(cell))
        return false;
    return true;
}

const int WATER_SOURCE_VALUE = 1;

bool isCellWaterSource(Cell* cell)
{
    return cell->value == WATER_SOURCE_VALUE;
}

int getStepsFromWaterSource(Cell* cell)
{
    return cell->value - WATER_SOURCE_VALUE;
}

Cell createWaterSourceCell()
{
    Cell cell;
    cell.value = WATER_SOURCE_VALUE;
    return cell;
}

Cell createWallCell()
{
    Cell cell;
    cell.value = INT_MAX;
    // cell.value = ((unsigned)(-1)) >> 1;
    return cell;
}

Cell createEmptyCell()
{
    Cell cell;
    cell.value = 0;
    return cell;
}

struct Grid
{
    Cell* firstCell;
    size_t rowCount;
    size_t columnCount;
};

Cell* getCellAt(Grid* grid, size_t rowIndex, size_t columnIndex)
{
    if (rowIndex >= grid->rowCount)
        return 0;
    if (columnIndex >= grid->columnCount)
        return 0;
    size_t linearIndex = rowIndex * grid->columnCount + columnIndex;
    return grid->firstCell + linearIndex;
}

size_t getGridLinearArrayLength(Grid* grid)
{
    return grid->rowCount * grid->columnCount;
}

Cell* getCellAtIndex(Grid* grid, size_t linearIndex)
{
    if (linearIndex >= getGridLinearArrayLength(grid))
    {
        std::cout << "hello";
    }
    assert(linearIndex < getGridLinearArrayLength(grid));
    return grid->firstCell + linearIndex;
}

const size_t MAX_NEIGHBOR_COUNT = 4;

struct EdgeMask
{
    std::array<bool, MAX_NEIGHBOR_COUNT> values;
};

EdgeMask getEdgeMask(Grid* grid, size_t currentIndex)
{
    std::array<bool, MAX_NEIGHBOR_COUNT> isOnEdge
    {
        // Left column
        (currentIndex % grid->columnCount) == 0,

        // Right column
        ((currentIndex + 1) % grid->columnCount) == 0,

        // Top row
        currentIndex < grid->columnCount,

        // Bottom row
        currentIndex >= (grid->columnCount * (grid->rowCount - 1)),
    };
    return { isOnEdge };
}

bool isAnyEdge(EdgeMask* edgeMask)
{
    for (size_t i = 0; i < MAX_NEIGHBOR_COUNT; i++)
    {
        if (edgeMask->values[i])
            return true;
    }
    return false;
}

std::array<size_t, MAX_NEIGHBOR_COUNT> getNeighborIndices(Grid* grid, size_t currentIndex)
{
    std::array<size_t, MAX_NEIGHBOR_COUNT> neighborIndices
    {
        // Left neighbor
        currentIndex - 1,

        // Right neighbor
        currentIndex + 1,

        // Top neighbor
        currentIndex - grid->columnCount,

        // Bottom neighbor
        currentIndex + grid->columnCount,
    };
    return neighborIndices;
}

void computeAndPrintBacktrace(Grid* grid, size_t currentIndex)
{
    std::vector<size_t> trace{};

    size_t backtrackIndex = currentIndex;
    while (true)
    {
        Cell *cell = getCellAtIndex(grid, backtrackIndex);
        trace.push_back(backtrackIndex);
        if (isCellWaterSource(cell))
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
            Cell *neighbor = getCellAtIndex(grid, neighborPosition);
            if (isCellEmpty(neighbor))
                continue;

            if (neighbor->value < minValue)
            {
                minValue = neighbor->value;
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

int main()
{
    std::string mapFromFile =
        "BBBBB"
        "BW BB"
        "BB BB"
        "B   B"
        "BBB B";

        // "BB "
        // " W "
        // "   ";
    
    Grid grid;
    grid.columnCount = 5;
    grid.rowCount = mapFromFile.size() / grid.columnCount;
    // size_t elementCount = grid.columnCount * grid.rowCount;
    size_t elementCount = mapFromFile.size();
    grid.firstCell = (Cell*) malloc(sizeof(Cell) * elementCount);

    for (size_t elementIndex = 0; elementIndex < elementCount; elementIndex += 1)
    {
        char symbolAtPosition = mapFromFile[elementIndex];
        Cell newCell;
        switch (symbolAtPosition)
        {
            case ' ':
            {
                newCell = createEmptyCell();
                break;
            }
            case 'B':
            {
                newCell = createWallCell();
                break;
            }
            case 'W':
            {
                newCell = createWaterSourceCell();
                break;
            }
            default:
            {
                std::cout 
                    << "Error at position "
                    << elementIndex
                    << ". Invalid symbol "
                    << symbolAtPosition
                    << std::endl;
                break;
            }
        }
        grid.firstCell[elementIndex] = newCell;
    }

    std::span memory = { grid.firstCell, getGridLinearArrayLength(&grid) };
    std::unordered_set<size_t> currentOutermostWaterIndices{};

    for (size_t elementIndex = 0; elementIndex < elementCount; elementIndex++)
    {
        Cell* cell = getCellAtIndex(&grid, elementIndex);
        if (isWaterCell(cell))
        {
            currentOutermostWaterIndices.insert(elementIndex);
        }
    }

    if (currentOutermostWaterIndices.empty())
    {
        std::cout << "Map doesn't have a water cell" << std::endl;
        return 1;
    }

    int currentValue = WATER_SOURCE_VALUE + 1;

    std::unordered_set<size_t> newWaterPositions{};

    while (true)
    {
        for (size_t currentIndex : currentOutermostWaterIndices)
        {
            EdgeMask isOnEdge = getEdgeMask(&grid, currentIndex);

            if (isAnyEdge(&isOnEdge))
            {
                computeAndPrintBacktrace(&grid, currentIndex);
                return 0;
            }

            std::array neighborIndices = getNeighborIndices(&grid, currentIndex);
            for (size_t i = 0; i < neighborIndices.size(); i++)
            {
                size_t neighborIndex = neighborIndices[i];
                Cell* neighbor = getCellAtIndex(&grid, neighborIndex);
                if (!isCellEmpty(neighbor) || isCellWall(neighbor))
                    continue;

                neighbor->value = currentValue;

                // NOTE: This is O(1) because we use a set.
                newWaterPositions.insert(neighborIndex);
            }
        }

        if (newWaterPositions.empty())
        {
            std::cout << "Maze is unescapable" << std::endl;
            return 0;
        }

        currentOutermostWaterIndices.clear();
        std::swap(newWaterPositions, currentOutermostWaterIndices);
        currentValue++;
    }

    return 0;
}