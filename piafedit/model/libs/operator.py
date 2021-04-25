from typing import Callable

import numpy as np

Buffer = np.ndarray
Operator = Callable[[Buffer], Buffer]
