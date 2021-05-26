from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QCheckBox, QStyle

from piafedit.gui.browser.source_browser import SourceBrowser
from piafedit.gui.image.overview import Overview
from piafedit.ui_utils import load_ui
from qtwidgets.browser.browser_config import BrowserConfig


class FullOverview(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        load_ui('overview', self)
        self.bestAspectButton.setIconSize(QSize(32, 32))

        buttons = {
            'best_aspect': (self.bestAspectButton, QIcon.fromTheme('view-fullscreen')),
            'new': (self.newButton, self.style().standardIcon(QStyle.SP_DialogOpenButton)),
            'clear': (self.clearButton, self.style().standardIcon(QStyle.SP_DialogCloseButton)),
        }
        for (btn, icon) in buttons.values():
            btn.setText(None)
            btn.setIcon(icon)
            btn.setIconSize(QSize(32, 32))

        self.bestAspectButton.clicked.connect(lambda: self.optimize_aspect())
        self.clearButton.clicked.connect(lambda: self.overview.views.clear())
        self.newButton.clicked.connect(lambda: self.overview.create_view())
        self.newButton.hide()
        self.clearButton.hide()

        self.autofitControl.stateChanged.connect(self.set_autofit)

        self.histogramControl.stateChanged.connect(lambda status: self.overview.views.set_histogram(status))
        self.toolBarControl.stateChanged.connect(self.set_toolbar)
        self.layoutCombo.currentTextChanged.connect(self.on_layout_change)

    def optimize_aspect(self):
        browser = self.source_browser
        w = browser.config.item_per_line
        h = int(browser.config.item_per_page / w)
        table_aspect = w / h

        self.overview.optimize_aspect(table_aspect)

    def set_autofit(self, status: bool):
        if status:
            self.optimize_aspect()

    def set_toolbar(self, status: bool):
        self.overview.views.set_toolbar(status)
        browser = self.source_browser
        browser.config.tool_bar = status
        browser.request_update()

    @property
    def autofit(self):
        autofit: QCheckBox = self.autofitControl
        return autofit.isChecked()

    def create_view(self):
        return self.overview.create_view()

    def closeEvent(self, ev) -> None:
        self.overview.close()
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

        browser = self.source_browser
        browser.config.tool_bar = config.tool_bar
        browser.config.item_per_line = config.item_per_line
        browser.config.item_per_page = config.item_per_page
        if self.autofit:
            self.optimize_aspect()
        browser.request_update()

    @property
    def source_browser(self) -> SourceBrowser:
        return self.browser

    @property
    def overview(self) -> Overview:
        return self.view

    @property
    def tool_bar_control(self) -> QCheckBox:
        return self.toolBarControl
