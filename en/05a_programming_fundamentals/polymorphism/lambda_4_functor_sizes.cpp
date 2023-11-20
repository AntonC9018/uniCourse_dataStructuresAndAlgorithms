#include <cassert>

int main()
{
    int a = 0;

    {
        auto func = [=](){};
        size_t size = sizeof(func);
        assert(size == 1); // aka has no fields
    }

    {
        auto func = [=](){ return a; };
        size_t size = sizeof(func);
        assert(size == sizeof(int)); // single copy capture
    }

    {
        float b = 0;
        auto func = [&](){ 
            a += 2;
            b *= 2;
        };
        size_t size = sizeof(func);
        assert(size == 2 * sizeof(void*));
    }
}