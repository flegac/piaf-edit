import logging
from dataclasses import dataclass

import pyqtgraph as pg

from piafedit.gui.common.handler.utils import Handler

log = logging.getLogger()


def dragEnterEvent(e):
    print({
        'text': e.mimeData().hasText(),
        'image': e.mimeData().hasImage(),
        'html': e.mimeData().hasHtml(),
        'urls': e.mimeData().hasUrls(),
        'color': e.mimeData().hasColor()
    })

    if e.mimeData().hasUrls():
        print('accept', e.mimeData().text())
        e.accept()
    else:
        print('ignore', e)
        e.ignore()


def dropEvent(e):
    print('....')
    print('handle', e.mimeData())


@dataclass
class DragHandler:
    # https://www.tutorialspoint.com/pyqt/pyqt_drag_and_drop.htm

    dragEnterEvent: Handler = dragEnterEvent
    dragLeaveEvent: Handler = log.debug
    dragMoveEvent: Handler = log.debug
    dropEvent: Handler = dropEvent
    acceptDrops: bool = False

    @staticmethod
    def backup(gv: pg.GraphicsView):
        if not hasattr(gv, '_drag_backup'):
            gv._backup = DragHandler(
                dragEnterEvent=gv.dragEnterEvent,
                dragLeaveEvent=gv.dragLeaveEvent,
                dragMoveEvent=gv.dragMoveEvent,
                dropEvent=gv.dropEvent,
                acceptDrops=gv.acceptDrops()
            )

    @staticmethod
    def reset(gv: pg.GraphicsView):
        if hasattr(gv, '_drag_backup'):
            gv._drag_backup.patch(gv)
            del gv._drag_backup

    def patch(self, gv: pg.GraphicsView):
        DragHandler.backup(gv)
        gv.dragEnterEvent = self.dragEnterEvent
        gv.dragLeaveEvent = self.dragLeaveEvent
        gv.dragMoveEvent = self.dragMoveEvent
        gv.dropEvent = self.dropEvent
        gv.setAcceptDrops(self.acceptDrops)