#include <string>

#pragma once

struct Car
{
    std::string companyName;
    std::string modelName;
    std::string numberplateText;
    int producedYear;
    int numberOfDoors;
};

#include <chrono>
#include <ctime>

inline int getCurrentYear()
{
    std::time_t currentTimestamp = std::time(0);
    // https://stackoverflow.com/questions/12212339/does-memory-for-localtime-need-to-be-deallocated
    std::tm* timeInfo = std::localtime(&currentTimestamp);
    std::time_t* t = &currentTimestamp;
    int year = timeInfo->tm_year;
    return year;
}