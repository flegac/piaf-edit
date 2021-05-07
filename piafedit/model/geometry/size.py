from copy import deepcopy
from dataclasses import dataclass
from typing import Tuple

from piafedit.model.libs.operator import Buffer
from piafedit.model.utils import absolute, relative


@dataclass
class SizeAbs:
    width: int
    height: int

    def __post_init__(self):
        self.width = int(self.width)
        self.height = int(self.height)

    @staticmethod
    def from_buffer(buffer: Buffer):
        h, w = buffer.shape[:2]
        return SizeAbs(w, h)

    @staticmethod
    def from_raw(data: Tuple[int, int]):
        return SizeAbs(*data)

    @property
    def aspect_ratio(self):
        if self.height == 0:
            return 1.0
        return self.width / self.height

    def limit(self, size: 'SizeAbs'):
        self.width = min(size.width, self.width)
        self.height = min(size.height, self.height)
        return self

    def copy(self):
        return deepcopy(self)

    def raw(self):
        return self.width, self.height

    def rel(self, size: 'SizeAbs'):
        return Size(
            width=relative(self.width, size.width),
            height=relative(self.height, size.height),
        )

    def __str__(self) -> str:
        return f'{self.width}x{self.height}'


@dataclass
class Size:
    width: float = 1.
    height: float = 1.

    @staticmethod
    def random():
        import random
        return Size(
            width=random.random(),
            height=random.random()
        )

    @staticmethod
    def from_aspect(aspect_ratio: float):
        if aspect_ratio >= 1.0:
            return Size(1.0, 1.0 / aspect_ratio)
        return Size(aspect_ratio, 1.0)

    @staticmethod
    def from_raw(data: Tuple[float, float]):
        return Size(*data)

    def copy(self):
        return deepcopy(self)

    def interpolate(self, a: float, other: 'Size'):
        dw = other.width - self.width
        dh = other.height - self.height
        return Size(width=self.width + a * dw, height=self.height + a * dh)

    def raw(self):
        return self.width, self.height

    def abs(self, size: SizeAbs):
        return SizeAbs(
            width=absolute(self.width, size.width),
            height=absolute(self.height, size.height),
        )

    @property
    def aspect_ratio(self):
        return self.width / self.height
