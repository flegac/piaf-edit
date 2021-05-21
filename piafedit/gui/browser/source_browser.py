from piafedit.editor_api import P
from piafedit.gui.browser.image_drag_handler import ImageDragHandler
from piafedit.model.source.data_source import DataSource
from qtwidgets.browser.browser_widget import BrowserWidget
from qtwidgets.gallery.image_button import ImageButton


class SourceBrowser(BrowserWidget):
    def __init__(self):
        super().__init__(builder=self.builder)
        ImageDragHandler().patch(self)

    def builder(self, source: DataSource):
        buffer = source.overview(size=256)
        button = ImageButton(buffer, name=source.infos().name)
        button.clicked.connect(lambda: P.show_source(source))
        return button
