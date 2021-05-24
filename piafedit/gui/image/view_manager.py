from typing import List

from piafedit.gui.image.bases.source_view import SourceView
from piafedit.model.libs.operator import Operator
from qtwidgets.observablelist import observablelist


class ViewManager:
    def __init__(self):
        self.histogram_status = False
        self.config_status = False
        self.views: List[SourceView] = observablelist()

    def create_view(self, op: Operator = None):
        from piafedit.gui.image.full_roi_view import FullRoiView
        view = FullRoiView()
        view.view.set_histogram(self.histogram_status)
        view.set_config(self.config_status)
        view.view.set_operator(op)
        self.views.append(view)
        return view

    def detach(self, view: SourceView):
        self.views.remove(view)

    def clear(self):
        for view in self.views:
            view.close()

    def set_config(self, status: bool):
        self.config_status = status
        for view in self.views:
            view.set_config(status)

    def set_histogram(self, status: bool):
        self.histogram_status = status
        for view in self.views:
            view.view.set_histogram(status)

    def switch_histogram(self):
        self.set_histogram(not self.histogram_status)

    def switch_config(self):
        self.set_config(not self.config_status)
