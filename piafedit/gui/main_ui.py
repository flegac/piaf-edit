import logging
from pathlib import Path
from typing import Any

from PyQt5.QtCore import QMutex
from PyQt5.QtWidgets import QFileSystemModel, QMainWindow, QVBoxLayout, QWidget

from piafedit.editor_api import P
from piafedit.gui.action_mapper import ActionMapper
from piafedit.gui.browser.source_browser import SourceBrowser
from piafedit.gui.image.image_manager import ImageManager
from piafedit.gui.worker_creator import create_worker
from piafedit.model.libs.filters import erode, edge_detection, dilate
from piafedit.model.source.data_source import DataSource
from piafedit.model.source.rio_data_source import RIODataSource
from piafedit.ui_utils import load_ui, resources_path
from qtwidgets.browser.browser_config import BrowserConfig, Item, Page
from qtwidgets.console.console_config import ConsoleConfig
from qtwidgets.console.console_widget import ConsoleWidget
from qtwidgets.observablelist import observablelist
from qtwidgets.worker.worker_manager_widget import WorkerManagerWidget


class MainUi(QMainWindow):
    EXIT_CODE_REBOOT = -123

    def __init__(self, ):
        super().__init__()
        load_ui('main', self)
        self.show()
        self.manager = None
        self.source = None

        self.lock = QMutex()

        # file browser
        self.setup_file_browser(resources_path())

        logs = ConsoleWidget(ConsoleConfig(
            'toto',
            loggers=[logging.getLogger()]
        ))
        self.setup(self.console, logs)

        processes = WorkerManagerWidget(
            model=observablelist([
                create_worker() for i in range(10)
            ]),
            config=BrowserConfig(
                item=Item(width=250),
                page=Page(size=1)
            )
        )
        self.setup(self.worker, processes)

        # browser
        self.browser = SourceBrowser(
            config=BrowserConfig(
                page=Page(size=20)
            )
        )
        self.setup(self.images, self.browser)

        self.setup_tool_box()

        self.actions = ActionMapper(self)

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

    def set_source(self, source: DataSource):
        self.lock.lock()
        try:
            self.source = source
            manager = ImageManager(source)
            # TODO fix that
            if self.manager:
                self.overview.layout().replaceWidget(self.manager.overview, manager.overview)
                self.setCentralWidget(manager.view)
                self.manager.view.close()
                self.manager.overview.close()
            else:
                self.setup(self.overview, manager.overview)
                self.setCentralWidget(manager.view)
                # self.setup(self.image, manager.view)

            self.manager = manager
        finally:
            self.lock.unlock()

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
            self.set_source(source)

    def on_click(self, ev):
        print(f'clicked: {ev}')
