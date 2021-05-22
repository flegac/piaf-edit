from typing import List

from piafedit.gui.image.source_view import SourceView
from piafedit.model.libs.operator import Operator


class ViewManager:
    def __init__(self):
        self.histogram_status = False
        self.views: List[SourceView] = []

    def create_view(self, op: Operator = None):
        from piafedit.gui.image.roi_view import RoiView
        view = RoiView()
        view.set_histogram(self.histogram_status)
        view.set_operator(op)
        self.views.append(view)
        return view

    def detach(self, view: SourceView):
        self.views.remove(view)

    def clear(self):
        for view in self.views:
            view.close()

    def switch_histogram(self):
        self.histogram_status = not self.histogram_status
        self.set_histogram(self.histogram_status)

    def set_histogram(self, status: bool):
        self.histogram_status = status
        for view in self.views:
            view.widget().set_histogram(status)
