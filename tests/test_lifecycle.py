# tests/test_lifecycle.py

import signal
from restmon.lifecycle import _handle_shutdown # type: ignore
from restmon.state import shutdown_event, reset_shutdown_state

def test_sigterm_sets_shutdown_flag():
    reset_shutdown_state()

    _handle_shutdown(signal.SIGTERM, None)

    assert shutdown_event.is_set()
