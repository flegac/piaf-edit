import logging

import pyqtgraph as pg
from PyQt5.QtGui import QCloseEvent
from rx.subject import Subject

from piafedit.gui.image.bases.source_view import SourceView
from piafedit.gui.image.view_manager import ViewManager
from piafedit.gui.utils import roi_to_rect
from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import Rect, RectAbs
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.libs.operator import Operator
from piafedit.model.source.data_source import DataSource

log = logging.getLogger(__name__)


class RoiController:
    def __init__(self):
        self.roi: RectAbs = None
        self.subject = Subject()

    def move(self, roi: RectAbs):
        self.roi = roi
        self.request_update()

    def request_update(self):
        self.subject.on_next(self.roi.copy())

    def pg_roi(self):
        roi = pg.RectROI(PointAbs(0, 0).raw(), SizeAbs(0, 0).raw())
        roi.sigRegionChanged.connect(self.update_rect)

    def update_rect(self):
        if self.source is None:
            return
        rx, ry = self.compute_roi_rect_ratio()
        rect = roi_to_rect(self.the_roi).scale(rx, ry)
        self.window.move(rect)

    def compute_roi_rect_ratio(self):
        over = self.source.overview_size(self.overview_size)
        full = self.source.infos().size
        rx = full.width / over.width
        ry = full.height / over.height
        return rx, ry

class Overview(SourceView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window = RoiController()
        self.overview_size = 256
        self.views = ViewManager()

        self.the_roi = pg.RectROI(PointAbs(0, 0).raw(), SizeAbs(0, 0).raw())
        self.the_roi.sigRegionChanged.connect(self.update_rect)
        self.addItem(self.the_roi)


    def set_source(self, source: DataSource):
        super().set_source(source)
        self.window.roi = Rect().abs(self.source.infos().size)
        buffer = source.overview(max_size=self.overview_size)
        self.set_buffer(buffer)
        self.update_roi()

    def create_view(self, op: Operator = None):
        view = self.views.create_view(op)
        view.subscribe(self)
        return view

    def closeEvent(self, ev: QCloseEvent):
        self.views.clear()
        super().closeEvent(ev)

    def setup_action(self, pos: PointAbs):
        overview = self

        def action():
            rect = overview.window.roi
            rect.pos = pos
            overview.update_roi()

        return action

    def compute_roi_rect_ratio(self):
        over = self.source.overview_size(self.overview_size)
        full = self.source.infos().size
        rx = full.width / over.width
        ry = full.height / over.height
        return rx, ry

    def update_rect(self):
        if self.source is None:
            return
        rx, ry = self.compute_roi_rect_ratio()
        rect = roi_to_rect(self.the_roi).scale(rx, ry)
        self.window.move(rect)

    def update_roi(self):
        rx, ry = self.compute_roi_rect_ratio()
        rect = self.window.roi
        roi = self.the_roi
        rect2 = rect.scale(1 / rx, 1 / ry)

        roi.setPos(*rect2.pos.raw())
        roi.setSize(rect2.size.raw())

        self.window.request_update()
