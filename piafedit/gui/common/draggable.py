from typing import Callable

from PyQt5.QtCore import QMimeData, Qt
from PyQt5.QtGui import QMouseEvent, QDrag
from PyQt5.QtWidgets import QWidget, QApplication


class Draggable:
    @staticmethod
    def patch(widget: QWidget, data_builder: Callable[[QWidget], QMimeData]):
        widget.drag_start_pos = None

        mouse_press_event = widget.mousePressEvent
        mouse_move_event = widget.mouseMoveEvent

        def mousePressEvent(ev: QMouseEvent):
            mouse_press_event(ev)
            if ev.button() == Qt.LeftButton:
                widget.drag_start_pos = ev.pos()

        def mouseMoveEvent(ev: QMouseEvent):
            mouse_move_event(ev)
            if widget.drag_start_pos is None:
                return
            d = (ev.pos() - widget.drag_start_pos).manhattanLength()
            if d < QApplication.startDragDistance():
                return
            drag = QDrag(widget)
            drag.setMimeData(data_builder(widget))
            drop_action = drag.exec(Qt.CopyAction | Qt.MoveAction)

        widget.mousePressEvent = mousePressEvent
        widget.mouseMoveEvent = mouseMoveEvent