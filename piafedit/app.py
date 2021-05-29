import logging

from PyQt5.QtGui import QIcon

from piafedit.editor_api import P
from piafedit.gui.main_ui import MainUi
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.source.rio_data_source import RIODataSource
from piafedit.model.source.window import Window
from piafedit.model.work_model import WorkModel
from piafedit.ui_utils import resources_path, gui_app

IMAGE_SIZE = 10_000

log = logging.getLogger()
log.setLevel(logging.DEBUG)


def gen_big_image():
    source = RIODataSource(resources_path() / 'kitten.jpg')
    dest = RIODataSource(resources_path() / 'fat.tif')

    size = SizeAbs(IMAGE_SIZE, IMAGE_SIZE / source.infos().aspect)
    log.debug(f'resize from {source.infos().size} to {size}')
    if not dest.path.exists():
        buffer = source.read(Window.from_size(size))
        dest.create(buffer)
    return dest


def main():
    with gui_app():
        model = WorkModel(resources_path())
        QIcon.setThemeName('tango')
        P.main_window = MainUi(model)


if __name__ == '__main__':
    main()
