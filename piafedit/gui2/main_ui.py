import logging
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QFileSystemModel, QMainWindow, QVBoxLayout

from piafedit.gui.browser.source_browser import SourceBrowser
from piafedit.gui.image.image_manager import ImageManager
from piafedit.gui2.worker_creator import create_worker
from piafedit.model.libs.filters import erode, edge_detection, dilate
from piafedit.model.source.data_source import DataSource
from piafedit.model.source.rio_data_source import RIODataSource
from qtwidgets.console.console_config import ConsoleConfig
from qtwidgets.console.console_widget import ConsoleWidget
from qtwidgets.flow.flow_config import FlowConfig, Item, Page
from qtwidgets.tasker.tasker_widget import TaskerWidget


class MainUi(QMainWindow):
    def __init__(self, root_dir: Path):
        super(MainUi, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi(root_dir / 'ui/main.ui', self)  # Load the .ui file
        self.show()

        # treeView
        self.tree_model = QFileSystemModel()
        path = str(root_dir)
        self.tree_model.setRootPath(path)
        self.treeView.setModel(self.tree_model)
        self.treeView.selectionModel().selectionChanged.connect(self.on_select)
        self.treeView.doubleClicked.connect(self.on_click)
        self.treeView.setRootIndex(self.tree_model.index(path))

        logs = ConsoleWidget(ConsoleConfig(
            'toto',
            loggers=[logging.getLogger()]
        ))
        self.console.setLayout(QVBoxLayout())
        self.console.layout().addWidget(logs)

        self.worker.setLayout(QVBoxLayout())
        processes = TaskerWidget(
            workers=[
                create_worker() for i in range(10)
            ],
            config=FlowConfig(
                item=Item(width=250),
                page=Page(size=1)
            )
        )
        self.worker.layout().addWidget(processes)

        # toolbox
        self.erodeButton.clicked.connect(lambda: self.manager.set_operator(erode))
        self.dilateButton.clicked.connect(lambda: self.manager.set_operator(dilate))
        self.edgeButton.clicked.connect(lambda: self.manager.set_operator(edge_detection))
        self.identityButton.clicked.connect(lambda: self.manager.set_operator(None))

        # browser
        self.browser = SourceBrowser(
            config=FlowConfig(
                item=Item(width=250),
                page=Page(size=20)
            )
        )
        self.images.setLayout(QVBoxLayout())
        self.images.layout().addWidget(self.browser)

        # view / overview
        self.manager = None
        self.source = None

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
        for idx in ev.indexes():
            path = Path(self.tree_model.filePath(idx))
            source = RIODataSource(path)
            self.set_source(source)

    def on_click(self, ev):
        print(f'clicked: {ev}')
