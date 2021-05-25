from PyQt5.QtWidgets import QWidget, QCheckBox

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
        self.histogramControl.stateChanged.connect(lambda status: self.view.views.set_histogram(status))
        self.toolBarControl.stateChanged.connect(self.set_toolbar)
        self.layoutCombo.currentTextChanged.connect(self.on_layout_change)

    def set_toolbar(self, status: bool):
        self.view.views.set_toolbar(status)

        from piafedit.editor_api import P
        browser: SourceBrowser = P.main_window.main_view
        browser.config.tool_bar = status
        browser.set_config(browser.config)

    def create_view(self):
        return self.view.create_view()

    def closeEvent(self, ev) -> None:
        self.view.close()
        self.infos.close()
        super().closeEvent(ev)

    def on_layout_change(self, name: str):
        grids = [(1, 1), (2, 1), (2, 2), (3, 2), (3, 3)]
        cases = {
            f'{x}x{y}': BrowserConfig(
                item_per_line=x,
                item_per_page=x * y,
                tool_bar=self.tool_bar_control.isChecked()
            )
            for x, y in grids
        }

        config = cases[name]

        from piafedit.editor_api import P
        browser: SourceBrowser = P.main_window.main_view
        browser.config.tool_bar = config.tool_bar
        browser.config.item_per_line = config.item_per_line
        browser.config.item_per_page = config.item_per_page
        browser.request_update()

    @property
    def tool_bar_control(self) -> QCheckBox:
        return self.toolBarControl
