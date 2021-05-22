from pathlib import Path
from typing import Any

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget, QSplitter

from piafedit.editor_api import P
from piafedit.gui.action_mapper import ActionMapper
from piafedit.gui.browser.source_browser import SourceBrowser
from piafedit.gui.image.full_overview import FullOverview
from piafedit.gui.image.overview import Overview
from piafedit.model.libs.operator import Operator
from piafedit.model.source.data_source import DataSource
from piafedit.model.source.rio_data_source import RIODataSource
from piafedit.model.work_model import WorkModel
from piafedit.ui_utils import load_ui
from qtwidgets.browser.browser_config import BrowserConfig, Page
from qtwidgets.worker.worker_manager_widget import WorkerManagerWidget


class MainUi(QMainWindow):
    EXIT_CODE_REBOOT = -123

    def __init__(self, model: WorkModel):
        super().__init__()
        load_ui('main', self)
        # self.setCentralWidget(None)
        self.setDockOptions(QMainWindow.GroupedDragging | QMainWindow.AllowTabbedDocks | QMainWindow.AllowNestedDocks)

        self.model = model
        self.current_view: Overview = None
        self.setup_file_browser()

        processes: WorkerManagerWidget = self.worker
        processes.set_model(self.model.workers)

        # browser
        images: SourceBrowser = self.images
        images.set_model(self.model.sources)
        images.set_config(BrowserConfig(
            page=Page(size=20)
        ))

        self.actions = ActionMapper(self)
        if self.current_view:
            self.set_source(self.current_view.source)

        tabs: QTabWidget = self.image

        def close_tab(index):
            tabs.removeTab(index)

        tabs.tabCloseRequested.connect(close_tab)

        self.actions.load_gui() or self.actions.restore_default_gui()
        self.show()

    def change_layout(self, layout: str):
        if layout is 'tabs':
            self.tabs_layout()
        elif layout is 'mosaic':
            self.mosaic_layout()

    def mosaic_layout(self):

        old_size = self.centralWidget().size()

        widget = QSplitter()
        widget.setOrientation(Qt.Horizontal)

        overview: FullOverview = self.current_view
        for view in overview.image.views.views:
            widget.addWidget(view)
            view.show()

        widget.show()
        widget.resize(old_size)
        self.setCentralWidget(widget)

    def tabs_layout(self):
        old_size = self.centralWidget().size()
        widget = QTabWidget()
        widget.resize(old_size)

        def close_tab(index):
            widget.removeTab(index)

        widget.tabCloseRequested.connect(close_tab)

        index = None
        overview: FullOverview = self.current_view
        for view in overview.image.views.views:
            index = widget.addTab(view, view.view_name())
        widget.setCurrentIndex(index)

        self.setCentralWidget(widget)

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

    def show_view(self, op: Operator = None):
        view = self.current_view.image.create_view(op)
        self.change_layout(self.current_view.current_layout)

    def set_source(self, source: DataSource):
        overview = FullOverview()
        overview.image.set_source(source)
        overview.infos.update_overview(overview.image)

        if self.current_view:
            self.overview.layout().replaceWidget(self.current_view, overview)
            self.current_view.close()
        else:
            self.setup(self.overview, overview)

        self.current_view = overview

        self.show_view(None)

    def on_select(self, ev):
        paths = set(
            Path(self.model.tree_model.filePath(idx))
            for idx in ev.indexes()
        )
        sources = list(map(RIODataSource, paths))
        P.open_sources(sources)
        self.set_source(P.model().sources[-1])

    def on_click(self, ev):
        print(f'clicked: {ev}')
