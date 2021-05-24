import logging

import pyqtgraph as pg
import rx
from PyQt5.QtGui import QCloseEvent
from rx import operators
from rx.subject import Subject

from piafedit.gui.image.source_view import SourceView
from piafedit.gui.image.view_manager import ViewManager
from piafedit.gui.utils import setup_roi
from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import Rect, RectAbs
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.libs.operator import Operator
from piafedit.model.source.data_source import DataSource

log = logging.getLogger(__name__)


class Overview(SourceView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui.histogram.hide()
        self.size = 256

        self.roi_subject = Subject()

        self.rect: RectAbs = None
        self.the_roi = pg.RectROI(PointAbs(0, 0).raw(), SizeAbs(0, 0).raw())
        self.the_roi.sigRegionChanged.connect(self.update_rect)
        self.addItem(self.the_roi)

        self.views = ViewManager()

    def subscribe(self):
        def mapper(x):
            return rx.from_([x, x * 2, x * 4])

        self.roi_subject.pipe(
            operators.flat_map_latest(mapper)
        ).subscribe(print)

    def set_source(self, source: DataSource):
        super().set_source(source)

        self.rect = Rect().abs(self.source.infos().size)
        buffer = self.source.overview(max_size=self.size)
        self.setImage(buffer)
        self.view.autoRange(padding=0.01)
        self.update_roi()

    def create_view(self, op: Operator = None):
        view = self.views.create_view(op)
        view.subscribe(self)
        return view

    def closeEvent(self, ev: QCloseEvent):
        self.views.clear()
        super().closeEvent(ev)

    def synchronize_rect(self):
        rx, ry = self.compute_roi_rect_ratio()
        rect = self.rect
        roi = self.the_roi
        rect.pos.x = round(roi.pos().x() * rx)
        rect.pos.y = round(roi.pos().y() * ry)
        rect.size.width = round(roi.size().x() * rx)
        rect.size.height = round(roi.size().y() * ry)

    def synchronize_roi(self):
        rx, ry = self.compute_roi_rect_ratio()
        rect = self.rect
        roi = self.the_roi
        rect2 = rect.scale(1 / rx, 1 / ry)
        setup_roi(roi, rect2)

    def compute_roi_rect_ratio(self):
        over = self.source.overview_size(self.size)
        full = self.source.infos().size
        rx = full.width / over.width
        ry = full.height / over.height
        return rx, ry

    def request_update(self):
        self.roi_subject.on_next(None)

    def setup_action(self, pos: PointAbs):
        overview = self

        def action():
            rect = overview.rect
            rect.pos = pos
            overview.update_roi()

        return action

    def update_rect(self):
        if self.source:
            self.synchronize_rect()
            self.request_update()

    def update_roi(self):
        self.synchronize_roi()
        self.request_update()
