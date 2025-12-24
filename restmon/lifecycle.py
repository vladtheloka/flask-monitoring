# restmon/lifecycle.py
import signal
from restmon.state import shutdown_event
import logging

log = logging.getLogger(__name__)

def setup_signal_handlers() -> None:
    def _handle_shutdown(signum, frame): # type: ignore
        log.info("Received signal %s, entering shudown", signum) # type: ignore
        shutdown_event.set()

    signal.signal(signal.SIGTERM, _handle_shutdown) # type: ignore
    signal.signal(signal.SIGINT, _handle_shutdown) # type: ignore