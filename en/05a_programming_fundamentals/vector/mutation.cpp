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

    Vector& operator+=(const Vector& other)
    {
        *this = *this + other;
        return *this;
    }

    Vector& operator-=(const Vector& other)
    {
        *this = *this - other;
        return *this;
    }

    Vector& operator*=(int scalar)
    {
        *this = *this * scalar;
        return *this;
    }
};


int main()
{
    Vector a{1, 2};
    Vector b{3, 4};

    Vector result = a + b;
    // You CAN do stuff like this, because it returns a reference.
    (result *= 5) -= a;
    result += b;

    return 0;
}