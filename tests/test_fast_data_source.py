from pathlib import Path
from unittest import TestCase

import numpy as np
import rasterio
from rasterio.profiles import DefaultGTiffProfile

from piafedit.data_source.fast_data_source import FastDataSource
from piafedit.geometry.point import Point
from piafedit.geometry.rect import Rect
from piafedit.geometry.size import SizeAbs, Size


def create_image(name: Path, size: SizeAbs):
    shape = size.raw()
    image = np.random.random((*shape, 3)) * 255
    image = image.astype('uint8')
    count = image.shape[2]

    with rasterio.open(name, 'w',
                       **DefaultGTiffProfile(
                           tiled=True,
                           width=size.width,
                           height=size.height,
                           count=count,
                           dtype=image.dtype,
                           driver='GTiff'
                       )) as dst:
        for i in range(count):
            data = image[..., i]
            dst.write(data, i + 1)


path = Path('../resources/test.tif')
source = FastDataSource(path)
area = Rect(
    pos=Point(.1, .1),
    size=Size(.1, .1)
)


class TestFastDataSource(TestCase):
    # configure tests --------------------------------------------------
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        if not path.exists():
            create_image(path, SizeAbs(10_000, 10_000))

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        # path.unlink()

    # actual tests -----------------------------------------------------

    def test_size(self):
        print('read size:', source.size())

    def test_write(self):
        data = np.zeros((100, 100))
        # source.write(data, area)

    def test_read(self):
        data = source.read(area)
        print('read data:', data.shape)
