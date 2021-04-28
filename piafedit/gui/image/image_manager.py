from piafedit.gui.image.overview import Overview
from piafedit.gui.image.roi_view import RoiView
from piafedit.gui.utils import setup_roi
from piafedit.model.geometry.point import Point
from piafedit.model.geometry.rect import Rect, RectAbs
from piafedit.model.geometry.size import Size, SizeAbs
from piafedit.model.source.data_source import DataSource


class ImageManager:
    ROI = Rect(Point(0.5, 0.5), Size(.2, .2))

    def __init__(self, source: DataSource):
        self.source = source
        self.current_buffer_shape = None
        self.overview = Overview(self)
        self.view = RoiView(self)
        self.update_roi()

    def update_status(self, cursor: RectAbs = None):
        from piafedit.editor_api import P
        cursor_infos = ''
        if cursor:
            x, y = cursor.pos.raw()
            dx, dy = cursor.size.raw()
            delta = f'[{dx},{dy}]' if dx != 0 or dy != 0 else ''
            cursor_infos = f'cursor: {x, y}{delta} '
        P.update_status(f'{cursor_infos}rect: {self.overview.rect} buffer: {self.current_buffer_shape}')

    def update_view(self):
        view = self.view
        overview = self.overview
        source = self.source

        window = self.overview.rect.limit(source.size())

        w = view.view.width()
        h = view.view.height()
        s = max(w, h)
        abs_size = SizeAbs(s, s)
        size = Size.from_aspect(window.size.aspect_ratio).abs(abs_size)

        buffer = source.read(window, output_size=size)
        view.setImage(buffer)
        view.view.autoRange(padding=0.0)
        overview.view.autoRange(padding=0.05)

        self.current_buffer_shape = buffer.shape
        self.update_status()

    def show_widgets(self, status: bool):
        if status:
            self.overview.ui.histogram.show()
            self.overview.ui.roiBtn.show()
            self.overview.ui.menuBtn.show()
        else:
            self.overview.ui.histogram.hide()
            self.overview.ui.roiBtn.hide()
            self.overview.ui.menuBtn.hide()

    def compute_roi_rect_ratio(self):

        over = self.source.overview_size(self.overview.size)
        full = self.source.size()
        rx = full.width / over.width
        ry = full.height / over.height
        return rx, ry

    def update_roi(self):
        rx, ry = self.compute_roi_rect_ratio()
        rect = self.overview.rect
        roi = self.overview.the_roi

        rect2 = rect.scale(1 / rx, 1 / ry)
        setup_roi(roi, rect2)
        self.update_view()
