from typing import TypeVar, Generic, List

T = TypeVar('T')


class Trajectory(Generic[T]):
    def __init__(self, trajectory: List[T]):
        self.trajectory = trajectory

    def iter(self, n: int):
        for i in range(n):
            a = i / (n - 1)
            yield self.interpolate(a)

    def interpolate(self, a: float) -> T:
        points = len(self.trajectory)
        intervals = points - 1
        inter_size = 1. / intervals

        for i in range(points - 1):
            if a <= inter_size:
                b = a / inter_size
                return self.trajectory[i].interpolate(b, self.trajectory[i + 1])
            else:
                a -= inter_size

        b = 1.0 + a
        return self.trajectory[-2].interpolate(b, self.trajectory[-1])
