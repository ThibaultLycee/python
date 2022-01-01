import copy

class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.makeRows()
        self.makeCols()
        self.makeSquares()
    
    def __repr__(self):
        rep = ""
        for i in self.rows:
            rep += f'{i}\n'
        return rep

    def makeRows(self): self.rows = [row for row in self.grid]
    def makeCols(self): self.cols = [[self.grid[y][x] for y in range(9)] for x in range(9)]
    def makeSquares(self): self.squares = [[self.rows[X*3+x][Y*3+y] for y in range(3) for x in range(3)] for Y in range(3) for X in range(3) ]

    def isFinished(self):
        for a in self.rows:
            for i in range(1, 10):
                if not i in a: return False
        for a in self.cols:
            for i in range(1, 10):
                if not i in a: return False
        for a in self.squares:
            for i in range(1, 10):
                if not i in a: return False
        print('Vérifié, correct')
        return True
    
    def isValidPosFor(self, nbre, case):
        if nbre in self.rows[case[0]]: return False
        if nbre in self.cols[case[1]]: return False
        if nbre in self.squares[(case[1] * 3 + case[0]) // 9]: return False
        return True

    def findFirstEmpty(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 'x':
                    return (i, j)  # row, col

        return None

    def copy(self):
        return Grid(copy.deepcopy(self.grid))

    def solve(self):
        empty = self.findFirstEmpty()
        print(empty)

        if empty == None:
            return self
        
        row, col = empty

        for nbre in range(1, 10):
            if self.isValidPosFor(nbre, (row, col)):
                nextGrid = self.copy()
                nextGrid.grid[row][col] = nbre
                solved = nextGrid.solve()
                if solved != False:
                    return nextGrid
        
        return False




gridPattern = [
    [2, 6, 3, 1, 4, 9, 7, 5, 8],
    [7, 1, 4, 2, 8, 5, 3, 6, 9],
    [9, 8, 5, 6, 3, 7, 1, 2, 4],
    [3, 7, 8, 9, 1, 2, 5, 4, 6],
    [1, 2, 9, 5, 6, 4, 8, 7, 3],
    [4, 5, 6, 3, 7, 8, 2, 9, 1],
    [6, 3, 2, 4, 5, 1, 9, 8, 7],
    [8, 9, 1, 7, 2, 6, 4, 3, 5],
    [5, 4, 7, 8, 9, 3, 6, 1, 2]
]
x = 'x'
gridPattern2 = [
    [x, 6, x, 4, x, x, x, 9, 2],
    [x, 2, 5, x, x, x, 4, x, x],
    [7, 4, x, 2, 3, 9, x, x, x],
    [5, 9, 6, x, 2, x, x, x, 1],
    [4, x, x, x, x, 5, x, 7, x],
    [2, 8, 7, x, 4, x, x, x, x],
    [x, 7, x, 8, x, 2, x, 1, 5],
    [8, x, x, 5, x, 7, 3, x, x],
    [x, 5, x, x, x, 4, x, x, x]
]

grid = Grid(gridPattern2)
print(grid)
print(grid.solve())