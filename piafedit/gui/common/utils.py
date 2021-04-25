from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtWidgets import QPushButton, QSizePolicy

from piafedit.model.libs.filters import normalize
from piafedit.model.libs.operator import Buffer
from piafedit.model.source.data_source import DataSource


def pixmap_from_numpy(buffer: Buffer) -> QPixmap:
    buffer = (normalize(buffer) * 255).astype('uint8')
    h, w = buffer.shape[:2]
    img = QImage(buffer.tobytes(), w, h, QImage.Format_RGB888)
    return QPixmap.fromImage(img)


def source_button(source: DataSource, size: int = 256):
    overview = source.overview(size=size)
    button = image_button(overview)

    def handler():
        from piafedit.editor_api import P

        P.show_source(source)

    button.clicked.connect(handler)
    width, height = source.size().raw()
    dtype = source.dtype()
    bands = source.bands()
    name = source.name
    button.setToolTip(f'{name} {width}x{height} {bands} {dtype}')

    return button


def image_button(buffer: Buffer):
    r, g, b = 0, 0, 0
    h, w = buffer.shape[:2]
    pixmap = pixmap_from_numpy(buffer)

    widget = QPushButton()
    # widget.clicked.connect(lambda: print('ok'))
    # widget.setText(text)
    widget.setStyleSheet(f'QPushButton {{ color: rgb{r, g, b}; margin: 0px }}')
    widget.setIcon(QIcon(pixmap))
    widget.setIconSize(QSize(w, h))
    widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    return widget
