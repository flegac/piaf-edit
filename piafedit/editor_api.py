import logging
from pathlib import Path

from PyQt5.QtWidgets import QWidget

from piafedit.gui.editor_window import EditorWindow
from piafedit.gui.image.image_manager import ImageManager
from piafedit.gui.utils import select_files
from piafedit.gui.widgets_enum import Widgets
from piafedit.model.source.data_source import DataSource
from piafedit.model.source.rio_data_source import RIODataSource


class P:
    log = logging.getLogger()
    main_window: EditorWindow = None

    @staticmethod
    def show_widget(widget: QWidget):
        P.main_window.show_widget(widget)

    @staticmethod
    def open_files():
        files = select_files()
        for file in files:
            P.open_source(RIODataSource(Path(file)))

    @staticmethod
    def open_source(source: DataSource):
        P.log.debug(f'open source: {source}')
        P.main_window.browser.register(source)

    @staticmethod
    def show_source(source: DataSource):
        manager = ImageManager(source)
        win = P.main_window
        win.dock.set_content(win.widgets[Widgets.view], manager.view)
        win.dock.set_content(win.widgets[Widgets.overview], manager.overview)

    @staticmethod
    def update_status(text: str):
        P.main_window.statusBar().showMessage(text)

    @staticmethod
    def save():
        P.main_window.dock.save()

    @staticmethod
    def restore():
        P.main_window.dock.restore()

    @staticmethod
    def switch_lock():
        P.main_window.dock.switch_lock()
