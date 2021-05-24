from PyQt5.QtWidgets import QWidget

from piafedit.gui.browser.source_browser import SourceBrowser
from piafedit.ui_utils import load_ui
from qtwidgets.browser.browser_config import BrowserConfig


class FullOverview(QWidget):
    def __init__(self):
        super().__init__()
        load_ui('overview', self)
        self.bestAspectButton.clicked.connect(lambda: self.view.optimize_aspect())

        self.newButton.clicked.connect(lambda: self.view.create_view())
        self.clearButton.clicked.connect(lambda: self.view.views.clear())
        self.histogram.stateChanged.connect(lambda status: self.view.views.set_histogram(status))
        self.config.stateChanged.connect(lambda status: self.view.views.set_config(status))
        self.layoutCombo.currentTextChanged.connect(self.on_layout_change)

    def create_view(self):
        return self.view.create_view()

    def closeEvent(self, ev) -> None:
        self.view.close()
        self.infos.close()
        super().closeEvent(ev)

    def on_layout_change(self, name: str):
        cases = {
            '1x1': BrowserConfig(
                item_per_line=1,
                item_per_page=1,
            ),
            '2x1': BrowserConfig(
                item_per_line=2,
                item_per_page=2,
            ),

            '2x2': BrowserConfig(
                item_per_line=2,
                item_per_page=4,
            ),

            '3x2': BrowserConfig(
                item_per_line=3,
                item_per_page=6,
            ),
            '3x3': BrowserConfig(
                item_per_line=3,
                item_per_page=9,
            ),
        }

        config = cases[name]

        from piafedit.editor_api import P
        browser: SourceBrowser = P.main_window.main_view

        browser.set_config(config)
