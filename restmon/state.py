# restmon/state.py
import threading

_ready = True
_lock = threading.Lock()
_shutdown_event = threading.Event()

def mark_shutting_down() -> None:
    _shutdown_event.set()

def is_shutting_down() -> bool:
    return _shutdown_event.is_set()

def set_not_ready() -> None:
    global _ready
    with _lock:
        _ready = False


def is_ready() -> bool:
    with _lock:
        return _ready