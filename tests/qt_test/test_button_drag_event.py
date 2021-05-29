import uuid

from PyQt5.QtCore import QMimeData, QUrl
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout

from piafedit.gui.common.draggable import Draggable
from piafedit.gui.common.drop import Drop
from piafedit.ui_utils import gui_app


class DragButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setText(str(uuid.uuid4()))
        self.clicked.connect(lambda: print('clicked!'))

        def accept(mime_data: QMimeData):
            return mime_data.hasUrls()

        def handle(widget: QWidget, mime_data: QMimeData):
            for url in mime_data.urls():
                path = url.path()
                widget.setText(path)

        Drop.patch(self, accept, handle)

        def data_builder(widget: QWidget):
            mime_data = QMimeData()
            mime_data.setUrls([
                QUrl(widget.text())
            ])
            return mime_data

        Draggable.patch(self, data_builder)


if __name__ == "__main__":
    with gui_app():
        w = QWidget()
        layout = QVBoxLayout()
        w.setLayout(layout)
        w.resize(800, 600)
        w.show()

        layout.addWidget(DragButton())
        layout.addWidget(DragButton())
        layout.addWidget(DragButton())
