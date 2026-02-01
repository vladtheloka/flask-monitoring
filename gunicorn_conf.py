# gunicorn_conf.py

bind = "0.0.0.0:5000"
workers = 1
threads = 2
worker_class = "gthread"

timeout = 60
graceful_timeout = 30
keepalive = 2

accesslog = "-"
errorlog = "-"
log_vele = "info"

preload_app = True

def worker_int(worker): # type: ignore
    from restmon.state import shutdown_event
    from restmon.metrics_state import shutdown_in_progress
    shutdown_event.set()
    shutdown_in_progress.set(1)
    worker.log.info("Worker received INT or QUIT signal. Shutting down...") # type: ignore