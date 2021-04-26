import logging
from dataclasses import dataclass

import pyqtgraph as pg

from piafedit.gui.common.handler.drag_handler import Handler

log = logging.getLogger()


@dataclass
class MouseHandler:
    mousePressEvent: Handler = log.debug
    mouseReleaseEvent: Handler = log.debug
    mouseMoveEvent: Handler = log.debug
    wheelEvent: Handler = log.debug

    @staticmethod
    def backup(gv: pg.GraphicsView):
        if not hasattr(gv, '_mouse_backup'):
            gv._backup = MouseHandler(
                mousePressEvent=gv.mousePressEvent,
                mouseReleaseEvent=gv.mouseReleaseEvent,
                mouseMoveEvent=gv.mouseMoveEvent,
                wheelEvent=gv.wheelEvent,
            )

    @staticmethod
    def reset(gv: pg.GraphicsView):
        if hasattr(gv, '_mouse_backup'):
            gv._backup.patch(gv)
            del gv._backup

    def patch(self, gv: pg.GraphicsView):
        MouseHandler.backup(gv)
        gv.mousePressEvent = self.mousePressEvent
        gv.mouseReleaseEvent = self.mouseReleaseEvent
        gv.mouseMoveEvent = self.mouseMoveEvent
        gv.wheelEvent = self.wheelEvent
