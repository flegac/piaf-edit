import logging
from dataclasses import dataclass
from typing import Callable, Any

import pyqtgraph as pg

Handler = Callable[[Any], None]

log = logging.getLogger()

@dataclass
class EventHandler:
    mousePressEvent: Handler = log.debug
    mouseReleaseEvent: Handler = log.debug
    mouseMoveEvent: Handler = log.debug
    wheelEvent: Handler = log.debug
    keyPressEvent: Handler = log.debug

    @staticmethod
    def backup(gv: pg.GraphicsView):
        if not hasattr(gv, '_backup'):
            gv._backup = EventHandler(
                mousePressEvent=gv.mousePressEvent,
                mouseReleaseEvent=gv.mouseReleaseEvent,
                mouseMoveEvent=gv.mouseMoveEvent,
                wheelEvent=gv.wheelEvent,
                keyPressEvent=gv.keyPressEvent,
            )

    @staticmethod
    def reset(gv: pg.GraphicsView):
        if hasattr(gv, '_backup'):
            gv._backup.patch(gv)
            del gv._backup

    def patch(self, gv: pg.GraphicsView):
        EventHandler.backup(gv)
        gv.mousePressEvent = self.mousePressEvent
        gv.mouseReleaseEvent = self.mouseReleaseEvent
        gv.mouseMoveEvent = self.mouseMoveEvent
        gv.wheelEvent = self.wheelEvent
        gv.keyPressEvent = self.keyPressEvent
