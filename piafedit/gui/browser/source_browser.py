from piafedit.editor_api import P
from piafedit.gui.browser.source_browser_drag_handler import SourceBrowserDragHandler
from piafedit.model.source.data_source import DataSource
from qtwidgets.browser.browser_config import BrowserConfig
from qtwidgets.browser.browser_widget import BrowserWidget
from qtwidgets.gallery.image_button import ImageButton


class SourceBrowser(BrowserWidget):
    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            builder=self.builder,
            config=BrowserConfig(
                item_per_line=5,
                item_per_page=20
            ))
        SourceBrowserDragHandler().patch(self)

    def builder(self, source: DataSource):
        buffer = source.overview(max_size=256)
        button = ImageButton(buffer, name=source.infos().name)
        button.clicked.connect(lambda: P.show_source(source))
        return button
