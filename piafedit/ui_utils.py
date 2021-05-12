from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


def resources_path():
    return Path(__file__).parent.parent / 'resources'


def find_ui(name: str):
    # FIXME: https://setuptools.readthedocs.io/en/latest/userguide/datafiles.html#accessing-data-files-at-runtime
    path = resources_path() / f'ui/{name}.ui'
    return path


def load_ui(name: str, widget: QWidget):
    uic.loadUi(find_ui(name), widget)
