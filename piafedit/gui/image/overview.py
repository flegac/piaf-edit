import pyqtgraph as pg

from piafedit.gui.utils import setup_roi
from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import Rect
from piafedit.model.geometry.size import SizeAbs, Size
from piafedit.model.source.data_source import DataSource
from piafedit.model.source.roi_data_source import RoiDataSource


class Overview(pg.ImageView):
    def __init__(self, source: DataSource):
        super().__init__()
        # TODO: use RoiDataSource!
        # self.source = RoiDataSource(source)

        self.source = source
        self.the_roi = pg.RectROI(PointAbs(0, 0).raw(), SizeAbs(0, 0).raw())
        self.rect = Rect().abs(self.source.size())

        self.ui.histogram.hide()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
        self.addItem(self.the_roi)
        self.size = 256

        buffer = self.source.overview(size=self.size)
        self.setImage(buffer)
        self.view.autoRange(padding=0.01)

    def get_buffer(self, size: SizeAbs):
        source = self.source
        window = self.rect.limit(source.size())
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
        full = self.source.size()
        rx = full.width / over.width
        ry = full.height / over.height
        return rx, ry