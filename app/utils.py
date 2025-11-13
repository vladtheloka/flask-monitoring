import psutil

def get_cpu_usage():
    return psutil.cpu_percent(interval=0.5)

def get_memory_usage():
    mem = psutil.virtual_memory()
    return mem.percent

def get_disk_usage():
    disk = psutil.disk_usage('/')
    return disk.percent

def top_processes(n=5):
    procs = [(p.info['pid'], p.info['name'], p.info['cpu_percent']) 
             for p in psutil.process_iter(['pid', 'name', 'cpu_percent'])]
    return sorted(procs, key=lambda x: x[2], reverse=True)[:n]
