from piafedit.gui.image.overview import Overview
from piafedit.gui.image.roi_view import RoiView
from piafedit.model.geometry.point import Point, PointAbs
from piafedit.model.geometry.rect import Rect, RectAbs
from piafedit.model.geometry.size import Size
from piafedit.model.source.data_source import DataSource


class ImageManager:
    ROI = Rect(Point(0.5, 0.5), Size(.2, .2))

    def __init__(self, source: DataSource):
        self.overview = Overview(source)
        self.view = RoiView(self)
        self.overview.the_roi.sigRegionChanged.connect(self.update_rect)
        self.update_roi()

    def update_view(self):
        view_size = self.view.size()
        buffer = self.overview.get_buffer(view_size)
        self.view.set_buffer(buffer)
        self.update_status()

    def setup_action(self, pos: PointAbs):
        def action():
            rect = self.overview.rect
            rect.pos = pos
            self.update_roi()

        return action

    def update_status(self, cursor: RectAbs = None):
        from piafedit.editor_api import P
        cursor_infos = ''
        if cursor:
            x, y = cursor.pos.raw()
            dx, dy = cursor.size.raw()
            delta = f'[{dx},{dy}]' if dx != 0 or dy != 0 else ''
            cursor_infos = f'cursor: {x, y}{delta} '
        P.update_status(f'{cursor_infos}rect: {self.overview.rect} buffer: {self.view.current_buffer_shape}')

    def update_rect(self):
        self.overview.synchronize_rect()
        self.update_view()

    def update_roi(self):
        self.overview.synchronize_roi()
        self.update_view()
