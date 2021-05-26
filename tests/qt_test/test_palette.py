import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QColorDialog

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = QColorDialog()

    window.show()
    sys.exit(app.exec_())
