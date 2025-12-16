# restmon/state.py
import threading

_ready = True
_lock = threading.Lock()


def set_not_ready() -> None:
    global _ready
    with _lock:
        _ready = False


def is_ready() -> bool:
    with _lock:
        return _ready