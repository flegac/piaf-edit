import numpy as np
from PyQt5.QtWidgets import QComboBox, QListWidget

from piafedit.gui.common.template_widget import TemplateWidget
from piafedit.model.libs.filters import erode, dilate, edge_detection
from piafedit.ui_utils import gui_app

operators = {
    'erode': erode,
    'dilate': dilate,
    'edge': edge_detection,
}


class PipelinePanel(TemplateWidget):
    def __init__(self, parent=None):
        super().__init__('pipeline', parent)
        self.operator_combo.addItems(operators.keys())
        self.insertButton.clicked.connect(self.insert_operator)
        self.removeButton.clicked.connect(self.remove_selected)
        self.show()

    def pipeline(self):
        keys = [self.pipeline_list.item(i).text() for i in range(self.pipeline_list.count())]
        ops = [
            operators[key]
            for key in keys
        ]

        def pipe(buffer: np.ndarray):
            for op in ops:
                buffer = op(buffer)
            return buffer

        return pipe

    def insert_operator(self):
        op = self.operator_combo.currentData()
        text = self.operator_combo.currentText()
        index = 0
        for item in self.pipeline_list.selectedItems():
            index = self.pipeline_list.row(item)
        self.pipeline_list.insertItem(index, text)
        self.request_update()

    def remove_selected(self):
        for item in self.pipeline_list.selectedItems():
            self.pipeline_list.takeItem(self.pipeline_list.row(item))
        self.request_update()

    @property
    def pipeline_list(self) -> QListWidget:
        return self.pipelineList

    @property
    def operator_combo(self) -> QComboBox:
        return self.operatorCombo


if __name__ == '__main__':
    with gui_app():
        pipe = PipelinePanel()
        pipe.show()
