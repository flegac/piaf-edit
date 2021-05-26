from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from piafedit.config.win_config import WinConfig
from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.size import SizeAbs


def synchronize_widget(widget: QWidget, config: WinConfig):
    widget.setWindowTitle(config.title)
    widget.move(config.offset.x, config.offset.y)
    widget.resize(config.size.width, config.size.height)
    if config.full_screen:
        widget.showMaximized()
    else:
        widget.show()
    message = f'widget updated: offset: {config.offset} size: {config.size} fullscreen: {config.full_screen}'
    widget.setStatusTip(message)


def synchronize_config(widget: QWidget, config: WinConfig):
    config.title = widget.windowTitle()
    config.offset = PointAbs(widget.x(), widget.y())
    config.size = SizeAbs(widget.width(), widget.height())
    config.full_screen = (widget.windowState() == Qt.WindowMaximized)
    message = f'widget updated: offset: {config.offset} size: {config.size} fullscreen: {config.full_screen}'
    widget.setStatusTip(message)
