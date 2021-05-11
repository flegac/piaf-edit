from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication


class TestUi(QWidget):

    def __init__(self):
        super().__init__()
        uic.loadUi(Path('../resources') / 'ui/test.ui', self)

        self.show()


if __name__ == '__main__':
    app = QApplication([])
    win = TestUi()
    app.exec_()
