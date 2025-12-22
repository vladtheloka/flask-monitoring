import signal
from restmon.state import mark_shutting_down


def setup_signal_handlers() -> None:
    def _handle_sigterm(signum, frame): # type: ignore
        mark_shutting_down()

    signal.signal(signal.SIGTERM, _handle_sigterm) # type: ignore