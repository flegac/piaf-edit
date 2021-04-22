from math import floor

import numpy as np


def absolute(a: float, size: int, clip: bool = False) -> int:
    res = a * size
    if clip:
        res = np.clip(res, 0, size)
    return int(res)


def relative(a: int, size: int) -> float:
    return a / size


def interval(a: float, size: float):
    parts = int(1.0 / size)
    return min(floor(a * parts), parts - 1)
    # return min(floor(a / size), parts - 1)


if __name__ == '__main__':
    s = .1
    for x in [
        0.,
        .099,
        .1,
        .265,
        .485,
        .8999999,
        .9,
        .999999999,
        .999999999999999999999999999999999999999999999999999,

        1.
    ]:
        val = interval(x, s)
        print(x, ' -> ', val)
