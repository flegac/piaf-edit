from PyQt5.QtWidgets import QWidget

from piafedit.gui.image.overview import Overview
from piafedit.model.source.window import Window
from piafedit.ui_utils import load_ui


class InfoPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        load_ui('infos', self)

    def update_overview(self, overview: Overview):
        source = overview.source
        if source is None:
            return
        infos = source.infos()
        h, w, b = infos.shape
        dtype = infos.dtype
        self.sourceLabel.setText(f'{infos.name} {w}x{h}:{b} {dtype}')

        area = overview.window.roi
        x, y = area.pos.raw()
        w, h = area.size.raw()

        buffer = source.read_at(Window(window=area))
        import numpy as np
        self.distributionLabel.setText(
            f'min: {buffer.min()} max: {buffer.max()}\n'
            f'mean: {np.mean(buffer):.2f} std: {np.std(buffer):.2f}'
        )

        self.windowLabel.setText(f'window: {x},{y} {w}x{h}')
