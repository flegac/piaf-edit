from copy import deepcopy
from dataclasses import dataclass
from typing import Tuple

from piafedit.model.geometry.point import Point, PointAbs
from piafedit.model.geometry.size import Size, SizeAbs
from piafedit.model.libs.operator import Buffer

RawRect = Tuple[Tuple[int, int], Tuple[int, int]]


@dataclass
class RectAbs:
    pos: PointAbs
    size: SizeAbs

    def copy(self):
        return deepcopy(self)

    def raw(self) -> RawRect:
        return self.pos.raw(), self.size.raw()

    @staticmethod
    def from_raw(data: RawRect):
        return RectAbs(Point.from_raw(data[0]), Size.from_raw(data[1]))

    @property
    def aspect_ratio(self):
        return self.size.aspect_ratio

    @property
    def center(self):
        return PointAbs(
            int(self.pos.x + self.size.width / 2),
            int(self.pos.y + self.size.height / 2)
        )

    def rel(self, size: SizeAbs):
        return Rect(
            pos=self.pos.rel(size),
            size=self.size.rel(size)
        )

    def limit(self, size: Size):
        res = deepcopy(self)
        if res.pos.x < 0:
            res.size.width += res.pos.x
            res.pos.x = 0
        if res.pos.y < 0:
            res.size.height += res.pos.y
            res.pos.y = 0
        res.size.width = max(0, min(size.width - res.pos.x, res.size.width))
        res.size.height = max(0, min(size.height - res.pos.y, res.size.height))
        return res

    def scale(self, rx: float, ry: float):
        return RectAbs(
            pos=PointAbs(
                x=round(self.pos.x * rx),
                y=round(self.pos.y * ry)
            ),
            size=SizeAbs(
                width=round(self.size.width * rx),
                height=round(self.size.height * ry)
            )
        )

    def move(self, dx: int, dy: int):
        self.pos.move(dx, dy)
        return self

    def crop(self, buffer: Buffer):
        x1, y1 = self.pos.raw()
        w, h = self.size.raw()
        bh, bw = buffer.shape[:2]
        x2 = max(0, x1 + w)
        y2 = max(0, y1 + h)
        x1 = max(0, min(x1, bw))
        y1 = max(0, min(y1, bh))
        return buffer[y1:y2, x1:x2, ...]

    def __str__(self) -> str:
        return f'[{self.pos} @ {self.size}]'


@dataclass
class Rect:
    pos: Point = Point()
    size: Size = Size()

    @staticmethod
    def random():
        return Rect(pos=Point.random(), size=Size.random())

    @staticmethod
    def from_raw(data: Tuple[Tuple[float, float], Tuple[float, float]]):
        return Rect(Point.from_raw(data[0]), Size.from_raw(data[1]))

    def copy(self):
        return deepcopy(self)

    def move(self, dx: float, dy: float):
        self.pos.move(dx, dy)

    def interpolate(self, a: float, other: 'Rect'):
        return Rect(
            pos=self.pos.interpolate(a, other.pos),
            size=self.size.interpolate(a, other.size)
        )

    def raw(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        return self.pos.raw(), self.size.raw()

    def abs(self, size: SizeAbs):
        return RectAbs(
            pos=self.pos.abs(size),
            size=self.size.abs(size)
        )

    def crop(self, buffer: Buffer):
        return self.abs(SizeAbs.from_buffer(buffer)).crop(buffer)
