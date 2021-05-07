import random
import time
from pathlib import Path

from piafedit.model.geometry.point import Point
from piafedit.model.geometry.rect import Rect
from piafedit.model.geometry.size import SizeAbs, Size
from piafedit.model.geometry.trajectory import Trajectory
from piafedit.model.source.data_source import DataSource
from piafedit.model.source.rio_data_source import RIODataSource
from piafedit.model.source.tile_source import TileConfig, TileSource


def timeit(f):
    def wrap(*args, **kwargs):
        start = time.time()
        f(*args, **kwargs)
        end = time.time()
        total = end - start
        print(f'{f.__name__}: {total}')

    return wrap


image_path = Path('./LC08_L1TP_139045_20170304_20170316_01_T1_B6.tiff')
image_path = Path('../resources/fat.tif')

random.seed(22)

trajectory = Trajectory([
    Rect(pos=Point.random(), size=Size(.12, .12))
    for i in range(4)
])


@timeit
def eval(source: DataSource):
    for window in (trajectory.iter(20)):
        data = source.read(window)
        print(data.shape)


if __name__ == '__main__':
    source = RIODataSource(image_path)
    source2 = TileSource(source, TileConfig(SizeAbs(256, 256)))
    eval(source)
    print('-------------------------')
    eval(source2)
