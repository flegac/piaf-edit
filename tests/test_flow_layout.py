from PyQt5.QtWidgets import QApplication

from piafedit.gui.common.flow_layout import FlowLayout
from piafedit.gui.common.utils import image_button
import numpy as np

if __name__ == '__main__':
    app = QApplication([])
    flow = FlowLayout()
    for _ in range(20):
        w, h = 128, 96
        shape = (h, w, 3)
        buffer = np.random.randint(0, 255, size=shape).astype('uint8')

        flow.register(image_button(buffer))
    flow.update_layout()
    flow.show()

    app.exec_()
