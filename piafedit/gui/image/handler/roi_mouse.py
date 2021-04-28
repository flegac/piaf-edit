from copy import deepcopy
from math import floor

from piafedit.gui.common.handler.mouse_handler import MouseHandler
from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import RectAbs
from piafedit.model.geometry.size import SizeAbs


class RoiMouseHandler(MouseHandler):
    def __init__(self, manager: 'ImageManager'):
        from piafedit.gui.image.image_manager import ImageManager
        self.manager: ImageManager = manager
        self.zoom_speed: float = 1.1

        self.cursor_origin = None
        self.rect_origin: RectAbs = None

    def mousePressEvent(self, ev):
        self.cursor_origin = ev.pos()
        self.rect_origin = deepcopy(self.manager.overview.rect)

    def mouseReleaseEvent(self, ev):
        self.cursor_origin = None
        self.rect_origin = None

    def wheelEvent(self, ev):
        rect: RectAbs = self.manager.overview.rect

        old_size = deepcopy(rect.size)

        delta = ev.angleDelta().y()
        speed = self.zoom_speed if delta < 0 else 1 / self.zoom_speed
        rect.size.width = round(rect.size.width * speed)
        rect.size.height = round(rect.size.height * speed)

        dx = old_size.width - rect.size.width
        dy = old_size.height - rect.size.height

        rect.pos.x += floor(dx / 2)
        rect.pos.y += floor(dy / 2)

        self.manager.update_roi()
        self.update_status(ev)

    def mouseMoveEvent(self, ev):
        cursor = ev.pos()
        x, y = cursor.x(), cursor.y()
        rect: RectAbs = self.manager.overview.rect

        dx, dy = (0, 0)
        if self.cursor_origin:
            ox, oy = self.cursor_origin.x(), self.cursor_origin.y()

            dx = self.cursor_origin.x() - cursor.x()
            dy = self.cursor_origin.y() - cursor.y()

            w = self.manager.view.view.width()
            h = self.manager.view.view.height()

            dx = (dx * rect.size.width / w)
            dy = (dy * rect.size.height / h)

            rect.pos.x = self.rect_origin.pos.x + dx
            rect.pos.y = self.rect_origin.pos.y + dy
            self.manager.update_roi()

        self.update_status(ev)

    def update_status(self, ev):
        cursor = ev.pos()
        x, y = cursor.x(), cursor.y()
        dx, dy = (0, 0)
        if self.cursor_origin:
            dx = self.cursor_origin.x() - cursor.x()
            dy = self.cursor_origin.y() - cursor.y()
        cursor_rect = RectAbs(PointAbs(x, y), SizeAbs(dx, dy))
        self.manager.update_status(cursor_rect)
