from dataclasses import dataclass

from piafedit.model.geometry.size import SizeAbs


@dataclass
class LayoutConfig:
    view: SizeAbs = SizeAbs(1024, 512)
    browser: SizeAbs = SizeAbs(256, 1024)
    overview: SizeAbs = SizeAbs(256, 256)
    tools: SizeAbs = SizeAbs(256, 16)


@dataclass
class WinConfig:
    title: str = 'Piaf Edit'
    size: SizeAbs = SizeAbs(1280, 860)
    layout: LayoutConfig = LayoutConfig()


