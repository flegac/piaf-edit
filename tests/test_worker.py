import random
import sys
import time

from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QApplication

from piafedit.gui2.tasks.worker import Worker, Task


def create_worker():
    def task(i: int) -> Task:
        if i % 4 == 1:
            def work():
                time.sleep(random.randint(500, 1000) / 1000)
                raise ValueError(i)

            return work

        def work():
            time.sleep(random.randint(500, 1000) / 1000)
            res = f'work-{i}'
            return res

        return work

    tasks = [task(i) for i in range(10)]
    return Worker(*tasks)


class WorkerWidget(QWidget):
    def __init__(self, pool: QThreadPool, worker: Worker):
        super().__init__()
        self.pool = pool
        self.worker = worker

        self.status = QLabel('status')
        self.progress = QLabel('progress')
        self.result = QLabel('result')
        self.error = QLabel('error')
        button = QPushButton("Run")
        button.clicked.connect(self.runTask)

        layout = QVBoxLayout()
        layout.addWidget(self.status)
        layout.addWidget(self.progress)
        layout.addWidget(self.result)
        layout.addWidget(self.error)
        layout.addWidget(button)

        self.setLayout(layout)

    def runTask(self):
        worker = self.worker
        worker.signal.status.connect(lambda status: self.status.setText(f'Status: {status}'))
        worker.signal.progress.connect(
            lambda progress: self.progress.setText(f'progress: {progress.done}/{progress.total}'))
        worker.signal.error.connect(lambda e: self.error.setText(f'error: {e}'))
        worker.signal.result.connect(lambda e: self.result.setText(f'result: {e}'))
        self.pool.start(worker)


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pool = QThreadPool()

        worker = WorkerWidget(self.pool, create_worker())

        self.setCentralWidget(worker)


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
