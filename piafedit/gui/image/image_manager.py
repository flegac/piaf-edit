import time

from piafedit.gui.browser.image_drag_handler import ImageDragHandler
from piafedit.gui.image.overview import Overview
from piafedit.gui.image.roi.roi_keyboard import RoiKeyboardHandler
from piafedit.gui.image.roi.roi_mouse import RoiMouseHandler
from piafedit.gui.image.roi.roi_view import RoiView
from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import RectAbs
from piafedit.model.geometry.size import Size, SizeAbs
from piafedit.model.libs.operator import Operator
from piafedit.model.source.data_source import DataSource


class ImageManager:
    def __init__(self, source: DataSource):
        self.last_update = 0

        self.overview = Overview(source)
        self.overview.the_roi.sigRegionChanged.connect(self.update_rect)
        self.view = self.create_view()
        self.op: Operator = None
        self.update_roi()

    def create_view(self):
        view = RoiView()

        manager = self
        widget = view.ui.graphicsView

        RoiKeyboardHandler(self).patch(widget)
        # Ui.actions.handler().patch(self.ui.graphicsView)
        RoiMouseHandler(self).patch(widget)
        ImageDragHandler().patch(widget)

        old_resizeEvent = widget.resizeEvent

        def resizeEvent(ev):
            old_resizeEvent(ev)
            manager.update_view()

        widget.resizeEvent = resizeEvent
        return view

    def set_operator(self, op: Operator):
        self.op = op
        self.update_view()

    def update_view(self):
        view_size = self.view.size()
        now = time.time()
        if now - self.last_update < 3:
            view_size = SizeAbs(64, 64)
        self.last_update = now

        buffer = self.overview.get_buffer(view_size)
        if self.op:
            buffer = self.op(buffer)
        self.view.set_buffer(buffer)
        self.update_status()

    def setup_action(self, pos: PointAbs):
        def action():
            rect = self.overview.rect
            rect.pos = pos
            self.update_roi()

        return action

    def update_status(self, cursor: RectAbs = None):
        from piafedit.editor_api import P
        cursor_infos = ''
        if cursor:
            x, y = cursor.pos.raw()
            dx, dy = cursor.size.raw()
            delta = f'[{dx},{dy}]' if dx != 0 or dy != 0 else ''
            cursor_infos = f'cursor: {x, y}{delta} '
        P.update_status(f'{cursor_infos}rect: {self.overview.rect} buffer: {self.view.current_buffer_shape}')

    def update_rect(self):
        self.overview.synchronize_rect()
        self.update_view()

    def update_roi(self):
        self.overview.synchronize_roi()
        self.update_view()
