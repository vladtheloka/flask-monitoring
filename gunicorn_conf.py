# gunicorn_conf.py
from restmon.lifecycle import initiate_shutdown

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

def on_exit(server): # type: ignore
    initiate_shutdown("gunicorn:on_exit")

def worker_exit(server, worker): # type: ignore
    initiate_shutdown("gunicorn:worker_exit")

def worker_int(worker): # type: ignore
    initiate_shutdown("gunicorn:worker_int")

def worker_abort(worker): # type: ignore
    initiate_shutdown("gunicorn:worker_abort")
