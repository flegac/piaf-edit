from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import QDir, QRectF
from PyQt5.QtWidgets import QWidget, QApplication, QFileSystemModel, QGraphicsScene


class TestUi(QWidget):
    def __init__(self):
        super(TestUi, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('../../resources/ui/test.ui', self)  # Load the .ui file

        model = QFileSystemModel()

        path = QDir.currentPath()
        print(path)

        path = Path('../gui').absolute().__str__()
        print(path)
        model.setRootPath(path)



        self.treeView.setModel(model)
        self.treeView.selectionModel().selectionChanged.connect(self.on_select)
        self.treeView.doubleClicked.connect(self.on_click)

        self.treeView.setRootIndex(model.index(path))

    def on_select(self, ev):
        print(f'selected: {ev}')

    def on_click(self, ev):
        print(f'clicked: {ev}')


if __name__ == '__main__':
    app = QApplication([])
    window = TestUi()
    window.show()
    app.exec_()
