import logging
from pathlib import Path
from typing import Optional

from PyQt5.QtCore import QMimeData
from PyQt5.QtWidgets import QWidget
from rasterio.enums import Resampling
from rx.subject import Subject

from piafedit.gui.common.drop import Drop
from piafedit.gui.common.utils import open_sources
from piafedit.gui.image.bases.buffer_view import BufferView
from piafedit.model.transform import Transform
from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import RectAbs
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.libs.operator import Operator
from piafedit.model.source.data_source import DataSource
from piafedit.model.source.window import Window

log = logging.getLogger(__name__)


def style_handler(path: Path):
    from piafedit.editor_api import P
    if path.suffix == '.stylesheet':
        P.load_style(path)
    else:
        P.load_style(None)


class SourceView(BufferView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._source: Optional[DataSource] = None
        self.operator: Optional[Operator] = None
        self.transform: Transform = Transform()
        self.resampling: Optional[Resampling] = None

        self.changed_subject = Subject()
        self.changed_subject.subscribe(lambda _: self.update_view())

        Drop.patch(self, lambda x: x.hasUrls(), SourceView.handle_drop())

    @staticmethod
    def handle_drop():
        def handle(widget: QWidget, mime_data: QMimeData):
            paths = Drop.read_urls(mime_data)
            if len(paths) != 1:
                log.warning(f'Only one source per View is allowed ({len(paths)} files selected)')
                return

            sources = open_sources(paths)
            try:
                widget.set_source(sources[0])
            except:
                log.warning(f'could not load source: {paths}')

        return handle

    @property
    def source(self):
        return self._source

    def request_update(self):
        self.changed_subject.on_next(self)

    def set_source(self, source: DataSource):
        self._source = source
        self.request_update()

    def set_operator(self, op: Operator):
        self.operator = op
        self.request_update()

    def set_resampling(self, resampling: Resampling):
        self.resampling = resampling
        self.request_update()

    def update_view(self, size: SizeAbs = None):
        if self.source is None:
            return

        window: Window = self.final_window(size)

        buffer = self.source.read(window)
        if self.operator:
            buffer = self.operator(buffer)
        self.set_buffer(buffer)

    def final_window(self, size):
        if size is None or self.width() < size.width:
            size = SizeAbs(self.width(), self.height())
        win_size = self.source.infos().size
        if hasattr(self, 'overview') and self.overview is not None:
            # FIXME: remove overview dependency
            win = self.overview.window.roi.limit(win_size)
        else:
            win = RectAbs(PointAbs(0, 0), win_size)
        window = Window(
            window=win,
            resampling=self.resampling
        )
        window.window.move(*self.transform.offset.raw())

        window.window.size.width = int(window.window.size.width * self.transform.zoom.width)
        window.window.size.height = int(window.window.size.height * self.transform.zoom.height)
        window.set_max_size(max(size.width, size.height))

        return window
