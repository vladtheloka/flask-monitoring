# restmon/lifecycle.py
import signal
from restmon.state import mark_shutting_down

def setup_signal_handlers() -> None:
    signal.signal(signal.SIGTERM, _handle_sigterm) # type: ignore

def _handle_sigterm(signum, frame): # type: ignore
    mark_shutting_down()