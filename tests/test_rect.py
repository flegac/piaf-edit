import numpy as np

from piafedit.geometry.point import Point
from piafedit.geometry.rect import Rect
from piafedit.geometry.size import Size


def test_crop():
    buffer = np.random.random((6, 6)) * 9
    buffer = buffer.astype('uint8')

    rect = Rect(
        pos=Point(.2, .3),
        size=Size(.4, .4)
    )

    area = rect.crop(buffer)

    print(buffer)
    print(area)
