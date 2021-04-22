from dataclasses import dataclass
from typing import Tuple

from piafedit.geometry.size import SizeAbs
from piafedit.geometry.utils import absolute, relative


@dataclass
class PointAbs:
    x: int
    y: int

    def __post_init__(self):
        self.x = int(self.x)
        self.y = int(self.y)

    @staticmethod
    def from_raw(data: Tuple[int, int]):
        return PointAbs(*data)

    def raw(self):
        return self.x, self.y

    def rel(self, size: SizeAbs):
        return Point(
            x=relative(self.x, size.width),
            y=relative(self.y, size.height)
        )


@dataclass
class Point:
    x: float = 0.
    y: float = 0.

    @staticmethod
    def from_raw(data: Tuple[float, float]):
        return Point(*data)

    def raw(self):
        return self.x, self.y

    def abs(self, size: SizeAbs):
        return PointAbs(
            x=absolute(self.x, size.width),
            y=absolute(self.y, size.height)
        )
