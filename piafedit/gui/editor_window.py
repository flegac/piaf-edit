import numpy as np
from PyQt5.QtWidgets import *
from pyqtgraph.dockarea import Dock

from piafedit.config.config import WinConfig, Win
from piafedit.gui.dock_panel import DockPanel
from piafedit.gui.layouts.flow_layout import FlowLayout
from piafedit.gui.layouts.utils import source_button
from piafedit.model.source.data_source import DataSource
from piafedit.model.source.simple_data_source import SimpleDataSource


class SourceBrowser(FlowLayout):
    def open_source(self, source: DataSource):
        self.register(source_button(source, size=230))


class EditorWindow(QMainWindow):
    def __init__(self, config: WinConfig):
        super().__init__()
        self.config = config
        self.dock = DockPanel()
        self.browser = SourceBrowser(1)
        for _ in range(7):
            w, h = 2000, int(2000/1.66)
            shape = (h, w, 3)
            buffer = np.random.randint(0, 255, size=shape).astype('uint8')
            source = SimpleDataSource(buffer)
            self.browser.open_source(source)
        self.browser.update_layout()

        self.setWindowTitle(config.title)
        self.resize(*config.size.raw())
        self.setCentralWidget(self.dock.area)

        LayoutBuilder(self).build()
        MenuLoader(self).load()

    def show_widget(self, widget: QWidget):
        dock = self.get_dock(Win.view)
        self.set_content(dock, widget)

    def set_content(self, dock: Dock, widget: QWidget):
        dock.currentRow = 1
        dock.widgets = [widget]
        dock.layout.addWidget(widget, dock.currentRow, 0, 1, 1)
        dock.raiseOverlay()

        # dock.addWidget(widget)

    def get_dock(self, win_id: Win):
        return self.widgets.get(win_id)


class LayoutBuilder:
    def __init__(self, win: EditorWindow):
        self.win = win

    def build(self):
        browser = self.win.dock.add_dock('browser', size=self.win.config.layout.browser)
        view = self.win.dock.add_dock('view', size=self.win.config.layout.view)
        overview = self.win.dock.add_dock('overview', size=self.win.config.layout.overview)
        toolbar = self.win.dock.add_dock('tools', size=self.win.config.layout.tools)
        infos = self.win.dock.add_dock('infos')
        self.win.widgets = {
            Win.view: view,
            Win.browser: browser,
            Win.overview: overview,
            Win.toolbar: toolbar,
            Win.infos: infos,
        }
        self.win.dock.area.moveDock(toolbar, 'bottom', view)
        self.win.dock.area.moveDock(browser, 'left', view)
        self.win.dock.area.moveDock(overview, 'top', browser)
        self.win.dock.area.moveDock(infos, 'bottom', overview)

        self.win.set_content(browser, self.win.browser)
        self.win.set_content(toolbar, self.win.dock.panel)
        self.win.dock.lock_ui(True)
        self.win.statusBar().showMessage('coucou')


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
        view.addSection('save UI')
        view.addSection('restore UI')
        view.addSection('lock UI')

        help = menu.addMenu('Help')

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
