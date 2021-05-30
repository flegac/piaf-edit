from piafedit.gui.common.template_widget import TemplateWidget
from piafedit.gui.image.views.overview import Overview
from piafedit.gui.image.views.roi_view import RoiView
from piafedit.gui.tools.view_config_panel import ViewConfigPanel


class FullRoiView(TemplateWidget):
    def __init__(self, parent=None):
        super().__init__('roi_view', parent)
        self.view.changed_subject.subscribe(on_next=self.on_view_change)
        self.configureButton.clicked.connect(self.show_config)
        self.panel: ViewConfigPanel = None

    def on_view_change(self, view: RoiView):
        self.nameLabel.setText(view.view_name())

    def show_config(self):
        self.panel = ViewConfigPanel()
        self.panel.set_view(self.view)
        self.panel.show()

    def set_toolbar(self, status: bool):
        if status:
            self.toolBar.show()
        else:
            self.toolBar.hide()

    def subscribe(self, overview: Overview):
        self.view.subscribe(overview)
