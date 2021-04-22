from pathlib import Path

import pyqtgraph as pg
from PyQt5.QtWidgets import *

from piafedit.config.config import WinConfig, Win
from piafedit.data_source.fast_data_source import FastDataSource
from piafedit.gui.image_manager import ImageManager
from piafedit.gui.main_window import MainWindow


def main():
    pg.setConfigOptions(imageAxisOrder='row-major')
    app = QApplication([])

    data = FastDataSource(Path('../resources/test.tif'))

    manager = ImageManager(data)

    win = MainWindow(WinConfig())
    win.set_content(win.widgets[Win.view], manager.view)
    win.set_content(win.widgets[Win.overview], manager.overview)
    win.set_content(win.widgets[Win.infos], manager.panel)

    win.show()
    app.exec_()


if __name__ == '__main__':
    main()
