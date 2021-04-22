import uuid
from abc import ABC, abstractmethod
from typing import Union, Tuple

import numpy as np

from piafedit.geometry.rect import Rect, RectAbs
from piafedit.geometry.size import SizeAbs, Size


class DataSource(ABC):
    def __init__(self, name: str = None):
        self.name = name or str(uuid.uuid4())

    @abstractmethod
    def dtype(self):
        ...

    @abstractmethod
    def shape(self) -> Tuple[int, int, int]:
        ...

    @abstractmethod
    def size(self) -> SizeAbs:
        ...

    @abstractmethod
    def read(self, area: Union[Rect, RectAbs] = None, out_shape: Union[Size, SizeAbs] = None) -> np.ndarray:
        ...

    @abstractmethod
    def write(self, buffer: np.ndarray, area: Union[Rect, RectAbs] = None):
        ...
