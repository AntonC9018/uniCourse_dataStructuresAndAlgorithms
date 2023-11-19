#include <iostream>
#include <array>
#include <vector>

using ButtonFunc = void(*)();
struct FuncOption
{
    std::string name;
    ButtonFunc func;
};

void printHello();
void greetUser();

void addTextOptions(std::vector<FuncOption> &allFunctions)
{
    allFunctions.push_back({"print \"Hello\"", printHello});
    allFunctions.push_back({"greet the user", greetUser});
}

void addTwoValues();
void subtractTwoValues();

void addCalculatorOptions(std::vector<FuncOption> &allFunctions)
{
    allFunctions.push_back({"add two values", addTwoValues});
    allFunctions.push_back({"subtract two values", subtractTwoValues});
}

int main()
{
    std::vector<FuncOption> allFunctions;
    addTextOptions(allFunctions);
    addCalculatorOptions(allFunctions);

    size_t functionChoice;
    while (true)
    {
        std::cout << "Select a function to be executed (";
        for (size_t i = 0; i < allFunctions.size(); i++)
        {
            std::cout << i << " - " << allFunctions[i].name << ", ";
        }
        std::cout << "): ";

        std::cin >> functionChoice;

        if (!std::cin.good())
            continue;
        if (functionChoice >= allFunctions.size())
            continue;
        break;
    } 
    
    allFunctions[functionChoice].func();
    return 0;
}


void greetUser()
{
    std::string userName;
    std::cout << "Enter your name: ";
    std::cin >> userName;
    std::cout << "Hello, " << userName << "!" << std::endl;
}

void printHello()
{
    std::cout << "Hello!" << std::endl;
}

std::array<float, 2> readTwoValues()
{
    std::array<float, 2> result;

    std::cout << "Enter a: ";
    std::cin >> result[0];
    
    std::cout << "Enter b: ";
    std::cin >> result[1];

    return result;
}

void addTwoValues()
{
    std::array values = readTwoValues();
    float result = values[0] + values[1];
    std::cout 
        << values[0] 
        << " + " 
        << values[1] 
        << " = " 
        << result 
        << std::endl;
}

void subtractTwoValues()
{
    std::array values = readTwoValues();
    float result = values[0] - values[1];
    std::cout 
        << values[0] 
        << " - " 
        << values[1] 
        << " = " 
        << result 
        << std::endl;
}