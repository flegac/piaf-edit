import logging
from pathlib import Path

from piafedit.gui.common.handler.drag_handler import DragHandler
from piafedit.gui.utils import open_sources

log = logging.getLogger()


class SourceViewDragHandler(DragHandler):
    def __init__(self, view: 'SourceView'):
        from piafedit.gui.image.bases.source_view import SourceView
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

        path = paths[0]
        from piafedit.editor_api import P
        if path.suffix == '.stylesheet':
            P.load_style(path)
        else:
            P.load_style(None)

        sources = open_sources(paths)
        try:
            self.view.set_source(sources[0])
            # TODO: remove this line ?
            self.view.update_view()
        except:
            log.warning(f'could not load source: {paths}')
