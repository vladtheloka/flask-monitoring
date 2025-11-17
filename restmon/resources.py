from flask_restful import Resource

import math
import psutil

class getMemory(Resource):
	def get(self):
		mem=psutil.virtual_memory()
		return {'totalMemory' : mem.total >> 20, 'availableMemory' : mem.available >> 20, 'freeMemory' : mem.free >> 20}


class getCPU(Resource):
	def get(self):
		cpu=psutil.cpu_times()
		return {'cpuuser' : cpu.user, 'cpusystem' : cpu.system, 'cpuidle' : cpu.idle, 'cpuiowait' : cpu.iowait}


class getCPUPercent(Resource):
	def get(self):
		cpu=psutil.cpu_times_percent(interval=1,percpu=False)
		return {'cpuuser' : cpu.user, 'cpusystem' : cpu.system, 'cpuidle' : cpu.idle, 'cpuiowait' : cpu.iowait}


class getStorage(Resource):
	def get(self):
		storage=psutil.disk_usage('/')
		return {'roottotal' : storage.total >> 20, 'rootused' : storage.used >> 20, 'rootfree' : storage.free >> 20, 'rootfreepercent' : storage.percent }


class frontPage(Resource):
	def get(self):
		return {'Hello' : 'World'}
		