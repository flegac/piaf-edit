from pathlib import Path

import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import *

from piafedit.config.config import WinConfig
from piafedit.model.source.fast_data_source import FastDataSource
from piafedit.editor_api import P
from piafedit.gui.editor_window import EditorWindow

IMAGE_SIZE = 4_000

def main():
    pg.setConfigOptions(imageAxisOrder='row-major')
    app = QApplication([])

    P.main_window = EditorWindow(WinConfig())
    P.main_window.show()

    source = FastDataSource(Path('../resources/test.tif'))
    if not source.path.exists():
        shape = (IMAGE_SIZE, IMAGE_SIZE, 3)
        buffer = np.random.random(shape)
        source.create(buffer)
    P.show_source(source)
    app.exec_()


if __name__ == '__main__':
    main()
