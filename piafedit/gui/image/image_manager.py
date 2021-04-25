import pyqtgraph as pg

from piafedit.gui.image.roi_handler import RoiHandler
from piafedit.gui.utils import rect_to_roi, setup_roi
from piafedit.model.geometry.point import Point
from piafedit.model.geometry.rect import Rect, RectAbs
from piafedit.model.geometry.size import Size, SizeAbs
from piafedit.model.libs.filters import edge_detection, contrast_stretching, dilate, erode
from piafedit.model.source.data_source import DataSource


class ImageManager:
    ROI = Rect(Point(0.5, 0.5), Size(.2, .2))

    def __init__(self, source: DataSource):
        self.source = source
        self.rect = Rect().abs(self.source.size())
        self.overview_size = 96
        self.buffer_size = 256
        self.current_buffer_shape = None

        roi = rect_to_roi(self.rect)
        self.overview = self.create_overview(roi)
        self.view = self.create_view(roi)
        self.update_view()

    def update_status(self, cursor: RectAbs = None):
        from piafedit.editor_api import P
        cursor_infos = ''
        if cursor:
            x, y = cursor.pos.raw()
            dx, dy = cursor.size.raw()
            delta = f'[{dx},{dy}]' if dx != 0 or dy != 0 else ''
            cursor_infos = f'cursor: {x, y}{delta} '
        P.update_status(f'{cursor_infos}rect: {self.rect} buffer: {self.current_buffer_shape}')

    def update_view(self):
        window = self.rect.limit(self.source.size())

        abs_size = SizeAbs(self.buffer_size, self.buffer_size)
        size = Size.from_aspect(window.size.aspect_ratio).abs(abs_size)

        source = self.source
        # source = self.source.map(edge_detection)
        # source = self.source.map(contrast_stretching)
        # source = self.source.map(dilate)
        # source = self.source.map(erode)

        buffer = source.read(window, output_size=size)
        self.current_buffer_shape = buffer.shape
        self.view.setImage(buffer)
        self.update_status()
        self.view.view.autoRange(padding=0.0)
        self.overview.view.autoRange(padding=0.05)

    def update_rect(self, roi: pg.RectROI):
        over = self.source.overview_size(self.overview_size)
        full = self.source.size()
        rx = full.width / over.width
        ry = full.height / over.height

        self.rect.pos.x = round(roi.pos().x() * rx)
        self.rect.pos.y = round(roi.pos().y() * ry)
        self.rect.size.width = round(roi.size().x() * rx)
        self.rect.size.height = round(roi.size().y() * ry)
        self.update_view()

    def update_roi(self, roi: pg.RectROI, rect: RectAbs):
        over = self.source.overview_size(self.overview_size)
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
        buffer = self.source.overview(size=self.overview_size)

        view = pg.ImageView()
        view.setImage(buffer)
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
