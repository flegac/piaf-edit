from dataclasses import dataclass
from typing import Tuple

from piafedit.model.geometry.size import SizeAbs


@dataclass
class SourceInfos:
    name: str
    dtype: str
    shape: Tuple[int, int, int]

    @property
    def size(self):
        h, w = self.shape[:2]
        return SizeAbs(w, h)

    @property
    def bands(self):
        return self.shape[2]

    @property
    def aspect(self):
        return self.size.aspect_ratio