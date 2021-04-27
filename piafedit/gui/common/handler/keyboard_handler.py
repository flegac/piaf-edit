import logging
from dataclasses import dataclass

from PyQt5.QtWidgets import QWidget

from piafedit.gui.common.handler.drag_handler import Handler

log = logging.getLogger()


@dataclass
class KeyboardHandler:
    keyPressEvent: Handler = log.debug

    @staticmethod
    def backup(w: QWidget):
        if not hasattr(w, '_keyboard_backup'):
            w._backup = KeyboardHandler(
                keyPressEvent=w.keyPressEvent,
            )

    @staticmethod
    def reset(w: QWidget):
        if hasattr(w, '_keyboard_backup'):
            w._backup.patch(w)
            del w._backup

    def patch(self, w: QWidget):
        KeyboardHandler.backup(w)
        w.keyPressEvent = self.keyPressEvent
