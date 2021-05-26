import logging

from piafedit.gui.common.drop import Drop
from piafedit.gui.common.handler.drag_handler import DragHandler
from piafedit.gui.common.utils import open_sources

log = logging.getLogger()


class SourceBrowserDragHandler(DragHandler):
    def __init__(self):
        self.acceptDrops = True

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        from piafedit.editor_api import P
        paths = Drop.read_urls(e.mimeData())
        sources = open_sources(paths)
        P.open_sources(sources)
