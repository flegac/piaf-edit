from piafedit.gui2.browser.image_drag_handler import ImageDragHandler
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.source.data_source import DataSource
from qtwidgets.browser.browser_config import BrowserConfig
from qtwidgets.browser.browser_widget import BrowserWidget
from qtwidgets.gallery.image_button import ImageButton


class SourceBrowser(BrowserWidget):
    def __init__(self, config: BrowserConfig):
        super().__init__(
            config=config,
            builder=self.builder,
        )
        ImageDragHandler().patch(self)

    def builder(self, source: DataSource):
        buffer = source.read(output_size=SizeAbs(256,256))
        button = ImageButton(buffer)
        return button
