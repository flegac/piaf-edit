import rx.operators as ops
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QCheckBox, QStyle

from piafedit.gui.common.template_widget import TemplateWidget
from piafedit.gui.image.views.overview import Overview
from piafedit.gui.image.view_browser import ViewBrowser
from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import RectAbs
from piafedit.model.source.window import Window
from qtwidgets.browser.browser_config import BrowserConfig


class FullOverview(TemplateWidget):
    def __init__(self, parent=None):
        super().__init__('overview', parent)
        self.bestAspectButton.setIconSize(QSize(32, 32))

        buttons = {
            'best_aspect': (self.bestAspectButton, QIcon.fromTheme('view-fullscreen')),
            'new': (self.newButton, self.style().standardIcon(QStyle.SP_DialogOpenButton)),
            'clear': (self.clearButton, self.style().standardIcon(QStyle.SP_DialogCloseButton)),
        }
        for (btn, icon) in buttons.values():
            btn.setText(None)
            btn.setIcon(icon)
            btn.setIconSize(QSize(20, 20))

        # connect buttons
        self.bestAspectButton.clicked.connect(self.fit_full_source)
        self.clearButton.clicked.connect(lambda: self.view_browser.clear())
        self.newButton.clicked.connect(lambda: self.create_view())

        # hide buttons
        self.newButton.hide()
        self.clearButton.hide()
        # self.bestAspectButton.hide()

        self.autofitControl.stateChanged.connect(self.set_autofit)

        self.histogramControl.stateChanged.connect(lambda status: self.view_browser.set_histogram(status))
        self.toolBarControl.stateChanged.connect(self.set_toolbar)
        self.layoutCombo.currentTextChanged.connect(self.on_layout_change)

        overview = self.overview

        full_overview = self

        def update_infos(ev):
            full_overview.update_infos()

        overview.window.on_change.pipe(
            ops.debounce(.2)
        ).subscribe(
            on_next=update_infos
        )

    def update_infos(self):
        source = self.overview.source
        if source is None:
            return
        infos = source.infos()
        h, w, b = infos.shape
        dtype = infos.dtype
        self.sourceLabel.setText(f'{infos.name} {w}x{h}:{b} {dtype}')

        area = self.overview.window.roi
        x, y = area.pos.raw()
        aw, ah = area.size.raw()

        buffer = source.read(Window(window=area))
        import numpy as np
        self.distributionLabel.setText(
            f'min: {buffer.min()} max: {buffer.max()}\n'
            f'mean: {np.mean(buffer):.2f} std: {np.std(buffer):.2f}'
        )

        # FIXME: update QSpinBox values
        # self.transformPanel.xSpinBox.setValue(int(x))
        # self.transformPanel.ySpinBox.setValue(int(y))
        # self.transformPanel.wSpinBox.setValue(aw)
        # self.transformPanel.hSpinBox.setValue(ah)

        self.windowLabel.setText(f'window: {x},{y} {aw}x{ah}')

    def fit_full_source(self):
        self.overview.window.roi = RectAbs(
            pos=PointAbs(0, 0),
            size=self.overview.source.infos().size
        )
        self.overview.update_roi()

    def optimize_aspect(self):
        browser = self.view_browser
        w = browser.config.item_per_line
        h = int(browser.config.item_per_page / w)
        table_aspect = w / h

        self.overview.optimize_aspect(table_aspect)

    def set_autofit(self, status: bool):
        if status:
            self.optimize_aspect()

    def set_toolbar(self, status: bool):
        browser = self.view_browser
        browser.set_toolbar(status)
        browser.config.tool_bar = status
        browser.request_update()

    @property
    def autofit(self):
        autofit: QCheckBox = self.autofitControl
        return autofit.isChecked()

    def create_view(self):
        view = self.view_browser.create_view()
        view.subscribe(self.overview)
        return view

    def closeEvent(self, ev) -> None:
        self.view_browser.clear()
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

        browser = self.view_browser
        browser.config.tool_bar = config.tool_bar
        browser.config.item_per_line = config.item_per_line
        browser.config.item_per_page = config.item_per_page
        if self.autofit:
            self.optimize_aspect()
        browser.request_update()

    @property
    def view_browser(self) -> ViewBrowser:
        return self.viewBrowser

    @property
    def overview(self) -> Overview:
        return self.view

    @property
    def tool_bar_control(self) -> QCheckBox:
        return self.toolBarControl
