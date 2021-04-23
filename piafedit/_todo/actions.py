from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict


class Actions(Enum):
    exit = auto()

    layout_switch_lock = auto()
    layout_store = auto()
    layout_restore = auto()


@dataclass
class Shortcut:
    key: str
    action: Actions


class ShorcutMapping:
    def __init__(self):
        self.by_key: Dict[str, Actions] = dict()
        self.by_action: Dict[Actions, str] = dict()

    def register(self, shortcut: Shortcut):
        self.by_key[shortcut.key] = shortcut
        self.by_action[shortcut.action] = shortcut
