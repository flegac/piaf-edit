import logging
from pathlib import Path
from typing import Any

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from piafedit.editor_api import P
from piafedit.gui.action_mapper import ActionMapper
from piafedit.gui.browser.source_browser import SourceBrowser
from piafedit.gui.image.full_overview import FullOverview
from piafedit.gui.image.overview import Overview
from piafedit.model.source.data_source import DataSource
from piafedit.model.source.rio_data_source import RIODataSource
from piafedit.model.work_model import WorkModel
from piafedit.ui_utils import load_ui
from qtwidgets.browser.browser_config import BrowserConfig, Page
from qtwidgets.browser.browser_widget import BrowserWidget
from qtwidgets.worker.worker_manager_widget import WorkerManagerWidget

log = logging.getLogger()


class MainUi(QMainWindow):
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

        # source browser
        self.source_browser.set_model(self.model.sources)
        self.source_browser.set_config(BrowserConfig(
            page=Page(size=20)
        ))

        self.actions = ActionMapper(self)
        if self.current_view:
            self.set_source(self.current_view.source)

        self.actions.load_gui() or self.actions.restore_default_gui()
        self.show()

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
        overview = FullOverview()
        overview.view.set_source(source)
        overview.infos.update_overview(overview.view)

        if self.current_view:
            self.overview.layout().replaceWidget(self.current_view, overview)
            self.current_view.close()
        else:
            self.setup(self.overview, overview)

        self.current_view = overview
        self.current_view.create_view()
        self.current_view.create_view()

        self.main_view.set_model(overview.view.views.views)

    def on_select(self, ev):
        paths = set(
            Path(self.model.tree_model.filePath(idx))
            for idx in ev.indexes()
        )
        sources = []
        for path in paths:
            try:
                sources.append(RIODataSource(path))
            except:
                log.warning(f'could not open source: {path}')
        P.open_sources(sources)
        self.set_source(P.model().sources[-1])

    def on_click(self, ev):
        print(f'clicked: {ev}')

    @property
    def source_browser(self) -> SourceBrowser:
        return self.sourceBrowser

    @property
    def main_view(self) -> BrowserWidget:
        return self.mainView
