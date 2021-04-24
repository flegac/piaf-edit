from pathlib import Path
from typing import List

import pyqtgraph as pg
from PyQt5.QtWidgets import QFileDialog

from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import RectAbs
from piafedit.model.geometry.size import SizeAbs


def rect_to_roi(rect: RectAbs):
    return pg.RectROI(*rect.raw())


def roi_to_rect(roi: pg.RectROI):
    point = PointAbs(roi.pos().x(), roi.pos().y())
    size = SizeAbs(roi.size().x(), roi.size().y())
    return RectAbs(point, size)


def setup_roi(roi: pg.RectROI, rect: RectAbs):
    roi.setPos(*rect.pos.raw())
    roi.setSize(rect.size.raw())


def select_files() -> List[str]:
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.ExistingFiles)
    dialog.setDirectory(str(Path('.').absolute()))
    # dialog.setFilter('Image files (*.jpg *.gif)')

    if dialog.exec():
        filenames = dialog.selectedFiles()
        print(filenames)
        return filenames
