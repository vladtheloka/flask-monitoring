# restmon/lifecycle.py
import logging
from restmon.state import shutdown_event

log = logging.getLogger(__name__)


def initiate_shutdown(source: str = "unknown"): # type: ignore
    log.warning("Receive signal %s, entering graceful shutdown", source) # type: ignore
    shutdown_event.set()
