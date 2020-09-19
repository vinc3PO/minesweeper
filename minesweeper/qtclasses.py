#!/usr/bin/env python

import sys
import random
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication,QLabel,
                             QFrame, QMainWindow, QAction, QMenu, QLayout, QHBoxLayout, QVBoxLayout, QLCDNumber,
                             QSpacerItem, QMessageBox)
from PyQt5.QtGui import QPixmap, QIcon
import PyQt5.QtCore
from PyQt5.QtCore import pyqtSignal, QElapsedTimer, QTimer
from minesweeper.logic import Board
import minesweeper.resources.resources




class Button(QPushButton):
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
            #self.setText("F")
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

    def __init__(self, mines_number, size, parent=None):
        super().__init__()
        self.x_board, self.y_board = size
        self.new_board = Board(mines_number, self.x_board, self.y_board)
        self.parent = parent
        self.mines_number = mines_number
        self.minesLeft = self.mines_number
        self.lockButton = False
        self.grid = None
        self.topLayout = QHBoxLayout()
        resetButton = QPushButton()
        #todo add smiley face
        resetButton.setText('Reset')
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
            self.grid.setColumnMinimumWidth(j,15)
            self.grid.setRowMinimumHeight(i,15)
            self.grid.addWidget(button, *(i, j))
        self.grid.setSpacing(0)
        self.minesLeft = self.mines_number

    def btnClicked(self, i=None, j=None):
        if not i and not j:
            i, j = (int(i) for i in self.sender().objectName().split(","))
        if (i, j) not in self.new_board.mines:
            self.btnRemoval(i, j)
            if self.firstClick:
                self.gameStart.emit()
                self.firstClick = False
            if self.countButtonLeft() == self.mines_number:
                self.gameWin.emit()
        else:
            if self.firstClick:
                # No mine in the first click
                while (i, j) in self.new_board.mines:
                    self.new_board = Board(self.mines_number, self.x_board, self.y_board)
                self.btnClicked(i,j)
            else:
                self.btnRemoval(i, j, firstBomb=True)
                self.flagClearing()
                self.gameOver.emit()
                self.lockButton = True


    def countButtonLeft(self):
        count = 0
        for i in range(self.grid.count()):
            try:
                if isinstance(self.grid.itemAt(i).widget(), QPushButton):
                    count +=1
            except:
                print(sys.exc_info())
        return count

    def btnRemoval(self, x, y, loop=None, firstBomb=None):
        widg = self.grid.itemAtPosition(x, y).widget()
        if widg is not None and isinstance(widg, QLabel) is False:
            widg.setParent(None)
            name = self.new_board.board[y][x]
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
                        except:
                            pass
            except:
                pass

            if (x, y) in self.new_board.mines and loop is None:
                print("minessssssssssss")
                "clear all the mine when blew up."
                for (i, j) in self.new_board.mines:
                    try:
                        if self.grid.itemAtPosition(i, j).widget().state !=1:
                            self.btnRemoval(i, j, loop=True)
                    except:
                        print(sys.exc_info())
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
                    if self.grid.itemAtPosition(i,j).widget().state ==1 and (i, j) not in self.new_board.mines:
                        self.grid.itemAtPosition(i, j).widget().setIcon(QIcon(":icons/flag_not.png"))
                except:
                    print(sys.exc_info())
                    pass

class MineSweeper(QMainWindow):
    def __init__(self, parent=None):
        super(MineSweeper, self).__init__(parent)
        ###  --  Start with the menu bar  --  ###
        self.barMenu = self.menuBar()
        menu = QMenu("&File", self.barMenu)
        beginner = QAction(menu)
        beginner.setText("&Beginner")
        beginner.setObjectName("beginner")
        intermediate = QAction(menu)
        intermediate.setText("&Intermediate")
        intermediate.setObjectName("intermediate")
        expert = QAction(menu)
        expert.setText("&Expert")
        expert.setObjectName("expert")
        exitAction = QAction(menu)
        exitAction.setText("&Exit")
        beginner.triggered.connect(self.newBoard)
        intermediate.triggered.connect(self.newBoard)
        expert.triggered.connect(self.newBoard)
        exitAction.triggered.connect(self.close)
        menu.addAction(beginner)
        menu.addAction(intermediate)
        menu.addAction(expert)
        menu.addSeparator()
        menu.addAction(exitAction)

        self.barMenu.addMenu(menu)
        ### -- Rest of the widget  --  ###
        centralWidg = QWidget(self)
        verticalLayout = QVBoxLayout(centralWidg)
        verticalLayout.setSizeConstraint(QLayout.SetFixedSize)
        horizontalLayout = QHBoxLayout()
        self.setCentralWidget(centralWidg)
        self.scoreBoard = QLCDNumber(self)
        self.mineCount = QLCDNumber(self)
        self.mines = 99
        self.boardSize=(16, 30)
        self.board = Gui_Board(self.mines, self.boardSize, self)
        resetBtn = QPushButton(self)
        resetBtn.clicked.connect(self.newBoard)
        resetBtn.setText("Reset")
        resetBtn.setObjectName('resetBtn')
        spacer1 = QSpacerItem(0,0,PyQt5.QtWidgets.QSizePolicy.MinimumExpanding,PyQt5.QtWidgets.QSizePolicy.Minimum)
        spacer2 = QSpacerItem(0, 0, PyQt5.QtWidgets.QSizePolicy.MinimumExpanding, PyQt5.QtWidgets.QSizePolicy.Minimum)
        horizontalLayout.addWidget(self.mineCount)
        horizontalLayout.addSpacerItem(spacer1)
        horizontalLayout.addWidget(resetBtn)
        horizontalLayout.addSpacerItem(spacer2)
        horizontalLayout.addWidget(self.scoreBoard)
        verticalLayout.addLayout(horizontalLayout)
        verticalLayout.addWidget(self.board)
        self.verticalLayout = verticalLayout
        self.timer = QElapsedTimer()
        self.clock = QTimer(self)
        self.clock.timeout.connect(self.showTime)
        self.status_bar = self.statusBar()
        # self.statusBar().showMessage('Time to be added')
        self.setWindowTitle('Minesweeper')
        self.setFixedSize(self.sizeHint())
        self.boardSignals()
        self.mineCount.display(self.mines)



    def boardSignals(self):
        self.board.gameOver.connect(self.gameOver)
        self.board.gameStart.connect(self.timerStart)
        self.board.mineleft.connect(self.updateMine)
        self.board.gameWin.connect(self.winner)

    def newBoard(self):
        sender = self.sender().objectName()
        if sender == "beginner":
            self.mines = 10
            self.boardSize = (8, 8)
        elif sender == "intermediate":
            self.mines = 40
            self.boardSize = (16, 16)
        elif sender == "expert":
            self.mines = 99
            self.boardSize = (16, 30)
        else:
            pass
        self.board.setParent(None)
        self.board = Gui_Board(self.mines, self.boardSize, self)
        self.verticalLayout.addWidget(self.board)
        QApplication.processEvents()  # has to be here to process resizing properly
        self.setFixedSize(self.sizeHint())
        self.boardSignals()
        self.clock.stop()
        self.clearClock()
        self.status_bar.showMessage("")
        self.mineCount.display(self.mines)

    def gameOver(self):
        self.status_bar.showMessage("GAME OVER in {} second".format(self.timer.elapsed()/1000))
        self.clock.stop()
        print("Game is OVER in {}".format(self.timer.elapsed()))

    def winner(self):
        message = QMessageBox(self)
        self.clock.stop()
        message.setText("Congratulation!\nDone in {} seconds".format(self.timer.elapsed()/1000))
        message.show()

    def timerStart(self):
        self.clock.start(1000)
        self.timer.start()
        self.showTime()

    def showTime(self):
        self.scoreBoard.display(round(self.timer.elapsed()/1000))

    def clearClock(self):
        self.scoreBoard.display(0)

    def updateMine(self, mine):
        self.mineCount.display(mine)

def main():
    app = QApplication(sys.argv)
    ex = MineSweeper()
    ex.show()
    app.exec_()


if __name__ == '__main__':
    main()


