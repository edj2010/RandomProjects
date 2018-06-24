# Solver for logic pic puzzle

import functools

class gameState:
    
    def __init__(self, width, height, rowCons, colCons):
        self.width = width
        self.height = height
        self.state = [[0]*self.width for _ in range(self.height)]
        # 0 is unknown, -1 is known empty, 1 is known full
        self.rowCons = rowCons
        self.colCons = colCons
        self.solvable = True
    
    def _copy(self, other):
        self.width = other.width
        self.height = other.height
        self.state = [list(row) for row in other.state]
        self.rowCons = other.rowCons # immutable
        self.colCons = other.colCons # immutable

    def _genKnownSquares(self, posSquares):
        # for each square, set to known only if among possible
        # values, only one option exists
        return [sum(set(square)) for square in zip(*posSquares)]

    def _partitions(self, count, base):
        if len(base) == 1:
            return [[base[0]+count]]
        return [[base[0] + i] + rest
                    for i in range(count+1)
                    for rest in self._partitions(count - i, base[1:])]

    def _genPosSquares(self, cons, maxLen):
        base = [0] + ([1]*(len(cons)-1)) + [0]
        freeSpace = maxLen - sum(base) - sum(cons)
        spaceDistros = self._partitions(freeSpace, base)
        lines = [sum([[-1]*distro[i] + [1]*cons[i]
                    for i in range(len(cons))], list()) + [-1]*distro[-1]
                        for distro in spaceDistros]
        return lines

    def _lineFits(self, line, linebase):
        return len([a*b for a, b in zip(line,linebase) if a*b < 0]) == 0

    def _getPosSquaresCons(self, cons, known, maxLen):
        return list(filter(lambda x: self._lineFits(x, known), self._genPosSquares(cons, maxLen)))

    def _getNewKnown(self, cons, known, maxLen):
        if cons == [0]:
            return [-1]*maxLen
        return [sum(set(square))
                    for square in zip(*(self._getPosSquaresCons(cons, known, maxLen)))]

    def _switchBoardAxes(self):
        self.state = list(zip(*(self.state)))

        temp = self.rowCons
        self.rowCons = self.colCons
        self.colCons = temp

        temp = self.width
        self.width = self.height
        self.height = temp

    def _advanceGameStateRow(self): # returns if anything was changed
        changed = False
        for i,row in enumerate(self.rowCons):
            newRow = self._getNewKnown(row, self.state[i], self.width)
            if not newRow:
                self.solvable = False
                return False
            if newRow != list(self.state[i]):
                changed = True
            self.state[i] = newRow
        return changed

    def _advanceGameState(self):
        changed = False
        changed |= self._advanceGameStateRow()
        if not self.solvable:
            return False
        self._switchBoardAxes()
        changed |= self._advanceGameStateRow()
        if not self.solvable:
            return False
        self._switchBoardAxes()
        return changed

    def _solved(self):
        return sum([1 for row in self.state for x in row if x == 0]) == 0

    def __str__(self):
        s = ""
        for row in self.state:
            for sq in row:
                if sq == 1:
                    s += "1 "
                elif sq == -1:
                    s += "0 "
                else:
                    s += "X "
            s += "\n"
        return s

    def solve(self):
        while self._advanceGameState():
            if not self.solvable:
                return False
        if not self._solved():
            for i in range(self.height):
                possibilities = self._getPosSquaresCons(self.rowCons[i], self.state[i], self.width)
                if len(possibilities) == 1:
                    continue
                if len(possibilities) == 0:
                    return False
                for p in possibilities:
                    other = gameState(0, 0, 0, 0)
                    other._copy(self)
                    other.state[i] = p
                    other.solve()
                break
        else:
            print(self)
        return True

g = gameState(16,18,[   [6],
                        [2, 3],
                        [2, 2],
                        [1, 2],
                        [2, 1],
                        [1, 2, 1],
                        [1, 2, 3],
                        [1, 3],
                        [2, 4],
                        [2, 1, 1, 2],
                        [2, 6, 2],
                        [1, 2, 5, 2],
                        [2, 5, 1, 2],
                        [2, 7],
                        [3, 3, 2],
                        [2, 6, 1],
                        [2, 3, 4],
                        [2, 3, 2]],
                    [   [3],
                        [2, 1],
                        [3, 2, 1],
                        [3, 2, 1],
                        [1, 1],
                        [1, 2, 2],
                        [2, 2, 1, 6],
                        [1, 2, 5, 1],
                        [1, 3, 3],
                        [1, 4, 3],
                        [2, 1, 7],
                        [2, 1, 3, 1],
                        [2, 1, 1, 5],
                        [2, 3, 1, 1, 2],
                        [7, 4, 2],
                        [4, 7]])
g.solve()


