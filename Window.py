import sys

import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic.properties import QtWidgets


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(400, 400, 400, 300)
    win.setWindowTitle("Pyqt5 Tutorial")
    win.show()
    sys.exit(app.exec_())
