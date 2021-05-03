from pathlib import Path

import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication

from piafedit.app_v1 import IMAGE_SIZE, log
from piafedit.editor_api import P
from piafedit.gui2.main_ui import Ui
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.source.rio_data_source import RIODataSource

ROOT_DIR = Path('../resources')


def gen_big_image():
    source = RIODataSource(ROOT_DIR / 'kitten.jpg')
    dest = RIODataSource(ROOT_DIR / 'fat.tif')

    size = SizeAbs(IMAGE_SIZE, IMAGE_SIZE / source.infos().aspect)
    log.debug(f'resize from {source.infos().size} to {size}')
    if not dest.path.exists():
        buffer = source.read(output_size=size)
        dest.create(buffer)
    return dest


if __name__ == '__main__':
    source = gen_big_image()

    pg.setConfigOptions(imageAxisOrder='row-major')
    app = QApplication([])
    P.main_window = Ui(ROOT_DIR)

    P.show_source(source)

    app.exec_()
