from typing import List

from piafedit.gui.image.bases.source_view import SourceView
from qtwidgets.browser.browser_widget import BrowserWidget
from qtwidgets.observablelist import observablelist


class ViewBrowser(BrowserWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.histogram_status = False
        self.toolbar_status = False
        # FIXME: remove this field (= super().widgets)
        self.views: List[SourceView] = observablelist()

    def create_view(self):
        from piafedit.gui.image.full_roi_view import FullRoiView
        view = FullRoiView()
        view.view.set_histogram(self.histogram_status)
        view.set_toolbar(self.toolbar_status)
        self.views.append(view)
        return view

    def detach(self, view: SourceView):
        self.views.remove(view)

    def clear(self):
        for view in self.views:
            view.close()

    def set_toolbar(self, status: bool):
        self.toolbar_status = status
        for view in self.views:
            view.set_toolbar(status)

    def set_histogram(self, status: bool):
        self.histogram_status = status
        for view in self.views:
            view.view.set_histogram(status)

    def switch_histogram(self):
        self.set_histogram(not self.histogram_status)

    def switch_config(self):
        self.set_toolbar(not self.toolbar_status)
