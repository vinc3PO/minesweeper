from PyQt5.QtWidgets import QApplication
import sys
from minesweeper.minesweeper import MineSweeper

if __name__=='__main__':
    app = QApplication(sys.argv)
    # app.setStyle("fusion")
    ex = MineSweeper()
    ex.show()
    app.exec_()