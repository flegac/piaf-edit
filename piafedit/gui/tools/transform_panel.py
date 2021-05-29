from piafedit.gui.common.template_widget import TemplateWidget
from piafedit.model.transform import Transform


class TransformPanel(TemplateWidget):
    def __init__(self, parent=None):
        super().__init__('transform', parent)
        self.transform: Transform = Transform()

        self.xSpinBox.valueChanged.connect(self.on_x_change)
        self.ySpinBox.valueChanged.connect(self.on_y_change)
        self.wSpinBox.valueChanged.connect(self.on_zoom_x_change)
        self.hSpinBox.valueChanged.connect(self.on_zoom_y_change)
        self.resamplingCombo.currentTextChanged.connect(self.on_resampling_change)
        self.fitButton.clicked.connect(self.fit)

    def set_transform(self, transform: Transform):
        self.transform = transform
        self.xSpinBox.setValue(transform.offset.x)
        self.ySpinBox.setValue(transform.offset.y)
        self.wSpinBox.setValue(transform.zoom.width * 100)
        self.hSpinBox.setValue(transform.zoom.height * 100)
        self.request_update()

    def on_x_change(self, value: int):
        self.transform.offset.x = value
        self.request_update()

    def on_y_change(self, value: int):
        self.transform.offset.y = value
        self.request_update()

    def on_zoom_x_change(self, value: float):
        self.transform.zoom.width = value / 100
        self.request_update()

    def on_zoom_y_change(self, value: float):
        self.transform.zoom.height = value / 100
        self.request_update()

    def on_resampling_change(self, name: str):
        from rasterio.enums import Resampling
        cases = {
            'nearest': Resampling.nearest,
            'bilinear': Resampling.bilinear,
            'cubic': Resampling.cubic
        }
        self.transform.resampling = cases[name]
        self.request_update()

    def fit(self):
        self.transform.offset.x = 0
        self.transform.offset.y = 0
        self.transform.zoom.width = 1.0
        self.transform.zoom.height = 1.0
        self.set_transform(self.transform)
