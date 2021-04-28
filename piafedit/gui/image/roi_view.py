import pyqtgraph as pg

from piafedit.gui.browser.image_drag_handler import ImageDragHandler
from piafedit.gui.image.handler.roi_keyboard import RoiKeyboardHandler
from piafedit.gui.image.handler.roi_mouse import RoiMouseHandler


class RoiView(pg.ImageView):
    def __init__(self, manager: 'ImageManager'):
        super().__init__()
        self.manager = manager
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()

        old_resizeEvent = self.ui.graphicsView.resizeEvent

        def resizeEvent(ev):
            old_resizeEvent(ev)
            manager.update_view()

        self.ui.graphicsView.resizeEvent = resizeEvent

        RoiKeyboardHandler(manager).patch(self.ui.graphicsView)
        # Ui.actions.handler().patch(self.ui.graphicsView)

        RoiMouseHandler(manager).patch(self.ui.graphicsView)
        ImageDragHandler().patch(self.ui.graphicsView)

        manager.overview.the_roi.sigRegionChanged.connect(self.update_rect)

    def update_rect(self):
        rx, ry = self.manager.compute_roi_rect_ratio()
        rect = self.manager.overview.rect
        roi = self.manager.overview.the_roi

        rect.pos.x = round(roi.pos().x() * rx)
        rect.pos.y = round(roi.pos().y() * ry)
        rect.size.width = round(roi.size().x() * rx)
        rect.size.height = round(roi.size().y() * ry)
        self.manager.update_view()
