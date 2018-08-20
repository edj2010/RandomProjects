/*
Matrix class

Provides wrapper that creates matricies, stores them with minimal overhead
Handles multiplication (scalar and constant) and addition.
*/

#include <cstddef>

template <typeName dataType>
class Matrix
{

        size_t width_, height_;

        dataType* data_;

    public:

        Matrix() = delete;
        Matrix(size_t, size_t); // default constructor
        Matrix(size_t, size_t, dataType); // default value constructor
        Matrix<dataType>& operator=(const Matrix<dataType>&);

        ~Matrix();

        Matrix<dataType> operator+(const Matrix<dataType>&) const;
        Matrix<dataType> operator*(const Matrix<dataType>&) const;
        dataType dotProd(const Matrix<dataType>&) const;
        Matrix<dataType> Row1DMul(const Matrix<dataType>&) const;
        Matrix<dataType> Col1DMul(const Matrix<dataType>&) const;

        dataType* operator[](const size_t index) const;

    private:

        void matMul_(size_t, size_t, size_t, size_t, size_t, size_t, const Matrix<dataType>&, Matrix<dataType>&);

};

#include "matrix_cpp.h"
