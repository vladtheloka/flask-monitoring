import os
import psutil
import platform  # Import the platform module
from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app) # type: ignore

class SystemResources:
	@staticmethod
	def get_os_details() -> dict[str, str]:
		return {
			"os": os.name,
			"platform": platform.system(),
			"release": os.uname().release,
			"version": os.uname().version,
			"machine": os.uname().machine,
		}

	@staticmethod
	def get_cpu_usage():
		return psutil.cpu_percent(interval=1)

	@staticmethod
	def get_memory_usage() -> dict[str, int | float]:
		memory = psutil.virtual_memory()
		return {
			"total": memory.total,
			"available": memory.available,
			"used": memory.used,
			"percent": memory.percent,
		}

	@staticmethod
	def get_storage_usage() -> dict[str, int | float]:
		disk = psutil.disk_usage('/')
		return {
			"total": disk.total,
			"used": disk.used,
			"free": disk.free,
			"percent": disk.percent,
		}
	
	@staticmethod
	def get_network_usage() -> dict[str, float]:
			net_io = psutil.net_io_counters()
			return {
				"bytes_sent": net_io.bytes_sent,
				"bytes_recv": net_io.bytes_recv,
				"packets_sent": net_io.packets_sent,
				"packets_recv": net_io.packets_recv,
			}

	@staticmethod
	def get_system_uptime() -> float:
			return psutil.boot_time()

	@staticmethod
	def get_process_count() -> int:
			return len(psutil.pids())