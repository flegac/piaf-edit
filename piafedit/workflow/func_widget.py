import uuid

from PyQt5 import QtCore
from PyQt5.QtCore import QMimeData
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QPushButton


class FuncWidget(QPushButton):
    def __init__(self):
        super().__init__()
        self.setText(str(uuid.uuid4()))
        self.setAcceptDrops(True)

    def mousePressEvent(self, event):
        print(f'{event}: {event.pos()} : {self.geometry()} {self.geometry().contains(event.pos())}')
        if event.button() == QtCore.Qt.LeftButton and self.geometry().contains(event.pos()):
            print('drag')
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText('coucou')
            drag.setMimeData(mime_data)
            dropAction = drag.exec()

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.setText(e.mimeData().text())
