#include <iostream>
#include <array>
#include <limits>

using ButtonFunc = void(*)();

void printHello()
{
    std::cout << "Hello!" << std::endl;
}

void greetUser()
{
    std::string userName;
    std::cout << "Enter your name:";
    std::cin >> userName;
    std::cout << "Hello, " << userName << "!" << std::endl;
}

int main()
{
    std::array allFunctions{
        printHello,
        greetUser,
    };

    size_t functionChoice;
    while (true)
    {
        std::cout << "Select a function to be executed:";
        if (!(std::cin >> functionChoice))
        {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            continue;
        }
        if (functionChoice >= allFunctions.size())
            continue;
        break;
    } 
    
    ButtonFunc selectedFunc = allFunctions[functionChoice];
    selectedFunc();
    return 0;
}
