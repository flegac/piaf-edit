from PyQt5.QtWidgets import QWidget

from piafedit.ui_utils import load_ui


class FullOverview(QWidget):
    def __init__(self):
        super().__init__()
        load_ui('overview', self)

        self.newButton.clicked.connect(lambda: self.view.create_view())
        self.clearButton.clicked.connect(lambda: self.view.views.clear())
        self.histogramButton.clicked.connect(lambda: self.view.views.switch_histogram())

    def create_view(self):
        return self.view.create_view()

    def closeEvent(self, ev) -> None:
        self.view.close()
        self.infos.close()
        super().closeEvent(ev)
