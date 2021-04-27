import math
from typing import List, Callable, TypeVar, Generic, Any

from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import *

T = TypeVar('T')
WidgetBuilder = Callable[[Any], QWidget]


class FlowWidget(QWidget, Generic[T]):
    def __init__(self, builder: WidgetBuilder, widget_width: int, parent=None) -> None:
        super().__init__(parent)
        self.widget_width = widget_width
        self.builder = builder
        self._widgets: List[QWidget] = []

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.scroll)
        self.setLayout(layout)

    def is_empty(self):
        return len(self._widgets) == 0

    def register(self, data: T):
        widget = self.builder(data)
        self._widgets.append(widget)
        self.update_layout()

    def resizeEvent(self, event: QResizeEvent):
        self.update_layout()

    def update_layout(self):
        n = len(self._widgets)
        if n == 0:
            return

        w = 30 + max(1, self.widget_width)
        width = max(1, math.floor(self.width() / w))

        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        for i in range(0, len(self._widgets), width):
            for j, widget in enumerate(self._widgets[i:i + width]):
                layout.addWidget(widget, i, j)

        widget = QWidget()
        widget.setLayout(layout)
        self.scroll.setWidget(widget)
