from PyQt5 import uic
from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QWidget, QProgressBar

from piafedit.gui2.console.log_widget import LogWidget
from piafedit.gui2.tasks.worker import Worker


class ProcessWidget(QWidget):
    def __init__(self, pool: QThreadPool, worker: Worker):
        super(ProcessWidget, self).__init__()
        from piafedit.editor_api import P
        uic.loadUi(P.resources() / 'ui/process.ui', self)
        self.show()
        self.pool = pool
        self.worker = worker

        logs = LogWidget('worker')
        logs.follow(worker.logger)
        self.layout().replaceWidget(self.logs, logs)

        self.runButton.clicked.connect(self.run_task)

    def stop(self):
        # stop task ?
        self.close()

    def run_task(self):
        worker = self.worker
        worker.signal.status.connect(lambda status: self.status.setText(f'Status: {status}'))

        progress_bar: QProgressBar = self.progress
        worker.signal.progress.connect(
            lambda progress: progress_bar.setValue(int(100 * progress.done / progress.total)))
        worker.signal.error.connect(lambda e: self.error.setText(f'error: {e}'))
        worker.signal.result.connect(lambda e: self.result.setText(f'result: {e}'))
        self.pool.start(worker)
