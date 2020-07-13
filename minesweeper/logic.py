import random

class Board:
    # beginner 8 x 8 - 10 mines
    # intermediate 16 x 16 - 40 mines
    # Expert 16 x 30 - 99 mines
    def __init__(self, number_mine=10, col=8, row=7):
        self.col = col
        self.row = row
        self.minesCount = number_mine
        self.board = []
        self.mines = []
        Board.setMines(self)
        Board.setBoard(self)
        # self.bomb_board = Board.place_mines(self)

    def setMines(self):
        """
        Create random set of mine location
        :return:
        """
        while len(self.mines) < self.minesCount:
            col = random.randint(0, self.col - 1)
            row = random.randint(0, self.row - 1)
            if (col, row) not in self.mines:
                self.mines.append((col, row))
        # create place mines in board row by row
        # Return an array of array where 9 are the mine and 0 empty.
        for row in range(self.row):
            singleRow = []
            for col in range(self.col):
                if (col, row) in self.mines:
                    singleRow.append(9)
                else:
                    singleRow.append(0)
            self.board.append(singleRow)
        return self.mines

    def setBoard(self):
        for row in range(self.row):
            #singleRow = self.board[row]
            for col in range(self.col):
                if (col, row) not in self.mines:
                    #mineAround = Board.getNumber(self, col, row)
                    #singleRow[col] = mineAround
                    self.board[row][col] = self.getNumber(col, row)
            #self.board[row] = singleRow

    def getNumber(self, col, row):
        """
        Function to get the number of mine around a given cell
        :param col:
        :param row:
        :return:
        """
        surrondings = []
        for y in range(-1, 2):
            for x in range(-1, 2):
                surrondings.append((col + x, row + y))
        number_mine = set(surrondings) & set(self.mines)
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
        for y in range(0, self.row):
            if y == 0:
                print(" " + self.col * (" " + 3 * '\u2015'))
            line = self.board[y]
            print("", end=" | ")
            for x in range(0, self.col):
                if line[x] == 0:
                    line[x] = " "
                elif line[x] == 9:
                    line[x] = "X"
                print(line[x], end=" | ")
            print("")
            print(" " + self.col * (" " + 3 * '\u2015'))

if __name__ == "__main__":
    board = Board()
    print(board.board)
    board.show()