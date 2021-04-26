from copy import deepcopy
from typing import Callable

from piafedit.gui.common.handler.mouse_handler import MouseHandler
from piafedit.gui.image.handler.roi_common import RoiCommon
from piafedit.model.geometry.rect import RectAbs


class RoiMouseHandler(RoiCommon, MouseHandler):
    def __init__(self, manager: 'ImageManager', updater: Callable[[RectAbs], None]):
        super().__init__(manager, updater)

    def mousePressEvent(self, ev):
        self.cursor_origin = ev.pos()
        self.rect_origin = deepcopy(self.manager.rect)

    def mouseReleaseEvent(self, ev):
        self.cursor_origin = None
        self.rect_origin = None

    def wheelEvent(self, ev):
        rect = self.manager.rect
        delta = ev.angleDelta().y()
        speed = self.zoom_speed if delta > 0 else 1 / self.zoom_speed
        rect.size.width = round(rect.size.width * speed)
        rect.size.height = round(rect.size.height * speed)
        self._update()
        self.update_status(ev)

    def mouseMoveEvent(self, ev):
        cursor = ev.pos()
        x, y = cursor.x(), cursor.y()
        rect: RectAbs = self.manager.rect

        dx, dy = (0, 0)
        if self.cursor_origin:
            ox, oy = self.cursor_origin.x(), self.cursor_origin.y()

            dx = self.cursor_origin.x() - cursor.x()
            dy = self.cursor_origin.y() - cursor.y()

            # dx = round(dx / rect.size.width)
            # dy = round(dy / rect.size.height)

            rect.pos.x = self.rect_origin.pos.x + dx
            rect.pos.y = self.rect_origin.pos.y + dy
            self._update()

        self.update_status(ev)
