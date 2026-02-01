# restmon/lifecycle.py
import signal
import logging
from restmon.state import shutdown_event

log = logging.getLogger(__name__)

def setup_signal_handlers() -> None:

    signal.signal(signal.SIGTERM, _handle_shutdown) # type: ignore
    signal.signal(signal.SIGINT, _handle_shutdown) # type: ignore

def _handle_shutdown(signum, frame): # type: ignore
    log.warning("Receive signal %s, entering graceful shutdown", signum) # type: ignore
    shutdown_event.set()
