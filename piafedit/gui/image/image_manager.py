import logging
import time

import rx.operators as ops
from rx.subject import Subject

from piafedit.gui.browser.image_drag_handler import ImageDragHandler
from piafedit.gui.image.overview import Overview
from piafedit.gui.image.roi.roi_keyboard import RoiKeyboardHandler
from piafedit.gui.image.roi.roi_mouse import RoiMouseHandler
from piafedit.gui.image.roi.roi_view import RoiView
from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import RectAbs
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.libs.operator import Operator
from piafedit.model.source.data_source import DataSource

log = logging.getLogger(__name__)


class ImageManager:
    MAX_REDRAW_PER_SEC = 24
    SMALL_REDRAW_LATENCY = 1. / MAX_REDRAW_PER_SEC
    MEDIUM_REDRAW_LATENCY = 2 * SMALL_REDRAW_LATENCY
    FULL_REDRAW_LATENCY = .2 + 2 * MEDIUM_REDRAW_LATENCY

    def __init__(self, source: DataSource):
        self.roi_update = Subject()
        self.last_update = 0

        self.roi_update.pipe(
            ops.throttle_first(1. / ImageManager.MAX_REDRAW_PER_SEC),
        ).subscribe(on_next=self.view_updater(SizeAbs(64, 64)))

        self.roi_update.pipe(
            ops.debounce(ImageManager.MEDIUM_REDRAW_LATENCY),
        ).subscribe(on_next=self.view_updater(SizeAbs(512, 512)))

        self.roi_update.pipe(
            ops.debounce(ImageManager.FULL_REDRAW_LATENCY),
        ).subscribe(on_next=self.view_updater())

        self.overview = Overview(source)
        self.overview.the_roi.sigRegionChanged.connect(self.update_rect)
        self.view = self.create_view()
        self.op: Operator = None
        self.update_roi()

    def request_update(self):
        self.roi_update.on_next(time.time())

    def create_view(self):
        view = RoiView()

        manager = self
        widget = view.ui.graphicsView

        RoiKeyboardHandler(self).patch(widget)
        RoiMouseHandler(self).patch(widget)
        ImageDragHandler().patch(widget)

        old_resizeEvent = widget.resizeEvent

        def resizeEvent(ev):
            old_resizeEvent(ev)
            manager.request_update()

        widget.resizeEvent = resizeEvent
        return view

    def set_operator(self, op: Operator):
        self.op = op
        self.request_update()

    def view_updater(self, size: SizeAbs = None):
        manager = self

        def updater(ev):
            try:
                if ev < manager.last_update:
                    return
                manager.last_update = ev

                view_size = size or manager.view.size()
                if manager.view.size().width < view_size.width:
                    view_size = manager.view.size()

                buffer = manager.overview.get_buffer(view_size)
                if manager.op:
                    buffer = manager.op(buffer)
                manager.view.set_buffer(buffer)
                manager.update_status()

            except Exception as e:
                log.warning(e)

        return updater

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
        self.request_update()

    def update_roi(self):
        self.overview.synchronize_roi()
        self.request_update()
