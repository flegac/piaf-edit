from PyQt5.QtWidgets import QWidget

from piafedit.gui.image.overview import Overview
from piafedit.model.libs.filters import edge_detection, erode, dilate
from piafedit.ui_utils import load_ui


class FullRoiView(QWidget):
    def __init__(self):
        super().__init__()
        load_ui('roi_view', self)

        self.view.changed_subject.subscribe(on_next=lambda view: self.infos.setText(view.view_name()))
        self.operator.currentTextChanged.connect(self.on_op_change)
        self.resampling.currentTextChanged.connect(self.on_resampling_change)

    def set_toolbar(self, status: bool):
        if status:
            self.toolBar.show()
        else:
            self.toolBar.hide()

    def subscribe(self, overview: Overview):
        self.view.subscribe(overview)

    def on_op_change(self, name: str):
        op = None
        if name == 'Identity':
            op = None
        if name == 'Edge':
            op = edge_detection
        elif name == 'Erode':
            op = erode
        elif name == 'Dilate':
            op = dilate

        self.view.set_operator(op)

    def on_resampling_change(self, name: str):
        from rasterio.enums import Resampling
        cases = {
            'nearest': Resampling.nearest,
            'bilinear': Resampling.bilinear,
            'cubic': Resampling.cubic
        }

        self.view.set_resampling(cases[name])
