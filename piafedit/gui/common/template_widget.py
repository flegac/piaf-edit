from PyQt5.QtWidgets import QWidget
from rx.subject import Subject

from piafedit.ui_utils import load_ui


class TemplateWidget(QWidget):
    def __init__(self, template: str, parent=None):
        super().__init__(parent)
        load_ui(template, self)
        self.on_change = Subject()

    def request_update(self):
        self.on_change.on_next(self)
