from typing import Callable

from PyQt5.QtCore import Qt

from piafedit.gui.common.handler.event_handler import EventHandler
from piafedit.gui.image.handler.roi_common import RoiCommon
from piafedit.gui.image.handler.roi_drag import RoiDragHandler
from piafedit.gui.image.handler.roi_mouse import RoiMouseHandler
from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import RectAbs


class RoiHandler(RoiCommon, EventHandler):

    def __init__(self, manager: 'ImageManager', updater: Callable[[RectAbs], None]):
        super().__init__(manager, updater)
        self.drag = RoiDragHandler()
        self.mouse = RoiMouseHandler(manager, updater)
        self.manager = manager
        self.updater = updater

        self.cursor_origin = None
        self.rect_origin: RectAbs = None

    def keyPressEvent(self, ev):
        rect = self.manager.rect
        size = self.manager.source.size()

        start = PointAbs(0, 0)
        end = PointAbs(size.width - rect.size.width, size.height - rect.size.height)

        handlers = {
            Qt.Key_Left: self.move_tile_action(-1, 0),
            Qt.Key_Right: self.move_tile_action(1, 0),
            Qt.Key_Up: self.move_tile_action(0, -1),
            Qt.Key_Down: self.move_tile_action(0, 1),
            Qt.Key_Home: self.setup_action(start),
            Qt.Key_End: self.setup_action(end),
        }
        handlers.get(ev.key(), lambda: None)()
        self.update_status(ev)
