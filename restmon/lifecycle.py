# restmon/lifecycle.py
import signal
from restmon.state import mark_shutting_down
import time

GRACE_PERIOD_SECONDS = 5

def setup_signal_handlers() -> None:
    signal.signal(signal.SIGTERM, _handle_sigterm) # type: ignore
    signal.signal(signal.SIGINT, _handle_sigterm) # type: ignore

def _handle_sigterm(signum, frame): # type: ignore
    mark_shutting_down()
    time.sleep(GRACE_PERIOD_SECONDS)