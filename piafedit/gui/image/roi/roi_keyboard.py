from PyQt5.QtCore import Qt

from piafedit.gui.common.handler.keyboard_handler import KeyboardHandler
from piafedit.model.geometry.point import PointAbs


class RoiKeyboardHandler(KeyboardHandler):

    def __init__(self, manager: 'ImageManager'):
        from piafedit.gui.image.image_manager import ImageManager
        self.manager: ImageManager = manager

    def keyPressEvent(self, ev):
        manager = self.manager
        rect = manager.overview.rect
        size = manager.overview.source.infos().size
        end = PointAbs(size.width - rect.size.width, size.height - rect.size.height)

        handlers = {
            Qt.Key_Left: self.move_tile_action(-1, 0),
            Qt.Key_Right: self.move_tile_action(1, 0),
            Qt.Key_Up: self.move_tile_action(0, -1),
            Qt.Key_Down: self.move_tile_action(0, 1),
            Qt.Key_Home: manager.setup_action(PointAbs(0, 0)),
            Qt.Key_End: manager.setup_action(end),
        }
        handlers.get(ev.key(), lambda: None)()
        self.update_status(ev)

    def move_tile_action(self, dx: int, dy: int):
        manager = self.manager

        def action():
            full_size = manager.overview.source.infos().size
            rect = manager.overview.rect

            w = rect.size.width
            h = rect.size.height
            new_x = rect.pos.x + dx * w
            new_y = rect.pos.y + dy * h
            if -w < new_x <= full_size.width:
                rect.pos.x += dx * w
            if -h < new_y <= full_size.height:
                rect.pos.y += dy * h
            manager.update_roi()

        return action

    def update_status(self, ev):
        self.manager.update_status(None)
