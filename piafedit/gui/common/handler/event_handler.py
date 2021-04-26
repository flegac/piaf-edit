import logging
from dataclasses import dataclass

import pyqtgraph as pg

from piafedit.gui.common.handler.drag_handler import Handler, DragHandler
from piafedit.gui.common.handler.mouse_handler import MouseHandler

log = logging.getLogger()


@dataclass
class EventHandler:
    keyPressEvent: Handler = log.debug
    mouse: MouseHandler = MouseHandler()
    drag: DragHandler = DragHandler()

    @staticmethod
    def backup(gv: pg.GraphicsView):
        if not hasattr(gv, '_keyboard_backup'):
            gv._backup = EventHandler(
                keyPressEvent=gv.keyPressEvent,
            )
        MouseHandler.backup(gv)
        DragHandler.backup(gv)

    @staticmethod
    def reset(gv: pg.GraphicsView):
        MouseHandler.reset(gv)
        DragHandler.reset(gv)
        if hasattr(gv, '_keyboard_backup'):
            gv._backup.patch(gv)
            del gv._backup

    def patch(self, gv: pg.GraphicsView):
        EventHandler.backup(gv)
        gv.keyPressEvent = self.keyPressEvent
        self.mouse.patch(gv)
        self.drag.patch(gv)
