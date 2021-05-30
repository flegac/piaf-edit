from PyQt5.QtCore import Qt, QSize, QMimeData, QUrl
from PyQt5.QtGui import QIcon, QResizeEvent, QPixmap
from PyQt5.QtWidgets import QToolButton
from qimage2ndarray import array2qimage

from piafedit.gui.common.draggable import Draggable
from piafedit.model.source.rio_data_source import RIODataSource


class SourceButton(QToolButton):
    def __init__(self, source: RIODataSource):
        super().__init__()
        from piafedit.editor_api import P

        self.source = source

        # self.setAutoFillBackground(True)
        self.setStyleSheet(f'QToolButton {{ margin: 0px; }}')
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setText(source.infos().name)

        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        buffer = source.overview(256)
        h, w = buffer.shape[:2]
        self.aspect = w / h
        self.pixmap = QPixmap.fromImage(array2qimage(buffer))
        self.resize_pixmap(h)

        self.clicked.connect(lambda: P.show_source(source))

        Draggable.patch(self, SourceButton.build_data)

    def build_data(self):
        data = QMimeData()
        path = str(self.source.path.absolute())
        data.setUrls([
            QUrl(path)
        ])
        return data

    def resize_pixmap(self, w: int):
        h = int(w / self.aspect)
        icon = QIcon(self.pixmap.scaled(w, h, Qt.KeepAspectRatio))
        self.setIcon(icon)
        size = QSize(w, h)
        self.setIconSize(size)

    def resizeEvent(self, ev: QResizeEvent) -> None:
        super().resizeEvent(ev)
        self.resize_pixmap(self.width() - 7)
