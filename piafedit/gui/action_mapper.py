from pathlib import Path
from typing import Optional

from PyQt5.QtWidgets import QMainWindow, QDockWidget

from piafedit.editor_api import P
from piafedit.gui.image.overview import Overview
from piafedit.model.libs.filters import erode, dilate, edge_detection
from piafedit.model.libs.operator import Operator
from piafedit.ui_utils import resources_path

LAYOUT_BACKUP_PATH = Path('layout.gui')


class ActionMapper:
    def __init__(self, win: QMainWindow):
        self.win = win
        self.setup_files()
        self.setup_operators()
        self.setup_tools()
        self.setup_view()

    @property
    def overview(self) -> Overview:
        return self.win.current_view

    def setup_operators(self):
        def operator_setter(op: Optional[Operator]):
            def action():
                self.win.show_view(op)

            return action

        self.win.actionEdge_detection.triggered.connect(operator_setter(edge_detection))
        self.win.actionErode.triggered.connect(operator_setter(erode))
        self.win.actionDilate.triggered.connect(operator_setter(dilate))
        self.win.actionIdentity.triggered.connect(operator_setter(None))

    def setup_tools(self):
        def switcher(widget: QDockWidget):
            def action():
                if widget.isHidden():
                    widget.show()
                else:
                    widget.hide()
            return action

        self.win.actionConsole.triggered.connect(switcher(self.win.consoleDock))
        self.win.actionOverview.triggered.connect(switcher(self.win.overviewDock))
        self.win.actionTreeview.triggered.connect(switcher(self.win.treeviewDock))
        self.win.actionImages.triggered.connect(switcher(self.win.imagesDock))
        self.win.actionWorkers.triggered.connect(switcher(self.win.workerDock))

    def setup_view(self):
        self.win.action100.triggered.connect(print)
        self.win.actionRestore_layout.triggered.connect(self.restore_default_gui)
        self.win.actionSave_layout.triggered.connect(self.save_gui)
        self.win.actionLoad_layout.triggered.connect(self.load_gui)
        self.win.actionHistogram.triggered.connect(self.switch_histogram)
        self.win.actionLoad_layout.setDisabled(not LAYOUT_BACKUP_PATH.exists())

    def setup_files(self):
        self.win.actionNew.triggered.connect(P.new_source)
        self.win.actionOpen.triggered.connect(P.open_source)
        self.win.actionSave.triggered.connect(print)
        self.win.actionSave_as.triggered.connect(print)
        self.win.actionClose.triggered.connect(print)
        self.win.actionExit.triggered.connect(print)
        self.win.actionRestart.triggered.connect(P.restart)

    def switch_histogram(self):
        if self.overview:
            self.overview.image.switch_histogram()

    def save_gui(self):
        with LAYOUT_BACKUP_PATH.open('wb') as _:
            _.write(self.win.saveState())
        self.win.actionLoad_layout.setDisabled(False)

    def load_gui(self):
        return self.load_gui_from(LAYOUT_BACKUP_PATH)

    def restore_default_gui(self):
        return self.load_gui_from(resources_path() / 'ui/layout.gui')

    def load_gui_from(self, path: Path):
        if not path.exists():
            return False
        with path.open('rb') as _:
            state = _.read()
        self.win.restoreState(state)
        return True
