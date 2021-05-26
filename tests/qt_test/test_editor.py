import sys

from PyQt5 import QtWidgets
from qutepart import Qutepart

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    editor = Qutepart()
    editor.completionEnabled = True
    with open(__file__) as _:
        editor.text = _.read()
    editor.show()

    editor.detectSyntax(xmlFileName='python.xml')

    sys.exit(app.exec_())
