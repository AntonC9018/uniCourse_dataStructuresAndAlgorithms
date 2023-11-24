#include <iostream>
#include "common.h"

bool validateCar(const Car& car, std::ostream& error, int currentYear);

int main()
{
    int currentYear = getCurrentYear();
    Car car{
        "", // empty string not allowed
        "ABC",
        "123123",
        2000,
        4,
    };

    bool isValid = validateCar(car, std::cout, currentYear);

    car.companyName = "Audi";
    isValid = validateCar(car, std::cout, currentYear);

    car.producedYear = currentYear + 1;
    isValid = validateCar(car, std::cout, currentYear);

    if (isValid)
        return 0;
    return 1;
}

bool validateCar(const Car& car, std::ostream& error, int currentYear)
{
    if (car.companyName.size() == 0)
    {
        error << "companyName is empty" << std::endl;
        return false;
    }
    if (car.modelName.size() == 0)
    {
        error << "modelName is empty" << std::endl;
        return false;
    }
    {
        size_t size = car.numberplateText.size();
        size_t minSymbols = 6;
        if (size < 6)
        {
            error << "numberplaceText has less than ";
            error << minSymbols;
            error << " symbols, the actual size was ";
            error << size;
            error << std::endl;
            return false;
        }
    }
    if (car.numberOfDoors < 0)
    {
        error << "numberOfDoors is negative";
        error << std::endl;
        return false;
    }
    if (car.producedYear > currentYear)
    {
        error << "producedYear is less than the current year ";
        error << currentYear;
        error << std::endl;
        return false;
    }
    return true;
}
