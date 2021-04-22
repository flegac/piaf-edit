from piafedit.geometry.point import Point
from piafedit.geometry.size_abs import SizeAbs


def test_point():
    size = SizeAbs(100, 200)
    p1 = Point(.25, .44)

    p2 = p1.abs(size)
    p3 = p2.rel(size)

    print(p1, p2, p3)

    assert p1 == p3
