from typing import Callable

from PyQt5.QtCore import Qt

from piafedit.geometry.point import PointAbs
from piafedit.geometry.rect import RectAbs
from piafedit.gui.event.event_handler import EventHandler


class RoiHandler(EventHandler):
    zoom_speed: int = 1.05

    def __init__(self, manager: 'ImageManager', updater: Callable[[RectAbs], None]):
        self.manager = manager
        self.updater = updater

        self.mouse_control = False
        self.last_mouse_pos = None

    def mousePressEvent(self, ev):
        self.mouse_control = True

    def mouseReleaseEvent(self, ev):
        self.mouse_control = False
        self.last_mouse_pos = None

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

    def wheelEvent(self, ev):
        rect = self.manager.rect
        delta = ev.angleDelta().y()
        speed = self.zoom_speed if delta > 0 else 1/self.zoom_speed
        rect.size.width = round(rect.size.width * speed)
        rect.size.height = round(rect.size.height * speed)
        self._update()

    def mouseMoveEvent(self, ev):
        rect = self.manager.rect
        last_pos = self.last_mouse_pos
        self.last_mouse_pos = ev.pos()
        if last_pos and self.mouse_control:
            dx = self.last_mouse_pos.x() - last_pos.x()
            dy = self.last_mouse_pos.y() - last_pos.y()
            rect.pos.x -= dx
            rect.pos.y -= dy
            self._update()

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
