# gunicorn_conf.py

bind = "0.0.0.0:5000"
workers = 1
threads = 2
worker_class = "gthread"

timeout = 60
graceful_timeout = 30

accesslog = "-"
errorlog = "-"
log_vele = "info"

preload_app = False