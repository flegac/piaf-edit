import logging
from pathlib import Path
from typing import List, Iterator

import pyqtgraph as pg
from PyQt5.QtWidgets import QFileDialog

from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import RectAbs
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.source.data_source import DataSource

log = logging.getLogger()


def rect_to_roi(rect: RectAbs):
    return pg.RectROI(*rect.raw())



def select_files() -> List[Path]:
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.ExistingFiles)
    dialog.setDirectory(str(Path('../gui').absolute()))
    # dialog.setFilter('Image files (*.jpg *.gif)')

    if dialog.exec():
        filenames = dialog.selectedFiles()
        log.debug(filenames)
        paths = [Path(file) for file in filenames]
        return paths


def open_sources(paths: Iterator[Path]) -> List[DataSource]:
    from piafedit.model.source.rio_data_source import RIODataSource
    sources = []
    for path in paths:
        if path.is_dir():
            sources.append(open_sources(list(path.iterdir())))
        else:
            try:
                source = RIODataSource(path)
                sources.append(source)
            except:
                log.warning(f'Could not open {path}')
    return sources
