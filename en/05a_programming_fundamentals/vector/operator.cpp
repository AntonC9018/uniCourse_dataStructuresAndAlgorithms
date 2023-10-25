struct Vector
{
    int x;
    int y;

    Vector operator+(Vector other) const
    {
        Vector result;
        result.x = this->x + other.x;
        result.y = this->y + other.y;
        return result;
    }

    Vector operator-(Vector other) const
    {
        Vector result;
        result.x = this->x - other.x;
        result.y = this->y - other.y;
        return result;
    }

    Vector operator*(int scalar) const
    {
        Vector result;
        result.x = this->x * scalar;
        result.y = this->y * scalar;
        return result;
    }
};


int main()
{
    Vector a{1, 2};
    Vector b{3, 4};

    Vector result = a + b;
    result = result * 5 - a;
    result = result + b;

    return 0;
}