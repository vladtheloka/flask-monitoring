# tests/test_lifecycle.py
from restmon.lifecycle import initiate_shutdown # type: ignore
from restmon.state import shutdown_event, reset_shutdown_state

def test_sigterm_sets_shutdown_flag():
    reset_shutdown_state()

    initiate_shutdown("test")

    assert shutdown_event.is_set()
