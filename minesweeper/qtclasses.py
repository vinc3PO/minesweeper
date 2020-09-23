#!/usr/bin/env python

import sys
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication,QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
import PyQt5.QtCore
from PyQt5.QtCore import pyqtSignal
from minesweeper.logic import Board




class Button(QPushButton):
    """
    Class of a tristate button
    0: No flags
    1: flag flag
    2: ? flag
    Button emit a signal when toggle by right click
    """
    flagSignal = pyqtSignal(int)
    def __init__(self, parent=None):
        super(Button, self).__init__()
        self.state = 0
        self.parent = parent

    def mousePressEvent(self, QMouseEvent):
        if self.parent.lockButton is False:
            super(Button, self).mousePressEvent(QMouseEvent)
        if QMouseEvent.button() == 2 and self.parent.lockButton is False:
            self.changeText()

    def changeText(self):
        self.state += 1
        if self.state == 1:
            self.setIcon(QIcon(":icons/flag.png"))
            self.flagSignal.emit(0)
            self.setIconSize(self.rect().size())
        elif self.state == 2:
            self.setIcon(QIcon())
            self.setText("?")
            self.flagSignal.emit(1)
        else:
            self.setText("")
            self.state = 0



class Gui_Board(QWidget):
    """
    Grid Widget that correspond to the minesweeper board.
    Widget only display what was created by the board in the logic module.
    When push button is instanciated it is name by its position.
    """

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
    gameStart = pyqtSignal()
    mineleft = pyqtSignal(int)
    gameWin = pyqtSignal()

    def __init__(self, minesCount, size, parent=None):
        super().__init__()
        self.x_board, self.y_board = size
        self.board = Board(minesCount, self.x_board, self.y_board)
        self.parent = parent
        self.minesCount = minesCount
        self.minesLeft = self.minesCount
        self.lockButton = False
        self.grid = None
        self.initUI()
        
    def initUI(self):
        """
        Initialisation/reload of the board widget/
        :return:
        """
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
            self.grid.setColumnMinimumWidth(j, 15)
            self.grid.setRowMinimumHeight(i, 15)
            self.grid.addWidget(button, *(i, j))
        self.grid.setSpacing(0)
        self.minesLeft = self.minesCount

    def btnClicked(self, i=None, j=None):
        """
        Button clicked signal
        :param i: row
        :param j: column
        :return: None
        """
        if not all([i, j]):
            i, j = (int(i) for i in self.sender().objectName().split(","))
        if (i, j) not in self.board.mines:
            self.btnRemoval(i, j)
            if self.firstClick:
                self.gameStart.emit()
                self.firstClick = False
            if self.countButtonLeft() == self.minesCount:
                self.gameWin.emit()
        else:
            if self.firstClick:
                # No mine in the first click
                while (i, j) in self.board.mines:
                    self.board = Board(self.minesCount, self.x_board, self.y_board)
                self.btnClicked(i,j)
            else:
                self.btnRemoval(i, j, firstBomb=True)
                self.flagClearing()
                self.gameOver.emit()
                self.lockButton = True


    def countButtonLeft(self):
        """
        Function used to count the number of push button left
        This is used to tell when only bomb are left uncovered
        :return:
        """
        count = 0
        for i in range(self.grid.count()):
            try:
                if isinstance(self.grid.itemAt(i).widget(), QPushButton):
                    count +=1
            except Exception:
                pass
        return count

    def btnRemoval(self, x, y, loop=None, firstBomb=None):
        """
        remove the button. Can recursively remove button when empty
        :param x: row
        :param y: column
        :param loop:  Recursion
        :param firstBomb: First bomb uncovered.
        :return:
        """
        widg = self.grid.itemAtPosition(x, y).widget()
        if widg is not None and isinstance(widg, QLabel) is False:
            widg.setParent(None)
            name = self.board.board[y][x]
            if name == 0:
                name = " "
                empty = True
            elif name == "X":
                name = ":/icons/bomb.png"
                #name = "X" # meaning that is a bomb
            else:
                name = str(name)

            if len(name)> 2:
                label = QLabel()
                label.setPixmap(QPixmap(name))
            else:
                label = QLabel(name)
            label.setFixedSize(35, 35)
            label.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
            if name == " " or len(name) > 2:
                label.setStyleSheet("QLabel{background-color:transparent;font:14pt ; border:1px solid grey;}")
                if firstBomb is not None:
                    label.setStyleSheet("QLabel{background-color:red;font:14pt ; border:1px solid grey;}")
            else:
                label.setStyleSheet(
                    "QLabel{{background-color:transparent; border:1px solid grey; font:14pt ;{0};}}".format(self.COLOR[str(name)]))
            self.grid.addWidget(label, *(x, y))
            try:
                empty
                for i in range(x-1, x+2):
                    for j in range(y-1, y+2):
                        try:
                            self.btnRemoval(i, j)
                        except Exception:
                            pass
            except Exception:
                pass

            if (x, y) in self.board.mines and loop is None:
                "clear all the mine when blew up."
                for (i, j) in self.board.mines:
                    try:
                        if self.grid.itemAtPosition(i, j).widget().state !=1:
                            self.btnRemoval(i, j, loop=True)
                    except Exception:
                        pass

    def flagAdded(self, value):
        if value == 0:
            self.minesLeft +=-1
        else:
            self.minesLeft +=1
        self.mineleft.emit(self.minesLeft)

    def flagClearing(self):
        for i in range(self.x_board):
            for j in range(self.y_board):
                try:
                    if self.grid.itemAtPosition(i,j).widget().state ==1 and (i, j) not in self.board.mines:
                        self.grid.itemAtPosition(i, j).widget().setIcon(QIcon(":icons/flag_not.png"))
                except Exception:
                    pass