from PyQt5.QtWidgets import QApplication
import sys
from minesweeper.qtclasses import MineSweeper

def main():
    app = QApplication(sys.argv)
    # app.setStyle("fusion")
    ex = MineSweeper()
    ex.show()
    app.exec_()

if __name__=='__main__':
    main()