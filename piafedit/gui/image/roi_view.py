import logging
import time
from typing import Optional

import rx.operators as ops
from PyQt5.QtGui import QCloseEvent
from rx.subject import Subject

from piafedit.gui.image.overview import Overview
from piafedit.gui.image.roi_keyboard_handler import RoiKeyboardHandler
from piafedit.gui.image.roi_mouse_handler import RoiMouseHandler
from piafedit.gui.image.views.source_view import SourceView
from piafedit.model.geometry.size import SizeAbs

log = logging.getLogger(__name__)

MAX_FPS = 24
SMALL_LATENCY = 1. / MAX_FPS
NORMAL_LATENCY = 2 * SMALL_LATENCY
FULL_LATENCY = 2 * NORMAL_LATENCY

SmallSize = SizeAbs(64, 64)
NormalSize = SizeAbs(256, 256)
FullSize = None


class RoiView(SourceView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.overview: Optional[Overview] = None

        self.update_subject = Subject()
        self.last_update = 0

        def size_mapper(target_size):
            def action(x):
                return x, target_size

            return action

        for target_size, pipe in [
            (SmallSize, ops.throttle_first(1. / MAX_FPS)),
            (NormalSize, ops.debounce(NORMAL_LATENCY)),
            (FullSize, ops.debounce(FULL_LATENCY)),
        ]:
            self.update_subject.pipe(
                pipe,
                ops.map(size_mapper(target_size))
            ).subscribe(on_next=self.view_updater)

    def view_name(self):
        name = 'undefined'
        if self.source is not None:
            name = self.source.infos().name
        return f'{name}'

    def subscribe(self, overview: Overview):
        self.detach()
        self.overview = overview
        if self.source is None:
            self.set_source(overview.source)

        RoiKeyboardHandler(overview).patch(self)
        RoiMouseHandler(overview).patch(self)
        overview.window.on_change.subscribe(self.request_update)
        self.request_update()

    def request_update(self, ev=None):
        # FIXME: this slow down a lot
        # super().request_update()
        event = time.time()
        self.update_subject.on_next(event)

    def detach(self):
        if self.overview:
            self.overview.views.detach(self)
            self.overview.roi_subject.observers.remove(self.request_update)

    def view_updater(self, ev):
        try:
            update_time, target_size = ev
            if update_time < self.last_update:
                return
            self.last_update = update_time
            self.update_view(target_size)
        except Exception as e:
            log.warning(e)

    # ---- QT Events ---------------------------------------------
    def closeEvent(self, ev: QCloseEvent):
        self.detach()
        super().closeEvent(ev)

    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        self.request_update()
