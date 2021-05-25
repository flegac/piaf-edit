from dataclasses import dataclass

from piafedit.model.geometry.size import SizeAbs


@dataclass
class WinConfig:
    title: str = 'Piaf Edit'
    size: SizeAbs = SizeAbs(1280, 860)
