import numpy as np

from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import RectAbs
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.source.raw_data_source import RawDataSource

if __name__ == '__main__':
    area = RectAbs(
        pos=PointAbs(1, 1),
        size=SizeAbs(2, 2)
    )
    data = np.zeros((5, 5))
    source = RawDataSource(data)

    out = source.read()
    print(out)

    source.write(np.ones((1, 1)), area)

    out = source.read()
    print(out)
