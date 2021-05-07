from PyQt5 import uic
from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QWidget, QTabWidget

from piafedit.gui2.tasks.process_widget import ProcessWidget
from piafedit.gui2.tasks.worker import Worker


class ProcessesWidget(QWidget):
    def __init__(self):
        super(ProcessesWidget, self).__init__()
        from piafedit.editor_api import P
        uic.loadUi(P.resources() / 'ui/processes.ui', self)
        self.show()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        self.pool = QThreadPool()

    def start(self, worker: Worker):
        tabs: QTabWidget = self.tabs
        tabs.addTab(ProcessWidget(self.pool, worker), 'worker')

    def close_tab(self, index: int):
        tabs: QTabWidget = self.tabs
        process: ProcessWidget = tabs.widget(index)
        process.abort_task()
        self.tabs.removeTab(index)
