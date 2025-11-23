from __future__ import annotations
import platform
from typing import Literal


Platform = Literal["Windows", "Linux", "Darwin"]


def get_platform() -> Platform:
    """
    Typed wrapper around platform.system().
    """
    system = platform.system()
    if system not in ("Windows", "Linux", "Darwin"):
        return "Linux"  # fallback
    return system