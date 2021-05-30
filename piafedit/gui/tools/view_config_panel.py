from piafedit.gui.common.template_widget import TemplateWidget
from piafedit.gui.image.views.source_view import SourceView
from piafedit.gui.tools.pipeline_panel import PipelinePanel
from piafedit.gui.tools.transform_panel import TransformPanel


class ViewConfigPanel(TemplateWidget):
    def __init__(self, parent=None):
        super().__init__('view_config', parent)
        self.view: SourceView = None

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.transform_panel.on_change.subscribe(lambda ev: self.view.request_update())
        self.pipeline_panel.on_change.subscribe(lambda ev: self.view.set_operator(self.pipeline_panel.pipeline()))

    def set_view(self, view: SourceView):
        self.view = view
        self.transform_panel.set_transform(view.transform)
        self.nameLabel.setText(view.view_name())

    def accept(self):
        print('accept')
        self.hide()

    def reject(self):
        print('reject')
        self.hide()

    @property
    def transform_panel(self) -> TransformPanel:
        return self.transformPanel

    @property
    def pipeline_panel(self) -> PipelinePanel:
        return self.pipelinePanel
