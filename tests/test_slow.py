import time
import pytest
from restmon.api import Slow
from restmon.state import shutdown_event, reset_shutdown_state
from restmon.metrics_state import slow_aborted_total

def test_slow_finished(monkeypatch: pytest.MonkeyPatch):
    reset_shutdown_state()

    monkeypatch.setattr(time, "sleep", lambda _: None)

    res, code = Slow().get()

    assert code == 200
    assert res["status"] == "finished"


def test_slow_aborted(monkeypatch: pytest.MonkeyPatch):
    reset_shutdown_state()

    calls = {"count": 0}

    def fake_sleep(_):
        calls["count"] += 1
        if calls["count"] == 2:
            shutdown_event.set()

    monkeypatch.setattr(time, "sleep", fake_sleep)

    before = slow_aborted_total._value.get()

    res, code = Slow().get()

    after = slow_aborted_total._value.get()

    assert code == 503
    assert res["status"] == "aboprted"
    assert after == before + 1
