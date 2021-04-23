from pathlib import Path
from typing import List

from PyQt5.QtWidgets import QFileDialog, QWidget

from piafedit.config.config import Win
from piafedit.data_source.data_source import DataSource
from piafedit.gui.editor_window import EditorWindow
from piafedit.gui.image.image_manager import ImageManager


class P:
    main_window: EditorWindow = None

    @staticmethod
    def select_files() -> List[str]:
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setDirectory(str(Path('.').absolute()))
        # dialog.setFilter('Image files (*.jpg *.gif)')

        if dialog.exec():
            filenames = dialog.selectedFiles()
            print(filenames)
            return filenames

    @staticmethod
    def display(widget: QWidget):
        P.main_window.show_widget(widget)

    @staticmethod
    def select_source(source: DataSource):
        manager = ImageManager(source)
        win = P.main_window
        win.set_content(win.widgets[Win.view], manager.view)
        win.set_content(win.widgets[Win.overview], manager.overview)
        win.set_content(win.widgets[Win.infos], manager.panel)
