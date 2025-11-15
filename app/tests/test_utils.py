from app.utils import get_cpu_usage, get_memory_usage, get_disk_usage, top_processes

def test_cpu_usage():
    assert 0 <= get_cpu_usage() <= 100

def test_memory_usage():
    assert 0 <= get_memory_usage() <= 100

def test_disk_usage():
    assert 0 <= get_disk_usage() <= 100

def test_top_processes():
    procs = top_processes()
    assert len(procs) <= 5
    for pid, name, cpu in procs:
        assert pid > 0
        assert isinstance(name, str)
        assert 0 <= cpu <= 100
