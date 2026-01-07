# restmon/lifecycle.py
import signal
from restmon.state import shutdown_event
import logging

log = logging.getLogger(__name__)

def setup_signal_handlers() -> None:

    signal.signal(signal.SIGTERM, _handle_shutdown) # type: ignore
    signal.signal(signal.SIGINT, _handle_shutdown) # type: ignore

def _handle_shutdown(signum, frame): # type: ignore
        log.warning("Received signal, entering graceful shutdown")
        shutdown_event.set()