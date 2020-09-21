import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication,
                             QMainWindow, QAction, QMenu, QLayout, QHBoxLayout, QVBoxLayout, QLCDNumber,
                             QSpacerItem, QMessageBox)
from PyQt5.QtGui import QIcon
import PyQt5.QtCore
from PyQt5.QtCore import  QElapsedTimer, QTimer, QSize
from minesweeper.qtclasses import Gui_Board
import minesweeper.resources.resources


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
        self.resetBtn = QPushButton(self)
        self.resetBtn.clicked.connect(self.newBoard)
        #resetBtn.setText("Reset")
        self.resetBtn.setIcon(QIcon(":icons/smileyFace.png"))
        self.resetBtn.setIconSize(QSize(24, 24))
        self.resetBtn.setObjectName('resetBtn')
        spacer1 = QSpacerItem(0,0,PyQt5.QtWidgets.QSizePolicy.MinimumExpanding,PyQt5.QtWidgets.QSizePolicy.Minimum)
        spacer2 = QSpacerItem(0, 0, PyQt5.QtWidgets.QSizePolicy.MinimumExpanding, PyQt5.QtWidgets.QSizePolicy.Minimum)
        horizontalLayout.addWidget(self.mineCount)
        horizontalLayout.addSpacerItem(spacer1)
        horizontalLayout.addWidget(self.resetBtn)
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
        self.resetBtn.setIcon(QIcon(":icons/smileyFace.png"))
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
        self.resetBtn.setIcon(QIcon(":icons/loseFace.png"))

    def winner(self):
        message = QMessageBox(self)
        self.clock.stop()
        self.resetBtn.setIcon(QIcon(":icons/winFace.png"))
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
    # app.setStyle("fusion")
    ex = MineSweeper()
    ex.show()
    app.exec_()

if __name__=='__main__':
    main()