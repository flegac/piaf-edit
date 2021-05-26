import logging
from pathlib import Path

from PyQt5.QtWidgets import QTreeView, QFileSystemModel

from piafedit.editor_api import P
from piafedit.model.source.rio_data_source import RIODataSource

log = logging.getLogger()


class FileBrowser(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)

    def setup_model(self, model: QFileSystemModel):
        self.setModel(model)
        self.selectionModel().selectionChanged.connect(self.on_select)
        self.doubleClicked.connect(self.on_click)
        self.setRootIndex(model.index(model.rootPath()))

    def on_select(self, ev):
        paths = set(
            Path(self.model().filePath(idx))
            for idx in ev.indexes()
        )
        sources = []
        for path in paths:
            try:
                sources.append(RIODataSource(path))
            except:
                log.warning(f'could not open source: {path}')
        P.open_sources(sources)

    def on_click(self, ev):
        pass
