from PyQt5.QtWidgets import QWidget, QVBoxLayout

from piafedit.extension.test_sequences import KeySequenceEdit


class ToolBar(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        layout.addWidget(KeySequenceEdit())
