from typing import Callable

from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import RectAbs
from piafedit.model.geometry.size import SizeAbs


class RoiCommon:

    def __init__(self, manager: 'ImageManager', updater: Callable[[RectAbs], None]):
        self.zoom_speed: float = 1.1

        self.acceptDrops = True
        self.manager = manager
        self.updater = updater

        self.cursor_origin = None
        self.rect_origin: RectAbs = None

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

    def setup_action(self, pos: PointAbs):
        def action():
            rect = self.manager.rect
            rect.pos = pos
            self._update()

        return action

    def move_tile_action(self, dx: int, dy: int):
        def action():
            rect = self.manager.rect
            w = rect.size.width
            h = rect.size.height

            new_x = rect.pos.x + dx * w
            new_y = rect.pos.y + dy * h

            if -w < new_x <= self.manager.source.size().width:
                rect.pos.x += dx * w
            if -h < new_y <= self.manager.source.size().height:
                rect.pos.y += dy * h
            self._update()

        return action

    def _update(self):
        self.updater(self.manager.rect)