import sys

from PyQt5.QtWidgets import QComboBox, QWidget, QFormLayout, QLabel, QLineEdit, QApplication


class combo(QComboBox):

    def __init__(self, title, parent):
        super(combo, self).__init__(parent)
        print(self.acceptDrops())
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):

        print({
            'text': e.mimeData().hasText(),
            'image': e.mimeData().hasImage(),
            'html': e.mimeData().hasHtml(),
            'urls': e.mimeData().hasUrls(),
            'color': e.mimeData().hasColor()
        })

        if e.mimeData().hasUrls():
            print('accept', e.mimeData().text())
            e.accept()
        else:
            print('ignore', e)
            e.ignore()

    def dropEvent(self, e):
        print('handle', e)

        print('urls', e.mimeData().urls())

        self.addItem(e.mimeData().text())


class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        lo = QFormLayout()
        lo.addRow(QLabel("Type some text in textbox and drag it into combo box"))

        edit = QLineEdit()
        edit.setDragEnabled(True)
        com = combo("Button", self)
        lo.addRow(edit, com)
        self.setLayout(lo)
        self.setWindowTitle('Simple drag & drop')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()


if __name__ == '__main__':
    main()
