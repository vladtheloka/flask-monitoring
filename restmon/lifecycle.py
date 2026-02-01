# restmon/lifecycle.py
import signal
import logging

log = logging.getLogger(__name__)

def setup_signal_handlers() -> None:

    signal.signal(signal.SIGTERM, _handle_shutdown) # type: ignore
    signal.signal(signal.SIGINT, _handle_shutdown) # type: ignore

def _handle_shutdown(signum, frame): # type: ignore
    with open("/tmp/sigterm.log", "w") as f:
        f.write("SIGTERM RECEIVED\n")
