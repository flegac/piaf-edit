import logging
from typing import Optional

from rx.subject import Subject

from piafedit.gui.image.bases.buffer_view import BufferView
from piafedit.gui.image.bases.source_view_drag_handler import SourceViewDragHandler
from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import RectAbs
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.libs.operator import Operator
from piafedit.model.source.data_source import DataSource
from piafedit.model.source.window import Window

log = logging.getLogger(__name__)


class SourceView(BufferView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._source: Optional[DataSource] = None
        self.op: Optional[Operator] = None
        SourceViewDragHandler(self).patch(self)

        self.changed_subject = Subject()
        self.changed_subject.subscribe(lambda _: self.update_view())

    @property
    def source(self):
        return self._source

    def set_source(self, source: DataSource):
        self._source = source
        self.changed_subject.on_next(self)

    def set_operator(self, op: Operator):
        self.op = op
        self.changed_subject.on_next(self)

    def update_view(self, size: SizeAbs = None):
        if self.source is None:
            return

        if size is None or self.width() < size.width:
            size = SizeAbs(self.width(), self.height())

        win_size = self.source.infos().size
        if hasattr(self, 'overview') and self.overview is not None:
            # FIXME: remove overview dependency
            win = self.overview.window.roi.limit(win_size)
        else:
            win = RectAbs(PointAbs(0, 0), win_size)
        window = Window(
            window=win
        )
        window.set_max_size(max(size.width, size.height))

        buffer = self.source.read(window)
        if self.op:
            buffer = self.op(buffer)
        self.set_buffer(buffer)
