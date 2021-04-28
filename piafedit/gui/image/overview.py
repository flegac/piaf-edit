import pyqtgraph as pg

# from piafedit.gui.image.image_manager import ImageManager
from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import Rect
from piafedit.model.geometry.size import SizeAbs


class Overview(pg.ImageView):
    def __init__(self, manager: 'ImageManager'):
        super().__init__()
        self.the_roi = pg.RectROI(PointAbs(0, 0).raw(), SizeAbs(0, 0).raw())
        self.rect = Rect().abs(manager.source.size())

        self.ui.histogram.hide()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
        self.addItem(self.the_roi)
        self.size = 256

        buffer = manager.source.overview(size=self.size)
        self.setImage(buffer)
