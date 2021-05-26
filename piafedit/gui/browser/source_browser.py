from piafedit.gui.browser.source_browser_drag_handler import SourceBrowserDragHandler
from piafedit.gui.browser.source_button import SourceButton
from qtwidgets.browser.browser_config import BrowserConfig
from qtwidgets.browser.browser_widget import BrowserWidget


class SourceBrowser(BrowserWidget):
    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            builder=SourceButton,
            config=BrowserConfig(
                item_per_line=5,
                item_per_page=20
            ))
        SourceBrowserDragHandler().patch(self)
