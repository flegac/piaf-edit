import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QSizePolicy


class BufferView(pg.ImageView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
        self.ui.histogram.hide()
        self.ui.graphicsView.setBackground(None)

    def set_histogram(self, status: bool):
        if status:
            self.ui.histogram.show()
        else:
            self.ui.histogram.hide()

    def switch_histogram(self):
        self.set_histogram(self.ui.histogram.isHidden())

    def set_buffer(self, buffer: np.ndarray):
        self.setImage(buffer)
        self.view.autoRange(padding=0.0)
