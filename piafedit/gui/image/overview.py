import time
from typing import List, Optional

import pyqtgraph as pg
from PyQt5.QtGui import QCloseEvent
from rx.subject import Subject

from piafedit.gui.utils import setup_roi
from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import Rect, RectAbs
from piafedit.model.geometry.size import SizeAbs, Size
from piafedit.model.libs.operator import Operator
from piafedit.model.source.data_source import DataSource
from qtwidgets.dock_widget import DockWidget


class Overview(pg.ImageView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.histogram_status = False
        self.roi_update = Subject()
        self.source: Optional[DataSource] = None
        self.rect: RectAbs = None

        self.views: List[DockWidget] = []
        self.the_roi = pg.RectROI(PointAbs(0, 0).raw(), SizeAbs(0, 0).raw())
        self.the_roi.sigRegionChanged.connect(self.update_rect)

        self.ui.histogram.hide()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
        self.addItem(self.the_roi)
        self.size = 256

    def set_source(self, source: DataSource):
        self.source = source
        self.rect = Rect().abs(self.source.infos().size)
        buffer = self.source.overview(size=self.size)
        self.setImage(buffer)
        self.view.autoRange(padding=0.01)
        self.update_roi()

    def closeEvent(self, ev: QCloseEvent):
        for view in self.views:
            view.close()
        super().closeEvent(ev)

    def get_view(self, op: Operator = None):
        from piafedit.gui.image.roi_view import RoiView
        name = 'undefined'
        if self.source:
            name = self.source.infos().name
        op_name = '' if op is None else op.__name__
        dock = DockWidget(f'{name} {op_name}')
        view = RoiView(self)
        view.set_histogram(self.histogram_status)
        view.set_operator(op)
        dock.setWidget(view)
        self.views.append(dock)
        return dock

    def set_histogram(self, status: bool):
        self.histogram_status = status
        for view in self.views:
            view.widget().set_histogram(status)

    def switch_histogram(self):
        self.histogram_status = not self.histogram_status
        self.set_histogram(self.histogram_status)

    def get_buffer(self, size: SizeAbs):
        source = self.source
        window = self.rect.limit(source.infos().size)
        aspect = window.size.aspect_ratio

        s = max(size.width, size.height)
        abs_size = SizeAbs(s, s)
        size = Size.from_aspect(aspect).abs(abs_size)

        buffer = source.read(window, output_size=size)
        return buffer

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
        event = time.time(), self
        self.roi_update.on_next(event)

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
