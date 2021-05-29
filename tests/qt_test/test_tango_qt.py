from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QPushButton

from piafedit.ui_utils import gui_app

if __name__ == "__main__":
    with gui_app():
        win = QPushButton()
        win.setIconSize(QSize(128, 128))
        win.setIcon(QtGui.QIcon.fromTheme('accessories-calculator'))
        win.show()
