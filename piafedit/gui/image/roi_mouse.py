from copy import deepcopy
from math import floor

from PyQt5.QtWidgets import QWidget

from piafedit.gui.common.handler.mouse_handler import MouseHandler
from piafedit.model.geometry.rect import RectAbs


class RoiMouseHandler(MouseHandler):
    def __init__(self, overview: 'Overview'):
        from piafedit.gui.image.overview import Overview
        from piafedit.gui.image.roi_view import RoiView
        self.overview: Overview = overview
        self.zoom_speed: float = 1.1

        self.cursor_origin = None
        self.rect_origin: RectAbs = None

        self.view: RoiView = None

    def patch(self, view: QWidget):
        super().patch(view.ui.graphicsView)
        self.view = view

    def mousePressEvent(self, ev):
        self.cursor_origin = ev.pos()
        self.rect_origin = deepcopy(self.overview.rect)

    def mouseReleaseEvent(self, ev):
        self.cursor_origin = None
        self.rect_origin = None

    def wheelEvent(self, ev):
        rect: RectAbs = self.overview.rect

        old_size = deepcopy(rect.size)

        delta = ev.angleDelta().y()
        speed = self.zoom_speed if delta < 0 else 1 / self.zoom_speed
        rect.size.width = round(rect.size.width * speed)
        rect.size.height = round(rect.size.height * speed)

        dx = old_size.width - rect.size.width
        dy = old_size.height - rect.size.height

        rect.pos.x += floor(dx / 2)
        rect.pos.y += floor(dy / 2)

        self.overview.update_roi()

    def mouseMoveEvent(self, ev):
        cursor = ev.pos()
        x, y = cursor.x(), cursor.y()
        rect: RectAbs = self.overview.rect

        dx, dy = (0, 0)
        if self.cursor_origin:
            ox, oy = self.cursor_origin.x(), self.cursor_origin.y()

            dx = self.cursor_origin.x() - cursor.x()
            dy = self.cursor_origin.y() - cursor.y()

            w = self.view.view.width()
            h = self.view.view.height()

            dx = (dx * rect.size.width / w)
            dy = (dy * rect.size.height / h)

            rect.pos.x = self.rect_origin.pos.x + dx
            rect.pos.y = self.rect_origin.pos.y + dy
            self.overview.update_roi()
