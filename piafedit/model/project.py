from dataclasses import dataclass
from pathlib import Path
from typing import List

from piafedit.model.source.data_source import DataSource





@dataclass
class Project:
    name: str
    path: Path
    sources: List[DataSource]
