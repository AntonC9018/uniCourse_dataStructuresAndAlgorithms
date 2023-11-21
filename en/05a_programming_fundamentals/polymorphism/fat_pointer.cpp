#include <iostream>
#include <string>

using IntroductionFunc = void(*)(void* context);
using SumFunc = int(*)(void* context, int a, int b);

struct VirtualTable
{
    IntroductionFunc introduceOneself;
    SumFunc answer;
};

struct FatPointer
{
    // We store this by pointer here, so that we can reuse
    // the given set of functions for multiple contexts,
    // without copying all of them each time.
    VirtualTable* methods;
    void* context;
};

void test(FatPointer& object)
{
    object.methods->introduceOneself(object.context);
    int answer = object.methods->answer(object.context, 5, 6);
    std::cout << answer << std::endl;
}

struct Human
{
    std::string name;
};

struct Dog
{
    int favoriteNumber;
};

int main()
{
    VirtualTable dumbMethods{
        // Doesn't say anything as the introduction.
        [](void*){},
        [](void*, int, int){ return 0; },
    };
    VirtualTable dogMethods{
        [](void*){ std::cout << "Woof" << std::endl; },
        [](void* context, int a, int b){ 
            Dog* d = reinterpret_cast<Dog*>(context);
            return d->favoriteNumber;
        },
    };
    VirtualTable humanMethods{
        [](void* context){ 
            Human* h = reinterpret_cast<Human*>(context);
            std::cout << "Hi. My name is ";
            std::cout << h->name << std::endl;
        },
        [](void*, int a, int b){
            return a + b;
        },
    };

    FatPointer dumbCat{&dumbMethods, nullptr};

    Dog huskyContext{11};
    FatPointer husky{&dogMethods, &huskyContext};

    Human johnContext{"John"};
    FatPointer john{&humanMethods, &johnContext};

    Human janeContext{"Jane"};
    FatPointer jane{&humanMethods, &janeContext};

    test(dumbCat);
    test(husky);
    test(john);
    test(jane);

    return 0;
}