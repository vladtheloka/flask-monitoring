# restmon/metrics.py
from flask_restful import Resource
from typing import List
import time
from restmon.resources import SystemResources

START_TIME = time.time()


class Metrics(Resource):
    """Prometheus-compatible metrics endpoint."""

    def get(self) -> str:
        uptime = time.time() - START_TIME
        mem = SystemResources.get_memory_usage()
        disk = SystemResources.get_storage_usage()

        lines: List[str] = [
            "# HELP process_uptime_seconds Process uptime in seconds",
            "# TYPE process_uptime_seconds gauge",
            f"process_uptime_seconds {uptime}",

            "# HELP system_cpu_usage_percent CPU usage percent",
            "# TYPE system_cpu_usage_percent gauge",
            f"system_cpu_usage_percent {SystemResources.get_cpu_usage()}",

            "# HELP system_memory_usage_percent Memory usage percent",
            "# TYPE system_memory_usage_percent gauge",
            f"system_memory_usage_percent {mem['percent']}",

            "# HELP system_memory_used_bytes Used memory in bytes",
            "# TYPE system_memory_used_bytes gauge",
            f"system_memory_used_bytes {mem['used']}",

            "# HELP system_disk_usage_percent Disk usage percent",
            "# TYPE system_disk_usage_percent gauge",
            f"system_disk_usage_percent {disk['percent']}",

            "# HELP process_count Number of running processes",
            "# TYPE process_count gauge",
            f"process_count {SystemResources.get_process_count()}",
        ]

        return "\n".join(lines), 200, {"Content-Type": "text/plain; version=0.0.4"} # type: ignore