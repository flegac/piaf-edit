from dataclasses import dataclass

from piafedit.config.win_config import WinConfig


@dataclass
class PiafConfig:
    window: WinConfig = WinConfig()
