
import sys

# https://github.com/PyQt5/Examples/blob/master/PySide2/3d/simple3d.py
from PySide2.QtWidgets import QApplication

from windows.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    p = app.exec_()

    sys.exit(p)
