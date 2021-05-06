import logging
from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Any, List

from PyQt5.QtCore import QObject, pyqtSignal, QRunnable

# https://realpython.com/python-pyqt-qthread/

Task = Callable[[logging.Logger], Any]


class WorkerStatus(Enum):
    started = auto()
    finished = auto()


@dataclass
class Progress:
    done: int
    remaining: int

    @property
    def total(self):
        return self.done + self.remaining


class WorkerSignal(QObject):
    status = pyqtSignal(WorkerStatus)
    result = pyqtSignal(object)
    error = pyqtSignal(Exception)
    progress = pyqtSignal(Progress)


class Worker(QRunnable):
    def __init__(self, *tasks: List[Task]):
        super().__init__()
        self.signal = WorkerSignal()
        self.tasks = tasks  # list(*tasks)
        self.logger = logging.getLogger(f'{self}')
        self.canceled = False

    def run(self):
        try:
            self.signal.status.emit(WorkerStatus.started)
            total = len(self.tasks)
            for i, task in enumerate(self.tasks):
                if self.canceled:
                    raise ValueError('Canceled')
                try:

                    self.signal.progress.emit(Progress(i, total - i))
                    res = task(self.logger)
                    self.signal.result.emit(res)
                except Exception as e:
                    self.signal.error.emit(e)
            self.signal.progress.emit(Progress(total, 0))

        finally:
            self.signal.status.emit(WorkerStatus.finished)

    def stop(self):
        self.canceled = True
