struct Vector
{
    int x;
    int y;
};

Vector add(Vector a, Vector b)
{
    Vector result;
    result.x = a.x + b.x;
    result.y = a.y + b.y;
    return result;
}

Vector subtract(Vector a, Vector b)
{
    Vector result;
    result.x = a.x - b.x;
    result.y = a.y - b.y;
    return result;
}

Vector scale(Vector a, int scalar)
{
    Vector result;
    result.x = a.x * scalar;
    result.y = a.y * scalar;
    return result;
}

int main()
{
    Vector a{1, 2};
    Vector b{3, 4};

    Vector result = add(a, b);
    result = subtract(scale(result, 5), a);
    result = add(result, b);

    return 0;
}