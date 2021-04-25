from dataclasses import dataclass
from pathlib import Path


@dataclass
class Project:
    name: str
    path: Path
