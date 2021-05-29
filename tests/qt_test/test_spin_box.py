# importing libraries

from PyQt5.QtWidgets import *

from piafedit.ui_utils import gui_app


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("Python ")

        # setting geometry
        self.setGeometry(100, 100, 600, 400)

        # calling method
        self.UiComponents()

        # showing all the widgets
        self.show()

    # method for widgets
    def UiComponents(self):
        # creating spin box
        self.spin = QSpinBox(self)

        # setting geometry to spin box
        # self.spin.setGeometry(100, 100, 100, 40)

        # setting value to the spin box
        self.spin.setValue(33)


if __name__ == '__main__':
    with gui_app():
        window = Window()
        window.show()
