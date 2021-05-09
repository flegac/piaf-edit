import logging

from PyQt5.QtWidgets import *

from piafedit.config.config import WinConfig
from piafedit.gui2.browser.source_browser import SourceBrowser
from qtwidgets.console.console_widget import ConsoleWidget
from piafedit.gui.dock_panel import DockPanel
from piafedit.gui.image.image_manager import ImageManager
from piafedit.gui.tool_bar import ToolBar
from piafedit.gui.widgets_enum import Widgets
from piafedit.model.source.data_source import DataSource


class EditorWindow(QMainWindow):
    def __init__(self, config: WinConfig):
        super().__init__()
        self.setGeometry(0, 0, 1024, 1024)
        self.config = config
        self.dock = DockPanel()
        self.browser = SourceBrowser(100)

        self.setWindowTitle(config.title)
        self.resize(*config.size.raw())
        self.setCentralWidget(self.dock.area)

        LayoutBuilder(self).build()
        MenuLoader(self).load()

    def set_source(self, source: DataSource):
        manager = ImageManager(source)
        self.dock.set_content(self.widgets[Widgets.view], manager.view)
        self.dock.set_content(self.widgets[Widgets.overview], manager.overview)

    def show_widget(self, widget: QWidget):
        dock = self.get_dock(Widgets.view)
        self.set_content(dock, widget)

    def get_dock(self, win_id: Widgets):
        return self.widgets.get(win_id)


class LayoutBuilder:
    def __init__(self, win: EditorWindow):
        self.win = win

    def build(self):
        browser = self.win.dock.add_dock(
            'browser',
            widget=self.win.browser,
            size=self.win.config.layout.browser
        )
        view = self.win.dock.add_dock(
            'view',
            widget=None,
            size=self.win.config.layout.view
        )
        overview = self.win.dock.add_dock(
            'overview',
            widget=None,
            size=self.win.config.layout.overview
        )

        toolbar = self.win.dock.add_dock(
            'tools',
            widget=ToolBar(),
            size=self.win.config.layout.tools
        )

        logs = ConsoleWidget('toto')
        logs.add_logger(logging.getLogger())
        console = self.win.dock.add_dock(
            'console',
            widget=logs,
            size=self.win.config.layout.tools
        )

        self.win.widgets = {
            Widgets.view: view,
            Widgets.browser: browser,
            Widgets.overview: overview,
            Widgets.toolbar: toolbar,
            Widgets.console: console,
        }
        self.win.dock.area.moveDock(console, 'bottom', view)
        self.win.dock.area.moveDock(toolbar, 'left', view)
        self.win.dock.area.moveDock(browser, 'right', view)
        self.win.dock.area.moveDock(overview, 'top', browser)
        self.win.dock.lock_ui(True)
        self.win.statusBar().showMessage('')


class MenuLoader:
    def __init__(self, win: QMainWindow):
        self.win = win

    def load(self):
        menu = self.win.menuBar()

        file = menu.addMenu('File')
        file.addAction(self.open())
        file.addSeparator()
        file.addAction(self.exit())

        edit = menu.addMenu('Edit')
        view = menu.addMenu('View')
        view.addAction(self.save_ui())
        view.addAction(self.restore_ui())
        view.addAction(self.switch_ui_lock())

        help = menu.addMenu('Help')

    def restore_ui(self):
        from piafedit.editor_api import P
        action = QAction('Restore UI', self.win)
        action.triggered.connect(P.restore)
        return action

    def save_ui(self):
        from piafedit.editor_api import P
        action = QAction('Save UI', self.win)
        action.triggered.connect(P.save)
        return action

    def switch_ui_lock(self):
        from piafedit.editor_api import P
        action = QAction('Switch UI lock', self.win)
        action.triggered.connect(P.switch_lock)
        return action

    def open(self):
        from piafedit.editor_api import P
        action = QAction('Open', self.win)
        action.setShortcut("Alt+O")
        action.setStatusTip('Exit application')
        action.triggered.connect(P.open_files)
        return action

    def exit(self):
        action = QAction('Exit', self.win)
        action.setShortcut("Alt+X")
        action.setStatusTip('Exit application')
        action.triggered.connect(self.win.close)
        return action
