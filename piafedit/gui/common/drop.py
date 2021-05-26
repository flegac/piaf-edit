from pathlib import Path
from typing import Callable

from PyQt5.QtCore import QMimeData, QUrl
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import QWidget


class Drop:
    @staticmethod
    def patch(widget: QWidget, accept: Callable[[QMimeData], bool], handle: Callable[[QWidget, QMimeData], None]):
        widget.setAcceptDrops(True)

        def dragEnterEvent(event: QDragEnterEvent):
            if accept(event.mimeData()):
                event.acceptProposedAction()

        def dropEvent(event: QDropEvent):
            if accept(event.mimeData()):
                handle(widget, event.mimeData())

        widget.dragEnterEvent = dragEnterEvent
        widget.dropEvent = dropEvent

    @staticmethod
    def read_urls(mime_data: QMimeData):
        paths = []
        for url in mime_data.urls():
            url: QUrl = url
            if url.isLocalFile():
                path = url.toLocalFile()
            else:
                path = url.path()
            paths.append(Path(path))
        return paths
