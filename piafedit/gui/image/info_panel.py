from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

from piafedit.gui.image.image_manager import ImageManager


class InfoPanel(QWidget):
    def __init__(self, manager: ImageManager):
        super().__init__()
        self.manager = manager

        self.view_infos = QLabel()
        self.overview_infos = QLabel()
        self.area_infos = QLabel()

        l = QVBoxLayout()
        l.addWidget(self.view_infos)
        l.addWidget(self.overview_infos)
        l.addWidget(self.area_infos)
        self.setLayout(l)

    def update_manager(self):
        manager = self.manager
        source = manager.source
        h, w, b = source.shape()
        dtype = source.dtype()
        self.view_infos.setText(f'view: {source.name} {w}x{h}:{b} {dtype}')

        buffer = manager.overview.image
        h, w, b = buffer.shape
        dtype = buffer.dtype
        self.overview_infos.setText(f'overview: {w}x{h}:{b} {dtype}')

        area = manager.rect
        x, y = area.pos.raw()
        w, h = area.size.raw()

        self.area_infos.setText(f'area: {x},{y} {w}x{h}')