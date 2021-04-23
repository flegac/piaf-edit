import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from piafedit.data_source.data_source import DataSource
from piafedit.geometry.point import Point
from piafedit.geometry.rect import Rect, RectAbs
from piafedit.geometry.size import SizeAbs, Size
from piafedit.gui.image.roi_handler import RoiHandler
from piafedit.gui.utils import rect_to_roi, setup_roi

MAX_AREA_SIZE = SizeAbs(1024, 1024)


class ImageManager:
    ROI = Rect(Point(0.5, 0.5), Size(.2, .2))

    def __init__(self, source: DataSource):
        self.source = source
        self.rect = ImageManager.ROI.abs(self.source.size())
        self.rect.size.limit(MAX_AREA_SIZE)
        self.overview_size = SizeAbs(256, 256)

        roi = rect_to_roi(self.rect)
        self.overview = self.create_overview(roi)
        self.view = self.create_view(roi)
        self.panel = InfoPanel(self)
        self.update_view()

    def update_view(self):
        self.rect.size.limit(MAX_AREA_SIZE)
        buffer = self.source.read(self.rect)
        self.view.setImage(buffer)
        self.panel.update_manager()

    def update_rect(self, roi: pg.RectROI):
        over = self.overview_size
        full = self.source.size()
        rx = full.width / over.width
        ry = full.height / over.height

        self.rect.pos.x = round(roi.pos().x() * rx)
        self.rect.pos.y = round(roi.pos().y() * ry)
        self.rect.size.width = round(roi.size().x() * rx)
        self.rect.size.height = round(roi.size().y() * ry)
        self.rect.size.limit(MAX_AREA_SIZE)
        self.update_view()

    def update_roi(self, roi: pg.RectROI, rect: RectAbs):
        over = self.overview_size
        full = self.source.size()
        rx = full.width / over.width
        ry = full.height / over.height

        rect2 = rect.scale(1 / rx, 1 / ry)
        setup_roi(roi, rect2)

    def create_view(self, roi: pg.RectROI):
        view = pg.ImageView()
        view.ui.roiBtn.hide()
        view.ui.menuBtn.hide()
        manager = self

        def handle_rect_update(rect: RectAbs):
            manager.update_roi(roi, rect)
            manager.update_view()

        handler = RoiHandler(self, handle_rect_update)
        handler.patch(view.ui.graphicsView)

        roi.sigRegionChanged.connect(lambda: manager.update_rect(roi))
        return view

    def create_overview(self, roi: pg.RectROI):
        data = self.source.read(Rect(), self.overview_size)
        view = pg.ImageView()
        view.setImage(data)
        view.ui.histogram.hide()
        view.ui.roiBtn.hide()
        view.ui.menuBtn.hide()
        view.addItem(roi)
        self.update_roi(roi, self.rect)
        return view

    def show_widgets(self, status: bool):
        if status:
            self.overview.ui.histogram.show()
            self.overview.ui.roiBtn.show()
            self.overview.ui.menuBtn.show()
        else:
            self.overview.ui.histogram.hide()
            self.overview.ui.roiBtn.hide()
            self.overview.ui.menuBtn.hide()


class InfoPanel(QWidget):
    def __init__(self, manager: ImageManager):
        super().__init__()
        self.manager = manager

        self.view_infos = QLabel()
        self.overview_infos = QLabel()
        self.area_infos = QLabel()

        l = QVBoxLayout()
        l.addWidget(self.view_infos)
        l.addWidget(self.overview_infos)
        l.addWidget(self.area_infos)
        self.setLayout(l)

    def update_manager(self):
        manager = self.manager
        source = manager.source
        h, w, b = source.shape()
        dtype = source.dtype()
        self.view_infos.setText(f'view: {source.name} {w}x{h}:{b} {dtype}')

        buffer = manager.overview.image
        h, w, b = buffer.shape
        dtype = buffer.dtype
        self.overview_infos.setText(f'overview: {w}x{h}:{b} {dtype}')

        area = manager.rect
        x, y = area.pos.raw()
        w, h = area.size.raw()

        self.area_infos.setText(f'area: {x},{y} {w}x{h}')
