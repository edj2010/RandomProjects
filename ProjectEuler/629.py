# Scatterstone Nim
# Calculate grundy number for each
# (minimum # unreachable)

grundyNums = dict()

def getParts(size, Max, count):
    if Max > size:
        return getParts(size, size, count)
    if size <= 0 or Max <= 0 or count <= 0:
        return list()
    if Max == 1:
        if count >= size:
            return [[1]*size]
        else:
            return list()
    ans = getParts(size, Max-1, count) + [[Max]+l for l in getParts(size-Max, Max, count-1)]
    if Max == size:
        ans += [[size]]
    return ans

def getNum(size, k):

    if size in grundyNums:
        return grundyNums[size]

    seen = set()
    
    for part in getParts(size, size-1, k):
        val = 0
        for el in part:
            val ^= getNum(el, k)

    for i in range(size):
        if i not in seen:
            grundyNums[size] = i
            return i
    
    return size # should never happen

def main():
    for i in range(1,100):
        print(i, getNum(i,2))

print(getParts(5,5,2))
