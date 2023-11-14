#include <iostream>
#include "common.h"

bool validateCar(const Car& car);

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

    bool isValid;

    isValid = validateCar(car, currentYear); // false

    car.companyName = "Audi";
    isValid = validateCar(car, currentYear); // true

    car.producedYear = currentYear + 1;
    isValid = validateCar(car, currentYear); // false

    // etc.

    if (isValid)
        return 0;

    return 1;
}

bool validateCar(const Car& car, int currentYear)
{
    if (car.companyName.size() == 0)
        return false;
    if (car.modelName.size() == 0)
        return false;
    if (car.numberplateText.size() < 6)
        return false;
    if (car.numberOfDoors < 0)
        return false;
    if (car.producedYear > currentYear)
        return false;
    return true;
}
