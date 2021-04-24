import uuid
from abc import ABC, abstractmethod
from typing import Union, Tuple

import numpy as np

from piafedit.model.geometry.rect import Rect, RectAbs
from piafedit.model.geometry.size import SizeAbs, Size


class DataSource(ABC):
    def __init__(self, name: str = None):
        self.name = name or str(uuid.uuid4())

    @abstractmethod
    def bands(self) -> int:
        ...

    @abstractmethod
    def dtype(self):
        ...

    @abstractmethod
    def shape(self) -> Tuple[int, int, int]:
        ...

    @abstractmethod
    def size(self) -> SizeAbs:
        ...

    @property
    def aspect_ratio(self):
        size = self.size()
        return size.width / size.height

    @abstractmethod
    def read(self, area: Union[Rect, RectAbs] = None, out_shape: Union[Size, SizeAbs] = None) -> np.ndarray:
        ...

    @abstractmethod
    def write(self, buffer: np.ndarray, area: Union[Rect, RectAbs] = None):
        ...

    def overview_size(self, size: int) -> SizeAbs:
        aspect = self.aspect_ratio
        if aspect > 1:
            w, h = size, size / aspect
        else:
            w, h = size * aspect, size
        return SizeAbs(w, h)

    def overview(self, size: int):
        overview_size = self.overview_size(size)
        overview = self.read(out_shape=overview_size)
        return overview