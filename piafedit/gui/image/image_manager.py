from piafedit.gui.image.overview import Overview
from piafedit.gui.image.roi_view import RoiView
from piafedit.model.source.data_source import DataSource


class ImageManager:

    def __init__(self, source: DataSource):
        self.overview = Overview(source)
        self.view = RoiView(self.overview)
