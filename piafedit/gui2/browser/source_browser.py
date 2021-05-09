from piafedit.gui2.browser.image_drag_handler import ImageDragHandler
from piafedit.gui.common.utils import source_button
from qtwidgets.flow.flow_config import FlowConfig
from qtwidgets.flow.flow_widget import FlowWidget


class SourceBrowser(FlowWidget):
    def __init__(self, config: FlowConfig):
        super().__init__(
            config=config,
            builder=lambda x: source_button(x, config.item.width)
        )
        ImageDragHandler().patch(self)
