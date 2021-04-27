import logging
from dataclasses import dataclass

from PyQt5.QtWidgets import QWidget

from piafedit.gui.common.handler.drag_handler import Handler

log = logging.getLogger()


@dataclass
class MouseHandler:
    mousePressEvent: Handler = log.debug
    mouseReleaseEvent: Handler = log.debug
    mouseMoveEvent: Handler = log.debug
    wheelEvent: Handler = log.debug

    @staticmethod
    def backup(w: QWidget):
        if not hasattr(w, '_mouse_backup'):
            w._backup = MouseHandler(
                mousePressEvent=w.mousePressEvent,
                mouseReleaseEvent=w.mouseReleaseEvent,
                mouseMoveEvent=w.mouseMoveEvent,
                wheelEvent=w.wheelEvent,
            )

    @staticmethod
    def reset(w: QWidget):
        if hasattr(w, '_mouse_backup'):
            w._backup.patch(w)
            del w._backup

    def patch(self, w: QWidget):
        MouseHandler.backup(w)
        w.mousePressEvent = self.mousePressEvent
        w.mouseReleaseEvent = self.mouseReleaseEvent
        w.mouseMoveEvent = self.mouseMoveEvent
        w.wheelEvent = self.wheelEvent
