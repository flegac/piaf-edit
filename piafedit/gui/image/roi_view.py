import logging
from typing import Optional

import rx.operators as ops
from PyQt5.QtGui import QCloseEvent

from piafedit.gui.image.overview import Overview
from piafedit.gui.image.roi_keyboard import RoiKeyboardHandler
from piafedit.gui.image.roi_mouse import RoiMouseHandler
from piafedit.gui.image.source_view import SourceView
from piafedit.model.geometry.size import SizeAbs

log = logging.getLogger(__name__)

MAX_REDRAW_PER_SEC = 24
SMALL_REDRAW_LATENCY = 1. / MAX_REDRAW_PER_SEC
MEDIUM_REDRAW_LATENCY = 2 * SMALL_REDRAW_LATENCY
FULL_REDRAW_LATENCY = .2 + 2 * MEDIUM_REDRAW_LATENCY


class RoiView(SourceView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.overview: Optional[Overview] = None
        self.last_update = 0

    def view_name(self):
        name = 'undefined'
        if self.source is not None:
            name = self.source.infos().name
        op_name = '' if self.op is None else self.op.__name__
        return f'{name} {op_name}'

    def closeEvent(self, ev: QCloseEvent):
        self.detach()
        super().closeEvent(ev)

    def detach(self):
        if self.overview:
            self.overview.views.detach(self)

    def subscribe(self, overview: Overview):
        self.detach()
        self.overview = overview
        self.source = overview.source
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

    def view_updater(self, size: SizeAbs = None):
        view = self

        def updater(ev):
            try:
                update_time = ev
                if update_time < view.last_update:
                    return
                view.last_update = update_time
                view.update_view(size)
            except Exception as e:
                log.warning(e)

        return updater
