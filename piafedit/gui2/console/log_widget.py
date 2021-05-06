import logging

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QVBoxLayout


class LogSignal(QObject):
    log = pyqtSignal(str)


class LogWidget(QWidget):
    def __init__(self, name: str, parent=None):
        super().__init__(parent)
        self.signals = LogSignal()
        self.signals.log.connect(self.add_line)

        self.name = name
        self.text_box = QPlainTextEdit(self)
        self.text_box.setReadOnly(True)

        # set up layout
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.text_box)
        self.setLayout(layout)

    def follow(self, logger: logging.Logger):
        logger.addHandler(QtHandler(self.signals))

    def clear(self):
        self.text_box.clear()

    def add_line(self, log_text: str):
        self.text_box.appendPlainText(log_text)
        self.text_box.centerCursor()


class QtHandler(logging.Handler):
    def __init__(self, signal: LogSignal):
        super().__init__()
        self.signal = signal
        self.setFormatter(logging.Formatter('%(asctime)s %(name)s %(levelname)s - %(message)s'))
        self.setLevel(logging.DEBUG)

    def emit(self, record):
        msg = self.format(record)
        self.signal.log.emit(msg)
