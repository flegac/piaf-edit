from PyQt5.QtWidgets import QDialog

from piafedit.gui.image.bases.source_view import SourceView
from piafedit.model.libs.filters import edge_detection, erode, dilate
from piafedit.ui_utils import load_ui


class ViewConfigPanel(QDialog):
    def __init__(self, view: SourceView):
        super().__init__()
        load_ui('view_config', self)
        self.view = view

        self.operator.currentTextChanged.connect(self.on_op_change)
        self.resampling.currentTextChanged.connect(self.on_resampling_change)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        infos = self.view.source.infos()

        self.xSpinBox.valueChanged.connect(self.on_x_change)
        self.ySpinBox.valueChanged.connect(self.on_y_change)
        self.wSpinBox.valueChanged.connect(self.on_zoom_x_change)
        self.hSpinBox.valueChanged.connect(self.on_zoom_y_change)

        self.xSpinBox.setValue(self.view.transform.offset.x)
        self.ySpinBox.setValue(self.view.transform.offset.y)
        self.wSpinBox.setValue(self.view.transform.zoom.width * 100)
        self.hSpinBox.setValue(self.view.transform.zoom.height * 100)

    def accept(self):
        super().accept()

    def reject(self):
        super().reject()

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

    def on_x_change(self, value: int):
        self.view.transform.offset.x = value
        self.view.request_update()

    def on_y_change(self, value: int):
        self.view.transform.offset.y = value
        self.view.request_update()

    def on_zoom_x_change(self, value: float):
        self.view.transform.zoom.width = value / 100
        self.view.request_update()

    def on_zoom_y_change(self, value: float):
        self.view.transform.zoom.height = value / 100
        self.view.request_update()
