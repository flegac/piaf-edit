from dataclasses import dataclass

from piafedit.model.geometry.rect import RectAbs
from piafedit.model.geometry.size import SizeAbs


@dataclass
class Window:
    window: RectAbs = None
    size: SizeAbs = None