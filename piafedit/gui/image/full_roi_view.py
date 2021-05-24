from PyQt5.QtWidgets import QWidget

from piafedit.gui.image.overview import Overview
from piafedit.model.libs.filters import edge_detection, erode, dilate
from piafedit.ui_utils import load_ui


class FullRoiView(QWidget):
    def __init__(self):
        super().__init__()
        load_ui('roi_view', self)

        self.view.changed_subject.subscribe(on_next=lambda view: self.infos.setText(view.view_name()))
        self.operatorCombo.currentTextChanged.connect(self.on_op_change)

    def subscribe(self, overview: Overview):
        self.view.subscribe(overview)

    def on_op_change(self, name: str):
        op = None
        if name == 'Identity':
            op = None
        if name == 'Edge':
            op = edge_detection
        elif name == 'Erode':
            op = erode
        elif name == 'Dilate':
            op = dilate

        self.view.set_operator(op)
