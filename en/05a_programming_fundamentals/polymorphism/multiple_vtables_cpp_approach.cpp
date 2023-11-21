#include <iostream>
#include <vector>

using VoidFunc = void(*)(void* context);

struct VTableBase
{
    size_t offsetToContext;
};

struct GreetingsVTable
{
    VTableBase base;
    VoidFunc introduceSelf;
    VoidFunc excuseSelf;
};

using ComputeFunc = int(*)(void* context, int a, int b);
using WriteCppProgramFunc = void(*)(void* context, std::ostream& out);

struct AnswersVTable
{
    VTableBase base;
    ComputeFunc computeSum;
    WriteCppProgramFunc writeCppProgram;
};

struct PersonBase
{
    GreetingsVTable* greetingsVTable;
    AnswersVTable* answersVTable;
};

enum ProgrammingLanguage
{
    None,
    Cpp,
    CSharp,
    Java,
};

struct PersonContext
{
    std::string name;
    std::string excuse;
    ProgrammingLanguage languageCanProgram;
    int maxNumberCanHoldInHead;
};

struct Person
{
    PersonBase base;
    PersonContext context;
};

struct DogBase
{
    AnswersVTable* answersVTable;
};

struct DogContext
{
    int favoriteNumber;
};

struct Dog
{
    DogBase base;
    DogContext context;
};


inline void* getContextForFunctionCall(VTableBase** object)
{
    VTableBase* vtable = *object;
    size_t offsetToContext = vtable->offsetToContext;
    void* context = reinterpret_cast<uint8_t*>(object) + offsetToContext;
    return context;
}

void enterAndThenLeave(GreetingsVTable** object)
{
    auto context = getContextForFunctionCall(reinterpret_cast<VTableBase**>(object));
    (*object)->introduceSelf(context);
    (*object)->excuseSelf(context);
}

void quiz(AnswersVTable** object)
{
    auto context = getContextForFunctionCall(reinterpret_cast<VTableBase**>(object));
    std::cout << "Question 1: What is 5 + 6?" << std::endl;
    int result1 = (*object)->computeSum(context, 5, 6);
    std::cout << "Answer: " << result1 << std::endl;

    std::cout << "Question 2: What is 10 + 20?" << std::endl;
    int result2 = (*object)->computeSum(context, 10, 20);
    std::cout << "Answer: " << result2 << std::endl;

    std::cout << "Question 3: Write a C++ program" << std::endl;
    (*object)->writeCppProgram(context, std::cout);
}

int main()
{
    PersonBase personBase{};
    {
        personBase.greetingsVTable = new GreetingsVTable{};
        personBase.greetingsVTable->base.offsetToContext = sizeof(PersonBase);
        personBase.greetingsVTable->excuseSelf = [](void* context)
        {
            auto typedContext = reinterpret_cast<PersonContext*>(context);
            std::cout << typedContext->excuse << std::endl;
        };
        personBase.greetingsVTable->introduceSelf = [](void* context)
        {
            auto typedContext = reinterpret_cast<PersonContext*>(context);
            std::cout << "Hi. My name is ";
            std::cout << typedContext->name << std::endl;
        };

        personBase.answersVTable = new AnswersVTable{};
        personBase.answersVTable->base.offsetToContext = 
            sizeof(PersonBase) - offsetof(PersonBase, answersVTable);
        personBase.answersVTable->computeSum = [](void* context, int a, int b)
        {
            auto typedContext = reinterpret_cast<PersonContext*>(context);
            int result = a + b;
            return std::min(result, typedContext->maxNumberCanHoldInHead);
        };
        personBase.answersVTable->writeCppProgram = [](void* context, std::ostream& out)
        {
            auto typedContext = reinterpret_cast<PersonContext*>(context);
            if (typedContext->languageCanProgram == Cpp)
            {
                out << "int main() { return 0; }" << std::endl;
            }
        };
    }

    Person john;
    Person jane;
    {
        PersonContext johnData{"John", "I'm not feeling well", Cpp, 30};
        john = {personBase, std::move(johnData)};

        PersonContext janeData{"Jane", "Sorry, I gotta go", Java, 20};
        jane = {personBase, std::move(janeData)};
    }

    
    DogBase dogBase{};

    {
        dogBase.answersVTable = new AnswersVTable{};
        dogBase.answersVTable->base.offsetToContext = sizeof(DogBase);
        dogBase.answersVTable->computeSum = [](void* context, int, int)
        {
            auto typedContext = reinterpret_cast<DogContext*>(context);
            return typedContext->favoriteNumber;
        };
        dogBase.answersVTable->writeCppProgram = [](void* context, std::ostream& out)
        {
        };
    }

    Dog husky;
    {
        DogContext huskyData{11};
        husky = {dogBase, huskyData};
    }

    std::vector<AnswersVTable**> objects{
        &john.base.answersVTable,
        &husky.base.answersVTable,
        &jane.base.answersVTable,
    };
    for (auto object : objects)
    {
        quiz(object);
    }

    std::vector<GreetingsVTable**> greetingsObjects{
        &john.base.greetingsVTable,
        &jane.base.greetingsVTable,
    };
    for (auto object : greetingsObjects)
    {
        enterAndThenLeave(object);
    }
}