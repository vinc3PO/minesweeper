import random

class Board:
    # beginner 8 x 8 - 10 mines
    # intermediate 16 x 16 - 40 mines
    # Expert 16 x 30 - 99 mines
    def __init__(self, number_mine, x_board, y_board):
        self.x_board = x_board
        self.y_board = y_board
        self.mine_number = number_mine
        self.board = []
        self.mines = []
        Board.place_mines(self)
        Board.place_number(self)
        # self.bomb_board = Board.place_mines(self)

    def place_mines(self):
        while len(self.mines) < self.mine_number:
            rand_x = random.randint(0, self.x_board - 1)
            rand_y = random.randint(0, self.y_board - 1)
            if (rand_x, rand_y) not in self.mines:
                self.mines.append((rand_x, rand_y))
        for y_line in range(0, self.y_board):
            line_board = []
            for x_line in range(0, self.x_board):
                if (x_line, y_line) in self.mines:
                    line_board.append(9)
                else:
                    line_board.append(0)
            self.board.append(line_board)
        return self.mines

    def place_number(self):
        for y_line in range(0, self.y_board):
            line_board = self.board[y_line]
            for x_line in range(0, self.x_board):
                if (x_line, y_line) not in self.mines:
                    number_mine = Board.mine_number(self, x_line, y_line)
                    line_board[x_line] = number_mine
            self.board[y_line] = line_board

    def mine_number(self, x_board, y_board):
        list_surrondings = []
        for y in range(-1, 2):
            for x in range(-1, 2):
                list_surrondings.append((x_board + x, y_board + y))
        number_mine = set(list_surrondings) & set(self.mines)
        return len(number_mine)

    def find_surronding(self, x_cell, y_cell):
        list_surrondings = [(x_cell, y_cell)]
        list_total = [(x_cell, y_cell)]
        if self.board[y_cell][x_cell] != " ":
            return list_total
        for (i, j) in list_surrondings:
            for y in range(j - 1, j + 2):
                for x in range(i - 1, i + 2):
                    # print(self.board[y][x])
                    if y >= 0 and y < self.y_board and x >= 0 and x < self.x_board:
                        if self.board[y][x] == " ":
                            if (x, y) not in list_surrondings:
                                list_surrondings.append((x, y))
                        if (x, y) not in list_total:
                            list_total.append((x, y))
        print(list_surrondings)
        print(list_total)
        return list_total

    def show(self):
        for y in range(0, self.y_board):
            if y == 0:
                print(" " + self.x_board * (" " + 3 * '\u2015'))
            line = self.board[y]
            print("", end=" | ")
            for x in range(0, self.x_board):
                if line[x] == 0:
                    line[x] = " "
                elif line[x] == 9:
                    line[x] = "X"
                print(line[x], end=" | ")
            print("")
            print(" " + self.x_board * (" " + 3 * '\u2015'))
