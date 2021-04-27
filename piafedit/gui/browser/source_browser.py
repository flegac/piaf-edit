from PyQt5.QtWidgets import QWidget, QPushButton

from piafedit.gui.browser.image_drag_handler import ImageDragHandler
from piafedit.gui.common.Flow_widget import FlowWidget, QVBoxLayout
from piafedit.gui.common.utils import source_button


class SourceBrowser(FlowWidget):
    def __init__(self, width: int):
        super().__init__(lambda x: source_button(x, width), width)
        ImageDragHandler().patch(self)

    def update_layout(self):
        if self.is_empty():
            from piafedit.editor_api import P

            button = QPushButton('Browse or Drag&Drop some images')
            button.clicked.connect(P.open_files)

            layout = QVBoxLayout()
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(button)
            widget = QWidget()
            widget.setLayout(layout)
            self.scroll.setWidget(widget)
        else:
            super().update_layout()
