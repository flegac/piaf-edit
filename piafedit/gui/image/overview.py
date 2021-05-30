import logging

import pyqtgraph as pg
from rx.subject import Subject

from piafedit.gui.common.utils import roi_to_rect
from piafedit.gui.image.views.source_view import SourceView
from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import Rect, RectAbs
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.source.data_source import DataSource

log = logging.getLogger(__name__)


class RoiController:
    def __init__(self):
        self.roi: RectAbs = None
        self.on_change = Subject()

    def move(self, roi: RectAbs):
        self.roi = roi
        self.request_update()

    def set_aspect(self, aspect: float):
        if self.roi is None:
            return
        old = self.roi.center
        if aspect < self.roi.aspect_ratio:
            self.roi.size.height = self.roi.size.width / aspect
        else:
            self.roi.size.width = self.roi.size.height * aspect
        dx = self.roi.center.x - old.x
        dy = self.roi.center.y - old.y

        self.roi.move(-dx, -dy)

    def request_update(self):
        self.on_change.on_next(self.roi.copy())


class Overview(SourceView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window = RoiController()
        self.overview_size = 256

        self.the_roi = pg.RectROI(PointAbs(0, 0).raw(), SizeAbs(0, 0).raw())
        self.the_roi.sigRegionChanged.connect(self.update_rect)
        self.addItem(self.the_roi)

    def optimize_aspect(self, table_aspect: float = 1.0):
        from piafedit.editor_api import P
        win = P.main_window.main_view
        a1 = win.width() / win.height()
        aspect = a1 / table_aspect
        self.window.set_aspect(aspect)
        self.update_roi()

    def set_source(self, source: DataSource):
        super().set_source(source)
        self.window.roi = Rect().abs(self.source.infos().size)
        buffer = source.overview(max_size=self.overview_size)
        self.set_buffer(buffer)
        self.update_roi()

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
        if self.window.roi is None:
            return

        rx, ry = self.compute_roi_rect_ratio()
        rect = self.window.roi
        rect2 = rect.scale(1 / rx, 1 / ry)

        roi = self.the_roi
        roi.setPos(*rect2.pos.raw())
        roi.setSize(rect2.size.raw())

        self.window.request_update()
