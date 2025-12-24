# gunicorn_conf.py

bind = "0.0.0.0:5000"
workers = 1
threads = 2
worker_class = "gthread"

timeout = 30
graceful_timeout = 20

accesslog = "-"
errorlog = "-"
log_vele = "info"

preload_app = False