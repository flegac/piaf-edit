import logging
from typing import Any, Callable

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QMoveEvent, QResizeEvent, QWindowStateChangeEvent
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from piafedit.config.config import PiafConfig
from piafedit.gui.action_mapper import ActionMapper
from piafedit.gui.browser.source_browser import SourceBrowser
from piafedit.gui.common.config_utils import synchronize_widget, synchronize_config
from piafedit.gui.file_browser import FileBrowser
from piafedit.gui.image.full_overview import FullOverview
from piafedit.model.source.data_source import DataSource
from piafedit.model.work_model import WorkModel
from piafedit.ui_utils import load_ui
from qtwidgets.dock_widget import DockWidget
from qtwidgets.worker.worker_manager_widget import WorkerManagerWidget

log = logging.getLogger()


class MainUi(QMainWindow):
    def __init__(self, model: WorkModel):
        super().__init__()
        load_ui('main', self)
        self.setDockOptions(QMainWindow.GroupedDragging | QMainWindow.AllowTabbedDocks | QMainWindow.AllowNestedDocks)

        self.model = model

        # widgets
        self.source_browser.set_model(self.model.sources)
        self.worker_browser.set_model(self.model.workers)
        self.file_browser.setup_model(self.model.tree_model)
        self.main_view.source_browser.config.tool_bar = False
        self.main_view.source_browser.request_update()

        # actions
        self.actions = ActionMapper(self)
        self.actions.load_gui() or self.actions.restore_default_gui()

        # gui config
        self.config = PiafConfig()
        synchronize_widget(self, self.config.window)

    def open_dock(self, title: str, factory: Callable[[], QWidget]):
        widget = factory()
        dock = DockWidget(title)
        dock.setWidget(widget)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.tabifyDockWidget(self.consoleDock, dock)
        dock.show()
        dock.raise_()

    def setup(self, placeholder: QWidget, widget: Any):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(widget)
        placeholder.setLayout(layout)

    def set_source(self, source: DataSource):
        main_view = self.main_view
        overview = main_view.overview
        overview.set_source(source)
        views = overview.views

        while len(views.views) < 6:
            main_view.create_view()
        main_view.source_browser.set_model(views.views)

    # ---- EVENTS -----------------------------------------------------

    def changeEvent(self, ev: QEvent):
        super().changeEvent(ev)
        if isinstance(ev, QWindowStateChangeEvent):
            synchronize_config(self, self.config.window)

    def moveEvent(self, ev: QMoveEvent):
        synchronize_config(self, self.config.window)

    def resizeEvent(self, ev: QResizeEvent):
        synchronize_config(self, self.config.window)

    # ---- GUI widgets ------------------------------------------------

    @property
    def main_view(self) -> FullOverview:
        return self.mainView

    @property
    def file_browser(self) -> FileBrowser:
        return self.fileBrowser

    @property
    def source_browser(self) -> SourceBrowser:
        return self.sourceBrowser

    @property
    def worker_browser(self) -> WorkerManagerWidget:
        return self.workerBrowser
