from unittest import TestCase

import numpy as np

from piafedit.model.geometry.point import Point
from piafedit.model.geometry.rect import Rect
from piafedit.model.source.raw_data_source import RawDataSource

shape = (5, 5, 3)
buffer = np.array(range(5 * 5 * 3)).reshape(shape)
source = RawDataSource(buffer)


class TestRawDataSource(TestCase):

    def test_infos(self):
        infos = source.infos()
        assert infos.dtype == buffer.dtype
        assert infos.shape == shape
        assert infos.bands == 3
        assert infos.size.raw() == (5,5)

    def test_write(self):
        b = np.zeros(shape)
        source.write_at(b)
        assert np.array_equal(buffer, b)

    def test_read(self):
        x = source.read_at()
        assert np.array_equal(x, buffer)
