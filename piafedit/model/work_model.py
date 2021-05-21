from pathlib import Path
from typing import List

from PyQt5.QtWidgets import QFileSystemModel

from piafedit.model.worker_creator import create_worker
from piafedit.model.source.data_source import DataSource
from qtwidgets.observablelist import observablelist


class WorkModel:
    def __init__(self, path: Path):
        self.path = path
        self.sources: List[DataSource] = observablelist([])
        self.source_index: int = None

        self.workers = observablelist([create_worker() for i in range(10)])
        self._tree_model: QFileSystemModel = None

    @property
    def tree_model(self):
        if not self._tree_model:
            self._tree_model = QFileSystemModel()
            self._tree_model.setRootPath(str(self.path))
        return self._tree_model
