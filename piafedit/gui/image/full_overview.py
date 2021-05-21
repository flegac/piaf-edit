from PyQt5.QtWidgets import QWidget

from piafedit.ui_utils import load_ui


class FullOverview(QWidget):
    def __init__(self):
        super().__init__()
        load_ui('overview', self)
