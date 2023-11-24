#include <iostream>
#include "common.h"

bool validateCar(const Car& car, std::ostream& error, int currentYear);

int main()
{
    int currentYear = 2000;
    Car car{
        "", // empty string not allowed
        "ABC",
        "123",
        2001,
        4,
    };

    bool isValid = validateCar(car, std::cout, currentYear);
    if (!isValid)
        return 1;

    return 0;
}

bool validateCar(const Car& car, std::ostream& error, int currentYear)
{
    bool isValid = true;
    if (car.companyName.size() == 0)
    {
        error << "companyName is empty" << std::endl;
        isValid = false;
    }
    if (car.modelName.size() == 0)
    {
        error << "modelName is empty" << std::endl;
        isValid = false;
    }
    {
        size_t size = car.numberplateText.size();
        size_t minSymbols = 6;
        if (size < minSymbols)
        {
            error << "numberplaceText has less than ";
            error << minSymbols;
            error << " symbols, the actual size was ";
            error << size;
            error << std::endl;
            isValid = false;
        }
    }
    if (car.numberOfDoors < 0)
    {
        error << "numberOfDoors is negative";
        error << std::endl;
        isValid = false;
    }
    if (car.producedYear > currentYear)
    {
        error << "producedYear is less than the current year ";
        error << currentYear;
        error << std::endl;
        isValid = false;
    }
    return isValid;
}
