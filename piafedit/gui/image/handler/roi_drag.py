from pathlib import Path

from piafedit.gui.common.handler.drag_handler import DragHandler
from piafedit.model.source.rio_data_source import RIODataSource


class RoiDragHandler(DragHandler):
    def __init__(self):
        self.acceptDrops = True

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        from piafedit.editor_api import P
        source = None
        for url in e.mimeData().urls():
            path = url.toLocalFile()
            path = Path(path)
            source = RIODataSource(path)
            P.open_source(source)
        if source:
            P.show_source(source)
