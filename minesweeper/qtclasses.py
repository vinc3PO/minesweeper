#!/usr/bin/env python

import sys
import random
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication,QLabel,
                             QFrame, QMainWindow, QAction, QMenu, QLayout, QHBoxLayout, QVBoxLayout, QLCDNumber,
                             QSpacerItem)
import PyQt5.QtCore
from PyQt5.QtCore import pyqtSignal
from minesweeper.logic import Board


class Button(QPushButton):
    flagSignal = pyqtSignal(int)
    def __init__(self, parent=None):
        super(Button, self).__init__()
        self.state = 0
        self.parent = parent

    def mousePressEvent(self, QMouseEvent):
        if self.text() == "" and self.parent.lockButton is False:
            super(Button, self).mousePressEvent(QMouseEvent)
        if QMouseEvent.button() == 2 and self.parent.lockButton is False:
            self.changeText()

    def changeText(self):
        self.state += 1
        if self.state == 1:
            self.setText("F")
            self.flagSignal.emit(0)
        elif self.state == 2:
            self.setText("?")
            self.flagSignal.emit(1)
        else:
            self.setText("")
            self.state = 0



class Gui_Board(QWidget):

    COLOR = {
        "1": "color:blue",
        "2": "color:green",
        "3": "color:red",
        "4": "color:purple",
        "5": "color:brown",
        "6": "color:turquoise",
        "7": "color:black",
        "8": "color:gray"
    }
    gameOver = pyqtSignal()

    def __init__(self, mines_number, x_board, y_board, parent=None):
        super().__init__()
        self.new_board = Board(mines_number, x_board, y_board)
        self.parent = parent
        self.mines_number = mines_number
        self.minesLeft = self.mines_number
        self.x_board = x_board
        self.y_board = y_board
        self.lockButton = False
        self.grid = None
        self.topLayout = QHBoxLayout()
        resetButton = QPushButton()
        resetButton.setText('Reset')
        self.firstClick = True
        print(self.new_board.mines)
        self.initUI()

        
    def initUI(self):
        if self.grid is None:
            self.grid = QGridLayout()
            self.setLayout(self.grid)
        self.firstClick = True
        positions = [(i, j) for i in range(self.x_board) for j in range(self.y_board)]
        for (i, j) in positions:
            button = Button(self)
            button.setFixedSize(35,35)
            button.setObjectName('{!s},{!s}'.format(i, j))
            button.clicked.connect(self.btnClicked)
            button.flagSignal.connect(self.flagAdded)
            #button.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
            #button.setStyleSheet("QLabel{background-color:transparent; border:1px solid grey};")
            self.grid.setColumnMinimumWidth(j,15)
            self.grid.setRowMinimumHeight(i,15)
            self.grid.addWidget(button, *(i, j))
        self.grid.setSpacing(0)
        self.minesLeft = self.mines_number
        self.parent.mineCount.display(self.minesLeft)
    
    def refresh(self):
        for i in reversed(range(self.grid.count())):
            try:
                self.grid.itemAt(i).widget().setParent(None)
            except:
                print(sys.exc_info())
        self.new_board = Board(self.mines_number,self.x_board,self.y_board)
        self.initUI()
        self.lockButton = False

    def btnClicked(self):
        print('clicked {}'.format(self.sender().objectName()))
        position = self.sender().objectName().split(",")
        i = int(position[0])
        j = int(position[1])
        if (i, j) in self.new_board.mines:
            if self.firstClick:
                while (i, j) in self.new_board.mines:
                    print("Mine on the first click")
                    self.new_board = Board(self.mines_number, self.x_board, self.y_board)
                    print(self.new_board.mines)
            else:
                self.gameOver.emit()
                self.lockButton = True
        self.btnRemoval(i, j)
        self.firstClick = False

    def btnRemoval(self, x, y):
        widg = self.grid.itemAtPosition(x, y).widget()
        if widg is not None and isinstance(widg, QLabel) is False:
            widg.setParent(None)
            name = self.new_board.board[y][x]
            empty = False
            if name == 0:
                name = " "
                empty = True
            elif name == 9:
                name = "X"
            else:
                name = str(name)
            label = QLabel(name)
            label.setFixedSize(35, 35)
            label.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
            if name == " " or name == "X":
                label.setStyleSheet("QLabel{background-color:transparent;font:14pt ; border:1px solid grey;}")
            else:
                label.setStyleSheet(
                    "QLabel{{background-color:transparent; border:1px solid grey; font:14pt ;{0};}}".format(self.COLOR[str(name)]))
            self.grid.addWidget(label, *(x, y))
            if empty is True:
                for i in range(x-1, x+2):
                    for j in range(y-1, y+2):
                        try:
                            self.btnRemoval(i, j)
                        except:
                            pass
            if (x, y) in self.new_board.mines:
                for (i, j) in self.new_board.mines:
                    self.btnRemoval(i, j)

    def flagAdded(self, value):
        print(self.minesLeft)
        print(value)
        if value == 0:
            self.minesLeft +=-1
        else:
            self.minesLeft +=1
        self.parent.mineCount.display(self.minesLeft)


class MineSweeper(QMainWindow):
    def __init__(self, parent=None):
        super(MineSweeper, self).__init__(parent)
        menu_bar = self.menuBar()
        #file_menu = menu_bar.addMenu("&File")
        #new_action = QAction('&New', self)
        #new_action.triggered.connect(self.NewBoard)
        #file_menu.addAction(new_action)
        centralWidg = QWidget(self)
        verticalLayout = QVBoxLayout(centralWidg)
        horizontalLayout = QHBoxLayout()
        self.setCentralWidget(centralWidg)
        scoreBoard = QLCDNumber(self)
        self.mineCount = QLCDNumber(self)
        self.board = Gui_Board(99, 16, 30, self)
        resetBtn = QPushButton(self)
        resetBtn.clicked.connect(self.NewBoard)
        resetBtn.setText("Reset")
        spacer1 = QSpacerItem(0,0,PyQt5.QtWidgets.QSizePolicy.MinimumExpanding,PyQt5.QtWidgets.QSizePolicy.Minimum)
        spacer2 = QSpacerItem(0, 0, PyQt5.QtWidgets.QSizePolicy.MinimumExpanding, PyQt5.QtWidgets.QSizePolicy.Minimum)
        horizontalLayout.addWidget(self.mineCount)
        horizontalLayout.addSpacerItem(spacer1)
        horizontalLayout.addWidget(resetBtn)
        horizontalLayout.addSpacerItem(spacer2)
        horizontalLayout.addWidget(scoreBoard)
        verticalLayout.addLayout(horizontalLayout)
        verticalLayout.addWidget(self.board)
        
        self.status_bar = self.statusBar()
        self.statusBar().showMessage('Time to be added')
        self.setWindowTitle('Minesweeper')
        self.board.gameOver.connect(self.gameOver)

        
    def NewBoard(self):
        #self.close()
        self.board.refresh()

    def gameOver(self):
        print("Game is OVER")

def main():
    #b = Board(40,16,16)
    #b.show()
    #tuple_input_x = input("Enter x \n")
    #tuple_input_y = input("enter y \n")
    #print(b.find_surronding(int(tuple_input_x),int(tuple_input_y)))
    app = QApplication(sys.argv)
    #app.setStyle("fusion")
    ex = MineSweeper()
    ex.show()
    app.exec_()


if __name__=='__main__':
    main()


