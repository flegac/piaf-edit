import sys

import pyqttango
from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QPushButton, QApplication

if __name__ == "__main__":
    pyqttango.init_resources()
    app = QApplication([])
    QtGui.QIcon.setThemeName('tango')
    win = QPushButton()
    win.setIconSize(QSize(128, 128))
    win.setIcon(QtGui.QIcon.fromTheme('accessories-calculator'))
    win.show()
    sys.exit(app.exec_())
