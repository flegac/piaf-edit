from PyQt5.QtWidgets import QApplication

from piafedit.gui.common.Flow_widget import FlowWidget
from piafedit.gui.common.utils import source_button
from piafedit.model.source.raw_data_source import RawDataSource

if __name__ == '__main__':
    import numpy as np

    app = QApplication([])
    flow = FlowWidget(source_button, 250)

    for _ in range(20):
        w, h = 128, 96
        shape = (h, w, 3)
        buffer = np.random.randint(0, 255, size=shape).astype('uint8')
        source = RawDataSource(buffer)
        flow.register(source)
    flow.update_layout()
    flow.show()

    app.exec_()
