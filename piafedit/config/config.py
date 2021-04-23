from dataclasses import dataclass
from enum import Enum, auto

from piafedit.geometry.size import SizeAbs


@dataclass
class LayoutConfig:
    view: SizeAbs = SizeAbs(1024, 512)
    browser: SizeAbs = SizeAbs(1024, 128)
    overview: SizeAbs = SizeAbs(256, 256)
    tools: SizeAbs = SizeAbs(256, 512)


@dataclass
class WinConfig:
    title: str = 'easy-qt'
    size: SizeAbs = SizeAbs(1280, 860)
    layout: LayoutConfig = LayoutConfig()


class Win(Enum):
    overview = auto()
    view = auto()
    browser = auto()
    toolbar = auto()
    infos = auto()
