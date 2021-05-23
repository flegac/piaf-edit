import logging
from typing import Optional

import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QSizePolicy
from rx.subject import Subject

from piafedit.gui.image.source_view_drag_handler import SourceViewDragHandler
from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import RectAbs
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.libs.operator import Operator
from piafedit.model.source.data_source import DataSource
from piafedit.model.source.window import Window

log = logging.getLogger(__name__)


class SourceView(pg.ImageView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.source_change = Subject()

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
        self.ui.graphicsView.setBackground(None)
        self._source: Optional[DataSource] = None
        self.op: Optional[Operator] = None
        SourceViewDragHandler(self).patch(self)

    @property
    def source(self):
        return self._source

    def set_source(self, source: DataSource):
        self._source = source
        self.source_change.on_next(self)

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
        self.update_view()

    def update_view(self, size: SizeAbs = None):
        if self.source is None:
            return

        if size is None or self.width() < size.width:
            size = SizeAbs(self.width(), self.height())

        win_size = self.source.infos().size
        if hasattr(self, 'overview') and self.overview is not None:
            win = self.overview.rect.limit(win_size)
        else:
            win = RectAbs(PointAbs(0, 0), win_size)
        window = Window(
            window=win
        )
        window.set_max_size(max(size.width, size.height))

        buffer = self.source.read(window)
        self.set_buffer(buffer)
