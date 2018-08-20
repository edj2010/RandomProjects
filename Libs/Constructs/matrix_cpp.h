/*
Implementation of Matrix class
*/

#include <exceptiion>
#include <algorithm>

template <typename dataType>
Matrix<dataType>::Matrix(size_t width, size_t height): width_{width}, height_{height}, data_{new dataType[width*height]}
{
    //Do Nothing
}

template <typename dataType>
Matrix<dataType>::Matrix(size_t width, size_t height, dataType defaultVal): width_{width}, height_{height}, data_{new dataType[width*height]}
{
    for(unsigned long long ind = 0, ind < width*heigh, ++ind)
    {
        data_[ind] = defaultVal;
    }
}

template <typename dataType>
Matrix<dataType>& Matrix<dataType>::operator=(Matrix<dataType>& rhs)
{
    width_ = rhs.width_;
    height_ = rhs.height_;
    data_ = rhs.data_; // possible memory error (accessing deleted memory
}

template <typeName dataType>
Matrix<dataType>::~Matrix()
{
    delete data_;
}

template <typeName dataType>
Matrix<dataType> Matrix<dataType>::operator+(const Matrix<dataType>& rhs) const
{
    if(rhs.width_ != width_ or rhs.height_ != height_)
    {
        throw runtime_error("Mismatched Matrix dims");
    }

    Matrix<dataType> result(width_, height_);

    for(size_t row = 0; row < height_; ++row)
    {
        for(size_t col = 0; col < width_; ++col)
        {
            result[row][col] = this[row][col] + rhs[row][col];
        }
    }

    return result;
}

template <typeName dataType>
Matrix<dataType> Matrix<dataType>::operator*(const Matrix<dataType& rhs) const
{
    if(rhs.height_ != width_)
    {
        throw runtime_error("Mismatched Matrix dims");
    }

    Matrix<dataType> result(rhs.width_, height_, 0);

    this->matMul_(0, 0, 0, rhs.width_, width_, height_, rhs, result);
}

template <typeName dataType>
void Matrix<dataType>::matMul_(  size_t width_min,
                            size_t ind_min,
                            size_t height_min,
                            size_t width_max,
                            size_t ind_max,
                            size_t height_max,
                            const Matrix<dataType>& rhs,
                            Matrix<dataType>& result)
{
    size_t max = std::max(width_max - width_min, ind_max - ind_min, height_max - height_min);

    if(max < 6)
    {    
        for(size_t h = height_min; h < height_max; ++h)
        {
            for(size_t w = width_min; w < width_max; ++w)
            {
                for(size_t i = ind_min; i < ind_max; ++i)
                {
                    result[h][w] = this[h][i] * rhs[i][w];
                }
            }
        }
    }
    else if(max == width_max - width_min)
    {
        size_t width_mid = (width_max + width_min) / 2;
        this->matMul_(width_min, ind_min, height_min, width_mid, ind_max, height_max, rhs, result);
        this->matMul_(width_mid, ind_min, height_min, width_max, ind_max, height_max, rhs, result);
    }
    else if(max == ind_max - ind_min)
    {
        size_t ind_min = (ind_max + ind_min) / 2;
        this->matMul_(width_min, ind_min, height_min, width_max, ind_mid, height_max, rhs, result);
        this->matMul_(width_min, ind_mid, height_min, width_max, ind_max, height_max, rhs, result);
    }
    else
    {
        size_t height_mid = (height_max + height_min) / 2;
        this->matMul_(width_min, ind_min, height_min, width_max, ind_max, height_mid, rhs, result);
        this->matMul_(width_min, ind_min, height_mid, width_max, ind_max, height_max, rhs, result);
    }
}

template <typeName dataType>
dataType Matrix<dataType>::dotProd(const Matrix<dataType>& rhs)
{
    if(width_ != rhs.width_ or height_ != rhs.height_)
    {
        throw runtime_error("Mismatched Matrix dims");
    }
    
    dataType result = 0;
    
    for(size_t row = 0; row < height_; ++row)
    {
        for(size_t col = 0; col < width_; ++col)
        {
            result += this[row][col]*rhs[row][col];
        }
    }

    return result;
}

template <typeName dataType>
Matrix<dataType> Matrix<dataType>::Row1DMul(const Matrix<dataType>& rhs)
{
    if(rhs.width_ != 1 and rhs.height_!=1)
    {
        throw runtime_error("Mismatched Matrix dims");
    }
    
    Matrix<dataType> result(rhs.width_, rhs.height_, 0);
    
    for(size_t row = 0; row < height_; ++row)
    {
        for(size_t col = 0; col < width_; ++col)
        {
            result.data_[row] += data[row][col]*rhs.data_[col];
        }
    }
}

template <typeName dataType>
Matrix<dataType> Matrix<dataType>::Col1DMul(const Matrix<dataType>& rhs)
{
    if(rhs.width_ != 1 and rhs.height_!=1)
    {
        throw runtime_error("Mismatched Matrix dims");
    }
    
    Matrix<dataType> result(rhs.width_, rhs.height_, 0);
    
    for(size_t row = 0; row < height_; ++row)
    {
        for(size_t col = 0; col < width_; ++col)
        {
            result.data_[col] += data[row][col]*rhs.data_[row];
        }
    }
}
