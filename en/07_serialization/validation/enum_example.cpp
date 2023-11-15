#include <iostream>
#include "common.h"

enum class ValidationResultKind
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
            break;

        case ValidationResultKind::NumberOfDoors_Negative:
            std::cout << "Number of doors was negative?? bruh";
            break;
        
        default:
            std::cout << "Some other error has occured";
            break;
    }

    // You can use the int value of the enum for the error code.
    // Valid is 0, which checks out with the "no-error" exit code of 0.
    return static_cast<int>(result);
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

