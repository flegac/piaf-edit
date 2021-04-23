import numpy as np
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtWidgets import QPushButton, QSizePolicy


def pixmap_from_numpy(buffer: np.ndarray) -> QPixmap:
    buffer = (normalize(buffer) * 255).astype('uint8')
    h, w = buffer.shape[:2]
    img = QImage(buffer.tobytes(), w, h, QImage.Format_RGB888)
    return QPixmap.fromImage(img)


def normalize(buffer: np.ndarray):
    a, b = buffer.min(), buffer.max()
    if b - a != 0:
        buffer = (buffer - a) / (b - a)
    return buffer


def image_button(buffer: np.ndarray):
    r, g, b = 0, 0, 255
    h, w = buffer.shape[:2]
    pixmap = pixmap_from_numpy(buffer)

    widget = QPushButton()
    widget.clicked.connect(lambda: print('ok'))
    # widget.setText(text)
    # TODO: add informations
    widget.setToolTip('<image name> 1024x1024 rgb 8bit')
    widget.setStyleSheet(f'QPushButton {{ color: rgb{r, g, b}; margin: 0px }}')
    widget.setIcon(QIcon(pixmap))
    widget.setIconSize(QSize(w, h))
    # widget.setIconSize(QSize(64, 64))
    widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    return widget
