from qtconsole.manager import QtKernelManager
from qtconsole.rich_jupyter_widget import RichJupyterWidget


class MyNotebook(RichJupyterWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        kernel_manager = QtKernelManager(kernel_name='python3')
        kernel_manager.start_kernel()
        kernel_client = kernel_manager.client()
        kernel_client.start_channels()

        self.kernel_manager = kernel_manager
        self.kernel_client = kernel_client

    def closeEvent(self, ev):
        print('Shutting down kernel...')
        self.kernel_client.stop_channels()
        self.kernel_manager.shutdown_kernel()
        super().closeEvent(ev)