import logging
from pathlib import Path
from typing import Iterator

import numpy as np
from PyQt5.QtWidgets import QMainWindow

from piafedit.gui.utils import select_files
from piafedit.model.source.data_source import DataSource
from piafedit.model.source.raw_data_source import RawDataSource
from piafedit.model.source.rio_data_source import RIODataSource
from piafedit.model.work_model import WorkModel


class P:
    log = logging.getLogger()
    main_window: QMainWindow = None

    @staticmethod
    def model() -> WorkModel:
        return P.main_window.model

    @staticmethod
    def restart():
        from piafedit.gui.main_ui import MainUi
        model = P.model()
        P.main_window.close()
        P.main_window = MainUi(model)

    @staticmethod
    def resources():
        return Path('../resources')

    @staticmethod
    def open_files():
        paths = select_files()
        sources = map(RIODataSource, paths)
        P.open_sources(sources)

    @staticmethod
    def new_source():
        data = np.zeros((2000, 2000, 3))
        source = RawDataSource(data)
        P.open_source(source)
        P.show_source(source)

    @staticmethod
    def open_source(source: DataSource):
        P.log.debug(f'open source: {source}')
        P.model().sources.append(source)

    @staticmethod
    def open_sources(sources: Iterator[DataSource]):
        P.log.debug(f'open sources: {sources}')
        P.model().sources.extend(sources)

    @staticmethod
    def show_source(source: DataSource):
        P.main_window.set_source(source)

    @staticmethod
    def update_status(text: str):
        if P.main_window:
            status = P.main_window.statusBar()
            status.showMessage(text)

    @staticmethod
    def change_layout(layout: str):
        if layout is 'tabs':
            P.main_window.tabs_layout()
        elif layout is 'mosaic':
            P.main_window.mosaic_layout()
