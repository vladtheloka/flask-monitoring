from __future__ import annotations
from typing import Dict, Union
from flask_restful import Resource
import psutil


class GetMemory(Resource):
    def get(self) -> Dict[str, int]:
        mem = psutil.virtual_memory()
        return {
            'totalMemory': mem.total >> 20,
            'availableMemory': mem.available >> 20,
            'freeMemory': mem.free >> 20,
        }


class GetCPU(Resource):
    def get(self) -> Dict[str, float]:
        cpu = psutil.cpu_times()
        return {
            'cpuuser': cpu.user,
            'cpusystem': cpu.system,
            'cpuidle': cpu.idle,
            'cpuiowait': getattr(cpu, 'iowait', 0),
        }


class GetCPUPercent(Resource):
    def get(self) -> Dict[str, float]:
        cpu = psutil.cpu_times_percent(interval=1, percpu=False)
        return {
            'cpuuser': cpu.user,
            'cpusystem': cpu.system,
            'cpuidle': cpu.idle,
            'cpuiowait': getattr(cpu, 'iowait', 0),
        }


class GetStorage(Resource):
    def get(self) -> Dict[str, Union[int, float]]:
        storage = psutil.disk_usage('/')
        return {
            'roottotal': storage.total >> 20,
            'rootused': storage.used >> 20,
            'rootfree': storage.free >> 20,
            'rootfreepercent': storage.percent,
        }


class FrontPage(Resource):
    def get(self) -> Dict[str, str]:
        return {'Hello': 'World'}