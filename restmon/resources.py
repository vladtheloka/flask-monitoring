from flask_restful import Resource
import psutil


class getMemory(Resource):
    def get(self) -> dict[str, int]:
        mem = psutil.virtual_memory()
        return {
            'totalMemory': mem.total >> 20,
            'availableMemory': mem.available >> 20,
            'freeMemory': mem.free >> 20,
        }


class getCPU(Resource):
    def get(self) -> dict[str, float]:
        cpu = psutil.cpu_times()
        return {
            'cpuuser': cpu.user,
            'cpusystem': cpu.system,
            'cpuidle': cpu.idle,
            'cpuiowait': getattr(cpu, 'iowait', 0),
        }


class getCPUPercent(Resource):
    def get(self) -> dict[str, float]:
        cpu = psutil.cpu_times_percent(interval=1, percpu=False)
        return {
            'cpuuser': cpu.user,
            'cpusystem': cpu.system,
            'cpuidle': cpu.idle,
            'cpuiowait': getattr(cpu, 'iowait', 0),
        }


class getStorage(Resource):
    def get(self) -> dict[str, int | float]:
        storage = psutil.disk_usage('/')
        return {
            'roottotal': storage.total >> 20,
            'rootused': storage.used >> 20,
            'rootfree': storage.free >> 20,
            'rootfreepercent': storage.percent,
        }


class frontPage(Resource):
    def get(self):
        return {'Hello': 'World'}
