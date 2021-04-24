from dataclasses import dataclass
from typing import Tuple

import numpy as np

from piafedit.model.utils import absolute, relative


@dataclass
class SizeAbs:
    width: int
    height: int

    def __post_init__(self):
        self.width = int(self.width)
        self.height = int(self.height)

    @staticmethod
    def from_buffer(buffer: np.ndarray):
        h, w = buffer.shape[:2]
        return SizeAbs(w, h)

    @staticmethod
    def from_raw(data: Tuple[int, int]):
        return SizeAbs(*data)

    def limit(self, size: 'SizeAbs'):
        self.width = min(size.width, self.width)
        self.height = min(size.height, self.height)

    def raw(self):
        return self.width, self.height

    def rel(self, size: 'SizeAbs'):
        return Size(
            width=relative(self.width, size.width),
            height=relative(self.height, size.height),
        )


@dataclass
class Size:
    width: float = 1.
    height: float = 1.

    @staticmethod
    def from_raw(data: Tuple[float, float]):
        return Size(*data)

    def raw(self):
        return self.width, self.height

    def abs(self, size: SizeAbs):
        return SizeAbs(
            width=absolute(self.width, size.width),
            height=absolute(self.height, size.height),
        )
