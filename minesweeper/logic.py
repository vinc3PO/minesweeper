import random

class Board:
    # beginner 8 x 8 - 10 mines
    # intermediate 16 x 16 - 40 mines
    # Expert 16 x 30 - 99 mines
    def __init__(self, number_mine=10, col=8, row=7):
        self.colCount = col
        self.rowCount = row
        self.minesCount = number_mine
        self.mines = self.setListMines()
        self.board = self.buildBoard()

    def buildBoard(self):
        board = []
        #print(board)
        for row in range(self.rowCount):
            singleRow = []
            for col in range(self.colCount):
                if (col, row) in self.mines:
                    singleRow.append("X")
                else:
                    singleRow.append(self.getNumber(col, row))
            board.append(singleRow)
        return board
        # First create list of mines

    def setListMines(self):
        print("mine list")
        minesCoord = []
        while len(minesCoord) < self.minesCount:
            col = random.randint(0, self.colCount - 1)
            row = random.randint(0, self.rowCount - 1)
            if (col, row) not in minesCoord:
                minesCoord.append((col, row))
        return minesCoord

    def getNumber(self, col, row):
        """
        Function to get the number of mine around a given cell
        :param col:
        :param row:
        :return:
        """
        surrounding = []
        for y in range(-1, 2):
            for x in range(-1, 2):
                surrounding.append((col + x, row + y))
        number_mine = set(surrounding) & set(self.mines)
        print(len(number_mine))
        return len(number_mine)

    def getMinesAround(self, col, row):
        """
        Function to check if a given cell a mine as a direct neighbour
        This is used to reveal all cell when an empty one is revealed.
        Not used anymore. Recursion done in the GUI level
        :param x_cell:
        :param y_cell:
        :return:
        """
        listEmpty = [(col, row)]
        listCells = [(col, row)]
        if self.board[row][col] != " ":
            return listCells
        for (i, j) in listEmpty:
            for y in range(j - 1, j + 2):
                for x in range(i - 1, i + 2):
                    # print(self.board[y][x])
                    if y >= 0 and y < self.row and x >= 0 and x < self.col:
                        if self.board[y][x] == " ":
                            if (x, y) not in listEmpty:
                                listEmpty.append((x, y))
                        if (x, y) not in listCells:
                            listCells.append((x, y))
        return listCells

    def show(self):
        for y in range(0, self.rowCount):
            if y == 0:
                print(" " + self.colCount * (" " + 3 * '\u2015'))
            line = self.board[y]
            print("", end=" | ")
            for x in range(0, self.colCount):
                if line[x] == 0:
                    line[x] = " "
                elif line[x] == 9:
                    line[x] = "X"
                print(line[x], end=" | ")
            print("")
            print(" " + self.colCount * (" " + 3 * '\u2015'))

if __name__ == "__main__":
    board = Board()
    print(board.board)
    #board.show()