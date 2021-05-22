import logging
from typing import Optional

import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QSizePolicy

from piafedit.gui.image.source_view_drag_handler import SourceViewDragHandler
from piafedit.model.geometry.size import SizeAbs, Size
from piafedit.model.libs.operator import Operator
from piafedit.model.source.data_source import DataSource

log = logging.getLogger(__name__)


class SourceView(pg.ImageView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
        self.ui.graphicsView.setBackground(None)
        self.source: Optional[DataSource] = None
        self.op: Optional[Operator] = None
        SourceViewDragHandler(self).patch(self)

    def set_histogram(self, status: bool):
        if status:
            self.ui.histogram.show()
        else:
            self.ui.histogram.hide()

    def switch_histogram(self):
        self.set_histogram(self.ui.histogram.isHidden())

    def set_buffer(self, buffer: np.ndarray):
        if self.op:
            buffer = self.op(buffer)
        self.setImage(buffer)
        self.view.autoRange(padding=0.0)

    def set_operator(self, op: Operator):
        self.op = op

    def update_view(self, size: SizeAbs = None):
        if size is None or self.width() < size.width:
            size = SizeAbs(self.width(), self.height())

        source = self.source
        window = self.overview.rect.limit(source.infos().size)
        aspect = window.size.aspect_ratio

        s = max(size.width, size.height)
        abs_size = SizeAbs(s, s)
        size = Size.from_aspect(aspect).abs(abs_size)

        buffer = source.read(window, output_size=size)
        self.set_buffer(buffer)
