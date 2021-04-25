from copy import deepcopy
from typing import Callable

from PyQt5.QtCore import Qt

from piafedit.gui.common.event_handler import EventHandler
from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import RectAbs
from piafedit.model.geometry.size import SizeAbs


class RoiHandler(EventHandler):
    zoom_speed: int = 1.1

    def __init__(self, manager: 'ImageManager', updater: Callable[[RectAbs], None]):
        self.manager = manager
        self.updater = updater

        self.cursor_origin = None
        self.rect_origin: RectAbs = None

    def mousePressEvent(self, ev):
        self.cursor_origin = ev.pos()
        self.rect_origin = deepcopy(self.manager.rect)

    def mouseReleaseEvent(self, ev):
        self.cursor_origin = None
        self.rect_origin = None

    def keyPressEvent(self, ev):
        rect = self.manager.rect
        size = self.manager.source.size()

        start = PointAbs(0, 0)
        end = PointAbs(size.width - rect.size.width, size.height - rect.size.height)

        handlers = {
            Qt.Key_Left: self.move_action(-1, 0),
            Qt.Key_Right: self.move_action(1, 0),
            Qt.Key_Up: self.move_action(0, -1),
            Qt.Key_Down: self.move_action(0, 1),
            Qt.Key_Home: self.setup_action(start),
            Qt.Key_End: self.setup_action(end),
        }
        handlers.get(ev.key(), lambda: None)()
        self.update_status(ev)

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

    def update_status(self, ev):
        cursor = None
        try:
            cursor = ev.pos()
        except:
            pass
        cursor_rect = None
        if cursor:
            x, y = cursor.x(), cursor.y()
            dx, dy = (0, 0)
            if self.cursor_origin:
                dx = self.cursor_origin.x() - cursor.x()
                dy = self.cursor_origin.y() - cursor.y()
            cursor_rect = RectAbs(PointAbs(x, y), SizeAbs(dx, dy))
        self.manager.update_status(cursor_rect)

    def switch_mouse_control_action(self, status: bool):
        def action():
            self.mouse_control = status

        return action

    def setup_action(self, pos: PointAbs):
        def action():
            rect = self.manager.rect
            rect.pos = pos
            self._update()

        return action

    def move_action(self, dx: int, dy: int):
        def action():
            rect = self.manager.rect
            w = rect.size.width
            h = rect.size.height
            rect.pos.x += dx * w
            rect.pos.y += dy * h
            self._update()

        return action

    def _update(self):
        self.updater(self.manager.rect)
