import math
from typing import List

import numpy as np
from PyQt5.QtWidgets import *

from piafedit.gui.layouts.utils import image_button


class FlowLayout(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._widgets: List[QWidget] = []

        self.widget = QWidget()
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.scroll.setWidget(self.widget)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.scroll)
        self.setLayout(layout)

        self.update_layout()

    def register(self, widget: QWidget):
        self._widgets.append(widget)

    def update_layout(self):
        n = len(self._widgets)
        if n == 0:
            return

        width = int(math.sqrt(n))
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        for i in range(0, len(self._widgets), width):
            for j, widget in enumerate(self._widgets[i:i + width]):
                layout.addWidget(widget, i, j)
        self.widget.setLayout(layout)


if __name__ == '__main__':
    app = QApplication([])
    flow = FlowLayout()
    for _ in range(20):
        w, h = 128, 96
        shape = (h, w, 3)
        buffer = np.random.randint(0, 255, size=shape).astype('uint8')

        flow.register(image_button(buffer))
    flow.update_layout()
    flow.show()

    app.exec_()
