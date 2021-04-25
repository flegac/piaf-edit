from pathlib import Path

from PyQt5.QtWidgets import QWidget

from piafedit.config.config import Win
from piafedit.gui.editor_window import EditorWindow
from piafedit.gui.image.image_manager import ImageManager
from piafedit.gui.utils import select_files
from piafedit.model.source.data_source import DataSource
from piafedit.model.source.rio_data_source import RIODataSource


class P:
    main_window: EditorWindow = None

    @staticmethod
    def show_widget(widget: QWidget):
        P.main_window.show_widget(widget)

    @staticmethod
    def open_files():
        files = select_files()
        for file in files:
            P.open_source(RIODataSource(Path(file)))
        P.main_window.browser.update_layout()

    @staticmethod
    def open_source(source: DataSource):
        P.main_window.browser.open_source(source)

    @staticmethod
    def show_source(source: DataSource):
        manager = ImageManager(source)
        win = P.main_window
        win.set_content(win.widgets[Win.view], manager.view)
        win.set_content(win.widgets[Win.overview], manager.overview)

    @staticmethod
    def update_status(text: str):
        P.main_window.statusBar().showMessage(text)
