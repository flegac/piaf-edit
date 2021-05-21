import logging
from typing import Optional

import numpy as np
import pyqtgraph as pg
import rx.operators as ops
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QSizePolicy

from piafedit.gui.browser.image_drag_handler import ImageDragHandler
from piafedit.gui.image.overview import Overview
from piafedit.gui.image.roi_keyboard import RoiKeyboardHandler
from piafedit.gui.image.roi_mouse import RoiMouseHandler
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.libs.operator import Operator

log = logging.getLogger(__name__)

MAX_REDRAW_PER_SEC = 24
SMALL_REDRAW_LATENCY = 1. / MAX_REDRAW_PER_SEC
MEDIUM_REDRAW_LATENCY = 2 * SMALL_REDRAW_LATENCY
FULL_REDRAW_LATENCY = .2 + 2 * MEDIUM_REDRAW_LATENCY


class RoiView(pg.ImageView):
    def __init__(self, overview: Overview):
        super().__init__()
        self.overview = overview
        self.last_update = 0
        self.subscribe(overview)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
        self.ui.graphicsView.setBackground(None)

        self.op: Optional[Operator] = None
        ImageDragHandler().patch(self)

    def view_name(self):
        name = 'undefined'
        if self.overview.source is not None:
            name = self.overview.source.infos().name
        op_name = '' if self.op is None else self.op.__name__
        return f'{name} {op_name}'

    def set_histogram(self, status: bool):
        if status:
            self.ui.histogram.show()
        else:
            self.ui.histogram.hide()

    def switch_histogram(self):
        self.set_histogram(self.ui.histogram.isHidden())

    def closeEvent(self, ev: QCloseEvent):
        self.overview.views.remove(self)
        super().closeEvent(ev)

    def subscribe(self, overview: Overview):
        self.overview = overview
        overview.roi_update.pipe(
            ops.throttle_first(1. / MAX_REDRAW_PER_SEC),
        ).subscribe(on_next=self.view_updater(SizeAbs(64, 64)))

        overview.roi_update.pipe(
            ops.debounce(MEDIUM_REDRAW_LATENCY),
        ).subscribe(on_next=self.view_updater(SizeAbs(512, 512)))

        overview.roi_update.pipe(
            ops.debounce(FULL_REDRAW_LATENCY),
        ).subscribe(on_next=self.view_updater(None))

        RoiKeyboardHandler(overview).patch(self)
        RoiMouseHandler(overview).patch(self)

    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        self.overview.request_update()

    def size(self):
        view = self.view
        w = view.width()
        h = view.height()
        return SizeAbs(w, h)

    def set_buffer(self, buffer: np.ndarray):
        if self.op:
            buffer = self.op(buffer)
        self.setImage(buffer)
        self.view.autoRange(padding=0.0)

    def set_operator(self, op: Operator):
        self.op = op

    def view_updater(self, size: SizeAbs = None):
        view = self

        def updater(ev):
            update_time, overview = ev
            try:
                if update_time < view.last_update:
                    return
                view.last_update = update_time

                view_size = size or view.size()
                if view.size().width < view_size.width:
                    view_size = view.size()
                buffer = overview.get_buffer(view_size)
                view.set_buffer(buffer)

            except Exception as e:
                log.warning(e)

        return updater
