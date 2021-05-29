from PyQt5.QtWidgets import QWidget

from piafedit.gui.image.overview import Overview
from piafedit.gui.image.roi_view import RoiView
from piafedit.gui.image.view_config_panel import ViewConfigPanel
from piafedit.ui_utils import load_ui


class FullRoiView(QWidget):
    def __init__(self):
        super().__init__()
        load_ui('roi_view', self)
        self.view.changed_subject.subscribe(on_next=self.on_change)
        self.configureButton.clicked.connect(self.show_config)

        self.panel: ViewConfigPanel = None

    def on_change(self, view: RoiView):
        self.nameLabel.setText(view.view_name())

    def show_config(self):
        self.panel = ViewConfigPanel(self.view)
        self.panel.show()

    def set_toolbar(self, status: bool):
        if status:
            self.toolBar.show()
        else:
            self.toolBar.hide()

    def subscribe(self, overview: Overview):
        self.view.subscribe(overview)
