import pyqtgraph as pg

from piafedit.geometry.point import PointAbs
from piafedit.geometry.rect import RectAbs
from piafedit.geometry.size import SizeAbs


def rect_to_roi(rect: RectAbs):
    return pg.RectROI(*rect.raw())


def roi_to_rect(roi: pg.RectROI):
    point = PointAbs(roi.pos().x(), roi.pos().y())
    size = SizeAbs(roi.size().x(), roi.size().y())
    return RectAbs(point, size)


def setup_roi(roi: pg.RectROI, rect: RectAbs):
    roi.setPos(*rect.pos.raw())
    roi.setSize(rect.size.raw())
