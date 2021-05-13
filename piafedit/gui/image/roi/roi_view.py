import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QSizePolicy

from piafedit.model.geometry.size import SizeAbs


class RoiView(pg.ImageView):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
        self.current_buffer_shape = None

    def size(self):
        view = self.view
        w = view.width()
        h = view.height()
        return SizeAbs(w, h)

    def set_buffer(self, buffer: np.ndarray):
        self.setImage(buffer)
        self.view.autoRange(padding=0.0)
        self.current_buffer_shape = buffer.shape
