#include <iostream>
#include <cassert>

namespace TrafficLightColor
{
    struct Type
    {
        int value;

        // Make sure the constructor is never called implicilty.
        // We could even make this private so that people can only use the constants,
        // but being able to convert from an int is useful.
        constexpr explicit Type(int value) : value(value) {}
    };

    inline static constexpr Type RED{0};
    inline static constexpr Type YELLOW{1};
    inline static constexpr Type GREEN{2};
};

using TrafficLightColorT = TrafficLightColor::Type;

void writeLightColor(TrafficLightColorT color)
{
    switch (color.value)
    {
        case TrafficLightColor::RED.value:
        {
            std::cout << "red";
            break;
        }
        case TrafficLightColor::YELLOW.value:
        {
            std::cout << "yellow";
            break;
        }
        case TrafficLightColor::GREEN.value:
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
    // writeLightColor(1); // doesn't work, because the constructor is explicit
    writeLightColor(TrafficLightColorT{1}); // converts to TrafficLightColor using the constructor
}