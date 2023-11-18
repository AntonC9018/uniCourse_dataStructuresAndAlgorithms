#include <iostream>
#include <cassert>

enum class TrafficLightColor
{
    RED = 0,
    YELLOW = 1,
    GREEN = 2,
};

void writeLightColor(TrafficLightColor color)
{
    switch (color)
    {
        case TrafficLightColor::RED:
        {
            std::cout << "red";
            break;
        }
        case TrafficLightColor::YELLOW:
        {
            std::cout << "yellow";
            break;
        }
        case TrafficLightColor::GREEN:
        {
            std::cout << "green";
            break;
        }
        default:
        {
            assert(false);
        }
    }
}

int main()
{
    writeLightColor(TrafficLightColor::RED);
    writeLightColor(TrafficLightColor::YELLOW);
    writeLightColor(static_cast<TrafficLightColor>(1)); // have to cast instead
}