from dataclasses import dataclass

from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.size import SizeAbs


@dataclass
class WinConfig:
    title: str = 'Piaf Edit'
    offset: PointAbs = PointAbs(0, 0)
    size: SizeAbs = SizeAbs(1280, 980)
    full_screen: bool = True
