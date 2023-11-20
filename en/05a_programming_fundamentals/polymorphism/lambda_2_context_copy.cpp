#include <iostream>
#include <array>

int main()
{
    std::array nums { 1, 2 };

    auto functor = [
        a = nums[0],
        b = 10.0f,
        nums
    ]() mutable
    {
        nums[0] = 2;
        a += 2;
        b *= 2;
        return a + b;
    };

    // Copies by value (simply copies the functor's memory).
    decltype(functor) functorCopy = functor;

    std::cout << nums[0] << std::endl;
    std::cout << functor() << std::endl;
    std::cout << functor() << std::endl;
    std::cout << functor() << std::endl;
    std::cout << nums[0] << std::endl;

    std::cout << functorCopy() << std::endl;
}


// For the type of the functor variable, 
// the compiler generated a type like:
class Functor
{
    int a;
    float b;
    std::array<float, 2> nums;

public:
    Functor(
        int a,
        std::array<float, 2> nums) : 

        a(a),
        b(10.0f),
        nums(nums)
    {
    }

    float operator()()
    {
        nums[0] = 2;
        a += 2;
        b *= 2;
        return a + b;
    }
};