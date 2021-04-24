from piafedit.model.geometry.size import SizeAbs, Size


def test_size():
    size = SizeAbs(100, 100)

    s1 = Size(.2, .4)
    s2 = s1.abs(size)
    s3 = s2.rel(size)

    print(s1, s2, s3)

    assert s1 == s3

    s4 = size.rel(s2)
    print(s4)
