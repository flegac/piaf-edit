from PyQt5.QtCore import QRect, QRectF
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene

from piafedit.ui_utils import load_ui
from piafedit.workflow.func_widget import FuncWidget


class GraphUi(QWidget):

    def __init__(self):
        super().__init__()
        load_ui('graph', self)
        self.show()

        scene = QGraphicsScene()
        scene.addRect(QRectF(10,10,25,25))

        view : QGraphicsView = self.view
        view.setScene(scene)


if __name__ == '__main__':
    app = QApplication([])
    win = GraphUi()
    app.exec_()
