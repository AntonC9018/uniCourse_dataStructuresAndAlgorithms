#include <iostream>
#include <cassert>

static inline const int RED = 0;
static inline const int YELLOW = 1;
static inline const int GREEN = 2;

void writeColorName(int color)
{
    switch (color)
    {
        case RED:
        {
            std::cout << "red";
            break;
        }
        case YELLOW:
        {
            std::cout << "yellow";
            break;
        }
        case GREEN:
        {
            std::cout << "green";
            break;
        }
        default:
        {
            assert(false); // shouldn't happen.
        }
    }
}

int main()
{
    std::cout << "Please input a color: ";
    const int numColors = 3;
    {
        std::cout << "0 - ";
        writeColorName(0);
    }
    for (int i = 1; i < numColors; i++) 
    {
        std::cout << i << " - ";
        writeColorName(i);
    }

    int color;
    do
    {
        std::cin >> color;
    }
    while (!std::cin.good()); // while not parsed

    switch (color)
    {
        case RED:
        {
            std::cout << "Stop";
            break;
        }
        case YELLOW:
        {
            std::cout << "Get ready";
            break;
        }
        case GREEN:
        {
            std::cout << "Go";
            break;
        }
    }

    return 0;
}