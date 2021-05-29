import uuid

from PyQt5.QtWidgets import QMainWindow, QPushButton

from piafedit.ui_utils import gui_app


class MainWindow(QMainWindow):
    singleton: 'MainWindow' = None

    def __init__(self):
        super().__init__()
        btn = QPushButton(f'RESTART\n{uuid.uuid4()}')
        btn.clicked.connect(MainWindow.restart)
        self.setCentralWidget(btn)
        self.show()

    @staticmethod
    def restart():
        MainWindow.singleton = MainWindow()


if __name__ == '__main__':
    with gui_app():
        MainWindow.restart()
