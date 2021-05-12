from pathlib import Path

from PyQt5.QtWidgets import QMainWindow

from piafedit.editor_api import P
from piafedit.ui_utils import resources_path

LAYOUT_BACKUP__PATH = Path('layout.gui')


class ActionMapper:
    def __init__(self, win: QMainWindow):
        self.win = win
        self.apply()

    def apply(self):
        # files
        self.win.actionNew.triggered.connect(P.new_source)
        self.win.actionOpen.triggered.connect(P.open_source)
        self.win.actionSave.triggered.connect(print)
        self.win.actionSave_as.triggered.connect(print)
        self.win.actionClose.triggered.connect(print)
        self.win.actionExit.triggered.connect(print)
        self.win.actionRestart.triggered.connect(P.restart)

        # tools
        self.win.actionLogs.triggered.connect(print)
        self.win.actionImages.triggered.connect(print)

        # view
        self.win.action100.triggered.connect(print)
        self.win.actionRestore_layout.triggered.connect(self.restore_default_gui)
        self.win.actionSave_layout.triggered.connect(self.save_gui)
        self.win.actionLoad_layout.triggered.connect(self.load_gui)
        self.win.actionLoad_layout.setDisabled(not LAYOUT_BACKUP__PATH.exists())
        self.restore_default_gui()

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
