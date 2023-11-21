#include <iostream>
#include <vector>

class GreetingAbstractBase
{
public:
    virtual void introduceSelf() = 0;
    virtual void excuseSelf() = 0;
};

class QuestionAbstractBase
{
public:
    virtual int computeSum(int a, int b) = 0;
    virtual void writeCppProgram(std::ostream& out) = 0;
};

enum ProgrammingLanguage
{
    None,
    Cpp,
    CSharp,
    Java,
};

class Person :
    public GreetingAbstractBase,
    public QuestionAbstractBase
{
    std::string name;
    std::string excuse;
    ProgrammingLanguage languageCanProgram;
    int maxNumberCanHoldInHead;

public:
    Person(
        std::string&& name,
        std::string&& excuse,
        ProgrammingLanguage languageCanProgram,
        int maxNumberCanHoldInHead)

        : name(std::move(name))
        , excuse(std::move(excuse))
        , languageCanProgram(languageCanProgram)
        , maxNumberCanHoldInHead(maxNumberCanHoldInHead)
    {
    }

    void introduceSelf() override
    {
        std::cout << "Hi. My name is ";
        std::cout << name << std::endl;
    }

    void excuseSelf() override
    {
        std::cout << excuse << std::endl;
    }

    int computeSum(int a, int b) override
    {
        int result = a + b;
        return std::min(result, maxNumberCanHoldInHead);
    }

    void writeCppProgram(std::ostream& out) override
    {
        if (languageCanProgram == Cpp)
        {
            out << "int main() { return 0; }" << std::endl;
        }
    }
};

class Dog :
    public QuestionAbstractBase
{
    int favoriteNumber;

public:
    Dog(int favoriteNumber)
        : favoriteNumber(favoriteNumber)
    {
    }

    int computeSum(int, int) override
    {
        return favoriteNumber;
    }

    void writeCppProgram(std::ostream& out) override
    {
    }
};

void enterAndThenLeave(GreetingAbstractBase* object)
{
    object->introduceSelf();
    object->excuseSelf();
}

void quiz(QuestionAbstractBase* object)
{
    std::cout << "Question 1: What is 5 + 6?" << std::endl;
    std::cout << "Answer: " << object->computeSum(5, 6) << std::endl;

    std::cout << "Question 2: What is 10 + 20?" << std::endl;
    std::cout << "Answer: " << object->computeSum(5, 6) << std::endl;

    std::cout << "Question 3: Write a C++ program" << std::endl;
    object->writeCppProgram(std::cout);
}

int main()
{
    Person john{"John", "I'm not feeling well", Cpp, 30};
    Person jane{"Jane", "I gotta go", Java, 20};

    Dog husky{11};

    std::vector<QuestionAbstractBase*> objects{
        &john,
        &jane,
        &husky,
    };
    for (auto object : objects)
    {
        quiz(object);
    }

    std::vector<GreetingAbstractBase*> greetingsObjects{
        &john,
        &jane,
    };
    for (auto object : greetingsObjects)
    {
        enterAndThenLeave(object);
    }
}