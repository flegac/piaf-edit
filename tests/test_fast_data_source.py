from pathlib import Path
from unittest import TestCase

import numpy as np

from piafedit.model.source.fast_data_source import FastDataSource
from piafedit.model.geometry.point import Point
from piafedit.model.geometry.rect import Rect
from piafedit.model.geometry.size import SizeAbs, Size

path = Path('../resources/test.tif')
source = FastDataSource(path)
area = Rect(
    pos=Point(.1, .1),
    size=Size(.1, .1)
)

SIZE = 8_000


class TestFastDataSource(TestCase):
    # configure tests --------------------------------------------------
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        if not path.exists():
            size = SizeAbs(SIZE, SIZE)
            image = np.random.random((*size.raw(), 3)) * 255
            image = image.astype('uint8')
            source.create(image)

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        # path.unlink()

    # actual tests -----------------------------------------------------

    def test_overview(self):
        print(f'creating overview...')

        source.create_overview()
        print(f'overview created!')

    def test_size(self):
        print('read size:', source.size())

    def test_write(self):
        data = np.zeros((100, 100))
        # source.write(data, area)

    def test_read(self):
        data = source.read(area)
        print('read data:', data.shape)
