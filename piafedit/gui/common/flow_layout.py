import math
from typing import List

from PyQt5.QtWidgets import *


class FlowLayout(QWidget):
    def __init__(self, width: int = None, parent=None) -> None:
        super().__init__(parent)
        self.width = width
        self._widgets: List[QWidget] = []

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.scroll)
        self.setLayout(layout)
        self.update_layout()

    def register(self, widget: QWidget):
        self._widgets.append(widget)

    def update_layout(self, width: int = None):

        n = len(self._widgets)
        if n == 0:
            return

        if width is None:
            width = self.width or int(math.sqrt(n))

        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        for i in range(0, len(self._widgets), width):
            for j, widget in enumerate(self._widgets[i:i + width]):
                layout.addWidget(widget, i, j)

        widget = QWidget()
        widget.setLayout(layout)
        self.scroll.setWidget(widget)
