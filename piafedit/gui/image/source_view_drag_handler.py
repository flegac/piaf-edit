import logging
from pathlib import Path

from piafedit.gui.common.handler.drag_handler import DragHandler
from piafedit.gui.utils import open_sources

log = logging.getLogger()


class SourceViewDragHandler(DragHandler):
    def __init__(self, view: 'SourceView'):
        from piafedit.gui.image.source_view import SourceView
        self.acceptDrops = True
        self.view: SourceView = view

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        urls = e.mimeData().urls()
        local_files = [url.toLocalFile() for url in urls]
        paths = list(map(Path, local_files))
        if len(paths) != 1:
            log.warning(f'Only one source per View is allowed ({len(paths)} files selected)')
            return
        sources = open_sources(paths)
        self.view.source = sources[0]
        self.view.update_view()
