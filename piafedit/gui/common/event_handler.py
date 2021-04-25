from dataclasses import dataclass
from typing import Callable, Any

import pyqtgraph as pg

Handler = Callable[[Any], None]


@dataclass
class EventHandler:
    mousePressEvent: Handler = print
    mouseReleaseEvent: Handler = print
    mouseMoveEvent: Handler = print
    wheelEvent: Handler = print
    keyPressEvent: Handler = print

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
