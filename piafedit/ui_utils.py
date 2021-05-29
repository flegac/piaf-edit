import logging
from contextlib import contextmanager
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

log = logging.getLogger()


def resources_path():
    return Path(__file__).parent.parent / 'resources'


@contextmanager
def gui_app():
    from PyQt5 import QtWidgets
    import sys
    try:
        import pyqttango
        pyqttango.init_resources()
    except:
        log.warning('Could not load tango icon set')

    import pyqtgraph as pg
    pg.setConfigOptions(imageAxisOrder='row-major')
    app = QtWidgets.QApplication([])
    from PyQt5 import QtGui
    QtGui.QIcon.setThemeName('tango')

    try:
        yield app
    finally:
        sys.exit(app.exec_())


def find_ui(name: str):
    # FIXME: https://setuptools.readthedocs.io/en/latest/userguide/datafiles.html#accessing-data-files-at-runtime
    path = resources_path() / f'ui/{name}.ui'
    return path


def load_ui(name: str, widget: QWidget):
    uic.loadUi(find_ui(name), widget)
