from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from piafedit.gui.common.handler.keyboard_handler import KeyboardHandler
from piafedit.model.geometry.point import PointAbs


class RoiKeyboardHandler(KeyboardHandler):

    def __init__(self, overview: 'Overview'):
        from piafedit.gui.image.overview import Overview
        self.overview: Overview = overview
        from piafedit.gui.image.roi_view import RoiView
        self.view: RoiView = None

    def patch(self, view: QWidget):
        super().patch(view.ui.graphicsView)
        self.view = view

    def keyPressEvent(self, ev):
        overview = self.overview
        rect = overview.rect
        size = overview.source.infos().size
        end = PointAbs(size.width - rect.size.width, size.height - rect.size.height)

        handlers = {
            Qt.Key_Left: self.move_tile_action(-1, 0),
            Qt.Key_Right: self.move_tile_action(1, 0),
            Qt.Key_Up: self.move_tile_action(0, -1),
            Qt.Key_Down: self.move_tile_action(0, 1),
            Qt.Key_Home: overview.setup_action(PointAbs(0, 0)),
            Qt.Key_End: overview.setup_action(end),
        }
        handlers.get(ev.key(), lambda: None)()
        self.update_status(ev)

    def move_tile_action(self, dx: int, dy: int):
        overview = self.overview

        def action():
            full_size = overview.source.infos().size
            rect = overview.rect

            w = rect.size.width
            h = rect.size.height
            new_x = rect.pos.x + dx * w
            new_y = rect.pos.y + dy * h
            if -w < new_x <= full_size.width:
                rect.pos.x += dx * w
            if -h < new_y <= full_size.height:
                rect.pos.y += dy * h
            overview.update_roi()

        return action

    def update_status(self, ev):
        self.overview.update_status(None)
