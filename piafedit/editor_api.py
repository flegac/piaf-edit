import logging
from pathlib import Path

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
        files = select_files()
        for file in files:
            P.open_source(RIODataSource(Path(file)))

    @staticmethod
    def new_source():
        data = np.zeros((2000, 2000, 3))
        source = RawDataSource(data)
        P.open_source(source)
        P.show_source(source)

    @staticmethod
    def open_source(source: DataSource):
        P.log.debug(f'open source: {source}')
        model = P.model()
        model.sources += [source]

    @staticmethod
    def show_source(source: DataSource):
        P.main_window.set_source(source)

    @staticmethod
    def update_status(text: str):
        if P.main_window:
            status = P.main_window.statusBar()
            status.showMessage(text)
