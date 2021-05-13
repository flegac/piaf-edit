from piafedit.editor_api import P
from piafedit.gui.browser.image_drag_handler import ImageDragHandler
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.source.data_source import DataSource
from qtwidgets.browser.browser_widget import BrowserWidget
from qtwidgets.gallery.image_button import ImageButton


class SourceBrowser(BrowserWidget):
    def __init__(self):
        super().__init__(builder=self.builder)
        ImageDragHandler().patch(self)

    def builder(self, source: DataSource):
        buffer = source.read(output_size=SizeAbs(256, 256))
        button = ImageButton(buffer)
        button.clicked.connect(lambda: P.show_source(source))
        return button
