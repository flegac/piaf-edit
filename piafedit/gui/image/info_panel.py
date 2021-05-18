from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

from piafedit.gui.image.overview import Overview


class InfoPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.view_infos = QLabel()
        self.overview_infos = QLabel()
        self.area_infos = QLabel()

        l = QVBoxLayout()
        l.addWidget(self.view_infos)
        l.addWidget(self.overview_infos)
        l.addWidget(self.area_infos)
        self.setLayout(l)

    def update_overview(self, overview: Overview):
        source = overview.source
        infos = source.infos()
        h, w, b = infos.shape
        dtype = infos.dtype
        self.view_infos.setText(f'view: {infos.name} {w}x{h}:{b} {dtype}')

        buffer = overview.image
        h, w, b = buffer.shape
        dtype = buffer.dtype
        self.overview_infos.setText(f'overview: {w}x{h}:{b} {dtype}')

        area = overview.rect
        x, y = area.pos.raw()
        w, h = area.size.raw()

        self.area_infos.setText(f'area: {x},{y} {w}x{h}')
