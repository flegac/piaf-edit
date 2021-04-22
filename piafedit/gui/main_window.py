from PyQt5.QtWidgets import *
from pyqtgraph.dockarea import Dock

from piafedit.config.config import WinConfig, Win
from piafedit.gui.dock_panel import DockPanel


class MainWindow(QMainWindow):
    def __init__(self, config: WinConfig):
        super().__init__()
        self.dock = DockPanel()
        self.setWindowTitle(config.title)
        self.resize(*config.size.raw())
        self.setCentralWidget(self.dock.area)

        view = self.dock.add_dock('view', size=config.layout.view)
        overview = self.dock.add_dock('overview', size=config.layout.overview)
        toolbar = self.dock.add_dock('tools', size=config.layout.tools)
        infos = self.dock.add_dock('infos')
        self.widgets = {
            Win.view: view,
            Win.overview: overview,
            Win.toolbar: toolbar,
            Win.infos: infos,
        }
        self.dock.area.moveDock(toolbar, 'left', view)
        self.dock.area.moveDock(overview, 'top', toolbar)
        self.dock.area.moveDock(infos, 'bottom', overview)

        self.set_content(toolbar, self.dock.panel)
        self.dock.lock_ui(True)

    def set_content(self, dock: Dock, widget: QWidget):
        dock.addWidget(widget)

    def get_dock(self, win_id: Win):
        return self.widgets.get(win_id)
