# restmon/state.py
import threading

shutdown_event = threading.Event()

def is_shutting_down() -> bool:
    return shutdown_event.is_set()

def reset_shutdown_state() -> None:
    shutdown_event.clear()
