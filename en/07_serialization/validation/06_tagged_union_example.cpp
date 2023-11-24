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

struct ValidationResult
{
    ValidationResultKind kind;
    union {
        // company name empty -- no context,
        // model name empty -- no context,

        // Numberplate text: expected length, actual length
        struct {
            size_t minLength;
            size_t actualLength;
        };

        // Number of doors: the number of doors.
        int numberOfDoors;

        // Produced year:
        struct {
            int actualProducedYear;
            int maximumAllowedProducedYear;
        };
    } payload;
};

ValidationResult validateCar(const Car& car, int currentYear);

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

    ValidationResult result = validateCar(car, currentYear);

    switch (result.kind)
    {
        case ValidationResultKind::Valid:
        {
            std::cout << "All fine";
            break;
        }

        case ValidationResultKind::NumberOfDoors_Negative:
        {
            std::cout 
                << "The number of doors " 
                << result.payload.numberOfDoors 
                << "must not be negative."
                << std::endl;
            break;
        }

        case ValidationResultKind::ProducedYear_BeyondCurrentYear:
        {
            std::cout
                << "Expected a year less than or equal to "
                << result.payload.maximumAllowedProducedYear
                << ", got "
                << result.payload.actualProducedYear
                << std::endl;
            break;
        }
        
        default:
            std::cout << "Some other error has occured";
            break;
    }

    // You can use the int value of the enum for the error code.
    // Valid is 0, which checks out with the "no-error" exit code of 0.
    return static_cast<int>(result.kind);
}

ValidationResult validateCar(const Car& car, int currentYear)
{
    if (car.companyName.size() == 0)
    {
        ValidationResult result;
        result.kind = ValidationResultKind::CompanyName_Empty;
        return result;
    }
    if (car.modelName.size() == 0)
    {
        ValidationResult result;
        result.kind = ValidationResultKind::ModelName_Empty;
        return result;
    }
    {
        size_t size = car.numberplateText.size();
        size_t minSymbols = 6;
        if (size < 6)
        {
            ValidationResult result;
            result.kind = ValidationResultKind::NumberplateText_TooShort;
            result.payload.actualLength = size;
            result.payload.minLength = minSymbols;
            return result;
        }
    }
    if (car.numberOfDoors < 0)
    {
        ValidationResult result;
        result.kind = ValidationResultKind::NumberOfDoors_Negative;
        result.payload.numberOfDoors = car.numberOfDoors;
        return result;
    }
    if (car.producedYear > currentYear)
    {
        ValidationResult result;
        result.kind = ValidationResultKind::ProducedYear_BeyondCurrentYear;
        result.payload.actualProducedYear = car.producedYear;
        result.payload.maximumAllowedProducedYear = currentYear;
        return result;
    }

    return { ValidationResultKind::Valid };
}

