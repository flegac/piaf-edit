import logging
from pathlib import Path
from typing import Any

from PyQt5.QtCore import QMutex
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from piafedit.editor_api import P
from piafedit.gui.action_mapper import ActionMapper
from piafedit.gui.browser.source_browser import SourceBrowser
from piafedit.gui.image.image_manager import ImageManager
from piafedit.model.work_model import WorkModel
from piafedit.model.source.data_source import DataSource
from piafedit.model.source.rio_data_source import RIODataSource
from piafedit.ui_utils import load_ui
from qtwidgets.browser.browser_config import BrowserConfig, Item, Page
from qtwidgets.console.console_widget import ConsoleWidget
from qtwidgets.worker.worker_manager_widget import WorkerManagerWidget


class MainUi(QMainWindow):
    EXIT_CODE_REBOOT = -123

    def __init__(self, model: WorkModel):
        super().__init__()
        load_ui('main', self)
        self.show()
        self.manager = None
        self.source = None

        self.model = model

        self.lock = QMutex()

        self.setup_file_browser()

        console: ConsoleWidget = self.console
        console.set_loggers([logging.getLogger()])

        processes: WorkerManagerWidget = self.worker
        processes.set_model(self.model.workers)
        processes.set_config(BrowserConfig(
            item=Item(width=250),
            page=Page(size=2)
        ))

        # browser
        images: SourceBrowser = self.images
        images.set_model(self.model.sources)
        images.set_config(BrowserConfig(
            page=Page(size=20)
        ))

        self.actions = ActionMapper(self)

    def setup_file_browser(self):
        model = self.model.tree_model
        self.treeView.setModel(model)
        self.treeView.selectionModel().selectionChanged.connect(self.on_select)
        self.treeView.doubleClicked.connect(self.on_click)
        self.treeView.setRootIndex(model.index(model.rootPath()))

    def setup(self, placeholder: QWidget, widget: Any):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(widget)
        placeholder.setLayout(layout)

    def set_source(self, source: DataSource):
        self.lock.lock()
        try:
            self.source = source
            manager = ImageManager(source)
            manager.view.setMinimumWidth(self.centralWidget().width())
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
            Path(self.model.tree_model.filePath(idx))
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
