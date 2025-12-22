bind = "0.0.0.0:5000"
workers = 2
threads = 4
timeout = 60
graceful_timeout = 30

accesslog = "-"
errorlog = "-"

preload_app = True

def worker_exit(server, worker): # type: ignore
    server.log.info("Worker exiting gracefully") # type: ignore