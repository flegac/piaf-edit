from PyQt5.QtWidgets import QWidget

from piafedit.ui_utils import load_ui


class FullOverview(QWidget):
    def __init__(self):
        super().__init__()
        load_ui('overview', self)
        from piafedit.editor_api import P
        self.newButton.clicked.connect(lambda: P.main_window.show_view())
        self.clearButton.clicked.connect(lambda: self.image.views.clear())
        self.histogramButton.clicked.connect(lambda: self.image.views.switch_histogram())

        self.mosaicButton.clicked.connect(lambda: self.change_layout('mosaic'))
        self.tabsButton.clicked.connect(lambda: self.change_layout('tabs'))
        self.current_layout = 'mosaic'

    def change_layout(self, value: str):
        from piafedit.editor_api import P
        self.current_layout = value
        P.change_layout(value)

    def closeEvent(self, ev) -> None:
        self.image.close()
        self.infos.close()
        super().closeEvent(ev)
