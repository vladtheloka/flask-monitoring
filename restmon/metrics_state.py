from prometheus_client import Gauge, Counter

shutdown_in_progress = Gauge(
    "shutdown_in_progress",
    "Service is in graceful shutdown"
)

requests_rejected_total = Counter(
    "requests_rejected_total",
    "Requests rejected due to shutdown"
)

slow_aborted_total = Counter(
    "slow_aborted_total",
    "Slow requests aborted due to shutdown"
)