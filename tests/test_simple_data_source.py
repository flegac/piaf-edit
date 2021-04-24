from unittest import TestCase

import numpy as np

from piafedit.model.source.simple_data_source import SimpleDataSource
from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import RectAbs
from piafedit.model.geometry.size import SizeAbs

area = RectAbs(
    pos=PointAbs(1, 1),
    size=SizeAbs(2, 2)
)
data = np.zeros((5, 5))
source = SimpleDataSource(data)


class TestSimpleDataSource(TestCase):
    def test_size(self):
        size = source.size()
        print(size)

    def test_write(self):
        out = source.read()
        print(out)

        source.write(np.ones((1, 1)), area)

        out = source.read()
        print(out)

    def test_read(self):
        out = source.read()
        print(out)
