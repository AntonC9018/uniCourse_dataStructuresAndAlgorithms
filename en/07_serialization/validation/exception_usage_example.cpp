#include <iostream>
#include <sstream>

int main()
{
    // Try different inputs:
    std::string str = "12311111111111abc";
    // std::string str = "abc";
    // std::string str = "123";
    // std::string str = "123abc";

    bool converted = false;
    int i;
    try
    {
        i = std::stoi(str);
        converted = true;
    }
    catch (const std::invalid_argument& e)
    {
        std::cout 
            << "Invalid argument: " 
            << e.what() // prints the string describing the exception.
            << std::endl;
    }
    catch (const std::out_of_range& e)
    {
        std::cout 
            << "Out of range: " 
            << e.what()
            << std::endl;
    }

    if (converted)
    {
        std::cout << i << std::endl;
    }
}