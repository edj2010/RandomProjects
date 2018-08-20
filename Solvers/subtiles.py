base = [
[ 0,  0,  0,  0,  0,  0,  0, 17,  0,  0,  0,  0, 14],
[ 0,  0,  0, 13, 13, 13,  0,  0,  0,  0,  0, 12,  0],
[ 0,  0,  0,  0,  0,  0,  0, 17,  3, 17,  0,  0,  0],
[ 0,  0,  0,  0,  0,  0, 16,  0,  0,  0,  0, 14,  0],
[13, 13, 17,  0,  0, 16,  0,  0,  0,  0, 12,  0,  0],
[ 0,  0,  0,  5, 16,  0,  0,  0,  0,  0,  0,  0,  0],
[ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
[ 0,  0,  0,  0,  0,  0,  0,  0, 10, 14,  0,  0,  0],
[ 0,  0,  9,  0,  0,  0,  0,  2,  0,  0, 11, 11,  8],
[ 0, 15,  0,  0,  0,  0, 10,  0,  0,  0,  0,  0,  0],
[ 0,  0,  0, 16, 16, 10,  0,  0,  0,  0,  0,  0,  0],
[ 0, 15,  0,  0,  0,  0,  0, 11, 15,  1,  0,  0,  0],
[ 9,  0,  0,  0,  0, 15,  0,  0,  0,  0,  0,  0,  0]]

start_num = 1

class vec:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __add__(self, rhs):
        return vec(self.a + rhs.a, self.b + rhs.b)

    def copy(self):
        return vec(self.a, self.b)

    def getAdj(self):
        return [self + vec(1,0), self + vec(0,1), self + vec(-1,0), self + vec(0,-1)]

class polyomino:

    def __init__(self):
        self.size = 0
        self.squares = list()

    def copy(self):
        p = polyomino()
        p.size = self.size
        p.squares = [s.copy() for s in self.squares]
        return p

    def getPosParents(self):
        newSquares = set()
        newOminos = list()
        for square in self.squares:
            newSquares.update(square.getAdj)
        for square in newSquares:
            omino = self.copy()
            omino.size += 1
            omino.squares.append(square)
            normalize(omino)
            newOminos.append(omino)
        return newOminos
