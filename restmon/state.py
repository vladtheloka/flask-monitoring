# restmon/state.py
import threading

_ready = True
_shutting_down = False
_lock = threading.Lock()

shutdown_event = threading.Event()

def mark_shutting_down() -> None:
    global _shutting_down
    _shutting_down = True
    shutdown_event.set()

def is_shutting_down() -> bool:
    return _shutting_down

def reset_shutdown_state() -> None:
    global _shutting_down
    _shutting_down = False

def set_not_ready() -> None:
    global _ready
    with _lock:
        _ready = False

def is_ready() -> bool:
    with _lock:
        return _ready