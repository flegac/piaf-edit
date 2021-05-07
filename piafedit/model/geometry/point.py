from copy import deepcopy
from dataclasses import dataclass
from typing import Tuple

from piafedit.model.geometry.size import SizeAbs
from piafedit.model.utils import absolute, relative


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

    def copy(self):
        return deepcopy(self)

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy
        return self

    def raw(self):
        return self.x, self.y

    def rel(self, size: SizeAbs):
        return Point(
            x=relative(self.x, size.width),
            y=relative(self.y, size.height)
        )

    def __str__(self) -> str:
        return f'{self.x, self.y}'


@dataclass
class Point:
    x: float = 0.
    y: float = 0.

    @staticmethod
    def random():
        import random
        return Point(
            x=random.random(),
            y=random.random()
        )

    @staticmethod
    def from_raw(data: Tuple[float, float]):
        return Point(*data)

    def copy(self):
        return deepcopy(self)

    def move(self, dx: float, dy: float):
        self.x += dx
        self.y += dy
        return self

    def interpolate(self, a: float, other: 'Point'):
        dx = other.x - self.x
        dy = other.y - self.y
        return Point(x=self.x + a * dx, y=self.y + a * dy)

    def raw(self):
        return self.x, self.y

    def abs(self, size: SizeAbs):
        return PointAbs(
            x=absolute(self.x, size.width),
            y=absolute(self.y, size.height)
        )
