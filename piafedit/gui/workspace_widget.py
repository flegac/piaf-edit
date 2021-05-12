import logging
from pathlib import Path
from typing import Any

from PyQt5.QtWidgets import QFileSystemModel, QVBoxLayout, QWidget, QApplication

from piafedit.app_v2 import gen_big_image
from piafedit.editor_api import P
from piafedit.gui.image.image_manager import ImageManager
from piafedit.gui.browser.source_browser import SourceBrowser
from piafedit.model.libs.filters import erode, edge_detection, dilate
from piafedit.model.source.data_source import DataSource
from piafedit.model.source.rio_data_source import RIODataSource
from piafedit.ui_utils import load_ui
from qtwidgets.browser.browser_config import BrowserConfig, Page
from qtwidgets.console.console_config import ConsoleConfig
from qtwidgets.console.console_widget import ConsoleWidget


class WorkspaceWidget(QWidget):

    def __init__(self):
        super().__init__()
        load_ui('workspace', self)
        self.show()

        logs = ConsoleWidget(ConsoleConfig(
            'toto',
            loggers=[logging.getLogger()]
        ))
        self.setup(self.console, logs)

        # browser
        self.browser = SourceBrowser(
            config=BrowserConfig(
                page=Page(size=20)
            )
        )
        self.setup(self.images, self.browser)

        # view / overview
        self.manager: ImageManager = None
        self.source = None

    def setup(self, placeholder: QWidget, widget: Any):
        placeholder.setLayout(QVBoxLayout())
        placeholder.layout().addWidget(widget)

    def setup_file_browser(self, root_dir: Path):
        self.tree_model = QFileSystemModel()
        path = str(root_dir)
        self.tree_model.setRootPath(path)
        self.treeView.setModel(self.tree_model)
        self.treeView.selectionModel().selectionChanged.connect(self.on_select)
        self.treeView.doubleClicked.connect(self.on_click)
        self.treeView.setRootIndex(self.tree_model.index(path))

    def setup_tool_box(self):
        self.erodeButton.clicked.connect(lambda: self.manager.set_operator(erode))
        self.dilateButton.clicked.connect(lambda: self.manager.set_operator(dilate))
        self.edgeButton.clicked.connect(lambda: self.manager.set_operator(edge_detection))
        self.identityButton.clicked.connect(lambda: self.manager.set_operator(None))

    def setup_menu(self):
        # TODO:
        self.actionNew.triggered.connect(P.new_source)

    def set_source(self, source: DataSource):
        self.source = source
        manager = ImageManager(source)

        if self.manager:
            self.overview.layout().replaceWidget(self.manager.overview, manager.overview)
            self.imageView.layout().replaceWidget(self.manager.view, manager.view)
        else:
            layout = QVBoxLayout()
            layout.addWidget(manager.overview)
            self.overview.setLayout(layout)

            layout = QVBoxLayout()
            layout.addWidget(manager.view)
            self.imageView.setLayout(layout)

        self.manager = manager

    def on_select(self, ev):
        paths = set(
            Path(self.tree_model.filePath(idx))
            for idx in ev.indexes()
        )
        source = None
        for path in paths:
            try:
                source = RIODataSource(path)
                P.open_source(source)
            except Exception as e:
                logging.warning(f'Fail reading image: {path}')
        if source:
            P.show_source(source)

    def on_click(self, ev):
        print(f'clicked: {ev}')


if __name__ == '__main__':
    import pyqtgraph as pg

    pg.setConfigOptions(imageAxisOrder='row-major')
    app = QApplication([])

    workspace = WorkspaceWidget()

    source = gen_big_image()
    workspace.set_source(source)
    app.exec_()
