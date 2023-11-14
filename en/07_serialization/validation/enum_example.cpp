#include <iostream>
#include "common.h"

enum ValidationResultKind
{
    Valid = 0,
    CompanyName_Empty = 1,
    ModelName_Empty = 2,
    NumberplateText_TooShort = 3,
    NumberOfDoors_Negative = 4,
    ProducedYear_BeyondCurrentYear = 5,
};

ValidationResultKind validateCar(const Car& car, int currentYear);

int main()
{
    int currentYear = getCurrentYear();
    std::cout << currentYear;
    Car car{
        "", // empty string not allowed
        "ABC",
        "123123",
        2000,
        4,
    };

    ValidationResultKind result = validateCar(car, currentYear);

    switch (result)
    {
        case ValidationResultKind::Valid:
            std::cout << "All fine";
            return 0;

        case ValidationResultKind::NumberOfDoors_Negative:
            std::cout << "Number of doors was negative?? bruh";
            return 1;
        
        default:
            std::cout << "Some other error has occured";
            return 2;
    }
}

ValidationResultKind validateCar(const Car& car, int currentYear)
{
    if (car.companyName.size() == 0)
    {
        return ValidationResultKind::CompanyName_Empty;
    }
    if (car.modelName.size() == 0)
    {
        return ValidationResultKind::ModelName_Empty;
    }
    {
        size_t size = car.numberplateText.size();
        size_t minSymbols = 6;
        if (size < 6)
        {
            return ValidationResultKind::NumberplateText_TooShort;
        }
    }
    if (car.numberOfDoors < 0)
    {
        return ValidationResultKind::NumberOfDoors_Negative;
    }
    if (car.producedYear > currentYear)
    {
        return ValidationResultKind::ProducedYear_BeyondCurrentYear;
    }
    return ValidationResultKind::Valid;
}

