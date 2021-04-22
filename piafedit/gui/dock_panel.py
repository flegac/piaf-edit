import pyqtgraph as pg
from PyQt5.QtWidgets import QPushButton
from pyqtgraph.dockarea import DockArea, Dock

from piafedit.geometry.size import SizeAbs


class DockPanel:
    def __init__(self):
        super().__init__()
        self.area = DockArea()
        self.is_locked = False

        self.state = None
        self.restore_button = None
        self.panel = self.build_ui()

    def build_ui(self):
        lock_button = QPushButton('ui lock')
        lock_button.clicked.connect(self.switch_lock)

        save_button = QPushButton('Save layout')
        save_button.clicked.connect(self.save)

        self.restore_button = QPushButton('Restore layout')
        self.restore_button.clicked.connect(self.restore)
        self.restore_button.setEnabled(False)

        panel = pg.LayoutWidget()
        panel.addWidget(save_button, row=0, col=0)
        panel.addWidget(self.restore_button, row=1, col=0)
        panel.addWidget(lock_button, row=2, col=0)
        self.lock_ui(self.is_locked)
        return panel

    def save(self):
        self.state = self.area.saveState()
        self.restore_button.setEnabled(True)

    def restore(self):
        self.area.restoreState(self.state)

    def switch_lock(self):
        self.is_locked = not self.is_locked
        self.lock_ui(self.is_locked)

    def lock_ui(self, status: bool = True):
        self.is_locked = status
        for dock in self.area.docks.values():
            self.setup_lock(dock, status)

    def add_dock(self, name: str, size: SizeAbs = None):
        if size is not None:
            size = size.raw()
        else:
            size = (10, 10)
        dock = Dock(name, size=size)
        self.area.addDock(dock, 'above')
        self.setup_lock(dock, self.is_locked)
        return dock

    def setup_lock(self, dock: Dock, status: bool):
        if status:
            dock.hideTitleBar()
        else:
            dock.showTitleBar()
