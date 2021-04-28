import numpy as np
import pyqtgraph as pg

from piafedit.gui.browser.image_drag_handler import ImageDragHandler
from piafedit.gui.image.handler.roi_keyboard import RoiKeyboardHandler
from piafedit.gui.image.handler.roi_mouse import RoiMouseHandler
from piafedit.model.geometry.size import SizeAbs


class RoiView(pg.ImageView):
    def __init__(self, manager: 'ImageManager'):
        super().__init__()
        self.manager = manager
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
        self.current_buffer_shape = None

        # events handlers
        self.setup_resize_event()
        RoiKeyboardHandler(manager).patch(self.ui.graphicsView)
        # Ui.actions.handler().patch(self.ui.graphicsView)
        RoiMouseHandler(manager).patch(self.ui.graphicsView)
        ImageDragHandler().patch(self.ui.graphicsView)

    def size(self):
        view = self.view
        w = view.width()
        h = view.height()
        return SizeAbs(w, h)

    def set_buffer(self, buffer: np.ndarray):
        self.setImage(buffer)
        self.view.autoRange(padding=0.0)
        self.current_buffer_shape = buffer.shape

    def setup_resize_event(self):
        manager = self.manager
        old_resizeEvent = self.ui.graphicsView.resizeEvent

        def resizeEvent(ev):
            old_resizeEvent(ev)
            manager.update_view()

        self.ui.graphicsView.resizeEvent = resizeEvent
