#include <iostream>
#include "common.h"

using BaseType = uint8_t; // 1 byte is enough for us

enum class ValidationResultFlags : BaseType
{
    None = 0,
    CompanyName_Empty = 1 << 0, // 1st bit set
    ModelName_Empty = 1 << 1, // 2nd bit set ...
    NumberplateText_TooShort = 1 << 2,
    NumberOfDoors_Negative = 1 << 3,
    ProducedYear_BeyondCurrentYear = 1 << 4,
    All = CompanyName_Empty 
        | ModelName_Empty 
        | NumberplateText_TooShort 
        | NumberOfDoors_Negative 
        | ProducedYear_BeyondCurrentYear,
    
    // Can also get it like this.
    // All = (((1 << 4) - 1) << 1) | 1,

    // Or like this (but with this you have to be wary of overflow).
    // All = (1 << 5) - 1,

    // Or like this:
    // All = static_cast<BaseType>(~0) >> (sizeof(BaseType) * 8 - 5),
};
using F = ValidationResultFlags;

// We have to redefine these operators, because C++ sucks.
inline F operator|(F a, F b)
{
    BaseType a1 = static_cast<BaseType>(a);
    BaseType b1 = static_cast<BaseType>(b);

    // The actual work done here.
    BaseType result = a1 | b1;

    return static_cast<F>(result);
}
inline F& operator|=(F& a, F b)
{
    a = a | b;
    return a; 
}

inline F operator&(F a, F mask)
{
    BaseType a1 = static_cast<BaseType>(a);
    BaseType mask1 = static_cast<BaseType>(mask);
    BaseType result = a1 & mask1;
    return static_cast<F>(result);
}

inline bool containsAnyOf(F a, F b)
{
    return (a & b) != F::None;
}

inline bool containsAllOf(F a, F b)
{
    return (a & b) == b;
}

inline bool containsNoneOf(F a, F b)
{
    return (a & b) == F::None;
}


F validateCar(const Car& car, int currentYear);

int main()
{
    int currentYear = getCurrentYear();
    Car car{
        "",
        "",
        "1231",
        20000,
        -5,
    };

    F result = validateCar(car, currentYear);
    {
        F errorsToFindMask = F::CompanyName_Empty | F::ProducedYear_BeyondCurrentYear;
        if (containsAnyOf(result, errorsToFindMask))
        {
            std::cout << "One or both of the two selected errors are present, and maybe more." << std::endl;
        }
    }

    if (result == F::All)
    {
        std::cout << "All possible errors are present in the result." << std::endl;
    }

    if (result == F::None)
    {
        std::cout << "None of the flags are set." << std::endl;
    }

    if (containsAnyOf(result, F::ModelName_Empty))
    {
        std::cout << "modelName is empty!" << std::endl;
    }

    {
        F mask = F::NumberplateText_TooShort | F::CompanyName_Empty;
        if (containsNoneOf(result, mask))
        {
            std::cout << "The error is NOT about either the numberplate or the company name." << std::endl;
        }
    }

    {
        F mask = F::NumberOfDoors_Negative | F::ProducedYear_BeyondCurrentYear;
        if (containsAllOf(result, mask))
        {
            std::cout << "The error is about doors and the produced year." << std::endl;
        }
    }

    return static_cast<int>(result);
}

F validateCar(const Car& car, int currentYear)
{
    F result{};
    if (car.companyName.size() == 0)
    {
        result |= F::CompanyName_Empty;
    }
    if (car.modelName.size() == 0)
    {
        result |= F::ModelName_Empty;
    }
    {
        size_t size = car.numberplateText.size();
        size_t minSymbols = 6;
        if (size < 6)
        {
            result |= F::NumberplateText_TooShort;
        }
    }
    if (car.numberOfDoors < 0)
    {
        result |= F::NumberOfDoors_Negative;
    }
    if (car.producedYear > currentYear)
    {
        result |= F::ProducedYear_BeyondCurrentYear;
    }
    return result;
}

