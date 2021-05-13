from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QDockWidget

from piafedit.ui_utils import load_ui


class TestUi(QDockWidget):

    def __init__(self):
        super().__init__()
        load_ui('ws_dock', self)
        self.show()


if __name__ == '__main__':
    app = QApplication([])
    win = TestUi()
    app.exec_()
