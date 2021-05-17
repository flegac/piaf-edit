from pathlib import Path

from PyQt5.QtWidgets import QMainWindow

from piafedit.editor_api import P
from piafedit.model.libs.filters import erode, dilate, edge_detection
from piafedit.ui_utils import resources_path

LAYOUT_BACKUP__PATH = Path('layout.gui')


class ActionMapper:
    def __init__(self, win: QMainWindow):
        self.win = win
        self.setup_files()
        self.setup_operators()
        self.setup_tools()
        self.setup_view()

    @property
    def manager(self):
        return self.win.manager

    def setup_operators(self):
        self.win.actionEdge_detection.triggered.connect(lambda: self.manager.set_operator(edge_detection))
        self.win.actionErode.triggered.connect(lambda: self.manager.set_operator(erode))
        self.win.actionDilate.triggered.connect(lambda: self.manager.set_operator(dilate))
        self.win.actionIdentity.triggered.connect(lambda: self.manager.set_operator(None))

    def setup_tools(self):
        self.win.actionConsole.triggered.connect(lambda: self.win.consoleDock.show())
        self.win.actionOverview.triggered.connect(lambda: self.win.overviewDock.show())
        self.win.actionTreeview.triggered.connect(lambda: self.win.treeviewDock.show())
        self.win.actionImages.triggered.connect(lambda: self.win.imagesDock.show())
        self.win.actionWorkers.triggered.connect(lambda: self.win.workerDock.show())

    def setup_view(self):
        self.win.action100.triggered.connect(print)
        self.win.actionRestore_layout.triggered.connect(self.restore_default_gui)
        self.win.actionSave_layout.triggered.connect(self.save_gui)
        self.win.actionLoad_layout.triggered.connect(self.load_gui)
        self.win.actionLoad_layout.setDisabled(not LAYOUT_BACKUP__PATH.exists())
        self.restore_default_gui()

    def setup_files(self):
        self.win.actionNew.triggered.connect(P.new_source)
        self.win.actionOpen.triggered.connect(P.open_source)
        self.win.actionSave.triggered.connect(print)
        self.win.actionSave_as.triggered.connect(print)
        self.win.actionClose.triggered.connect(print)
        self.win.actionExit.triggered.connect(print)
        self.win.actionRestart.triggered.connect(P.restart)

    def save_gui(self):
        with LAYOUT_BACKUP__PATH.open('wb') as _:
            _.write(self.win.saveState())
        self.win.actionLoad_layout.setDisabled(False)

    def load_gui(self):
        self.load_gui_from(Path('layout.gui'))

    def restore_default_gui(self):
        self.load_gui_from(resources_path() / 'ui/layout.gui')

    def load_gui_from(self, path: Path):
        with path.open('rb') as _:
            state = _.read()
        self.win.restoreState(state)
