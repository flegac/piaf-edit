from pathlib import Path

import pyqtgraph as pg
from PyQt5.QtWidgets import *

from piafedit.config.config import WinConfig
from piafedit.editor_api import P
from piafedit.gui.editor_window import EditorWindow
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.source.rio_data_source import RIODataSource

IMAGE_SIZE = 10_000


def gen_big_image():
    source = RIODataSource(Path('../resources/kitten.jpg'))
    dest = RIODataSource(Path('../resources/fat.tif'))

    size = SizeAbs(IMAGE_SIZE, IMAGE_SIZE / source.size().aspect_ratio)
    print(f'resize from {source.size()} to {size}')
    if not dest.path.exists():
        buffer = source.read(output_size=size)
        dest.create(buffer)
    return dest


def main():
    pg.setConfigOptions(imageAxisOrder='row-major')
    app = QApplication([])

    P.main_window = EditorWindow(WinConfig())
    P.main_window.show()

    source = gen_big_image()
    P.show_source(source)

    # P.open_source(source)
    # P.open_source(source)
    # P.open_source(source)
    # P.open_source(source)

    app.exec_()


if __name__ == '__main__':
    main()
