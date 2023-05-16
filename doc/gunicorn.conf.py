import multiprocessing

bind = '127.0.0.1:8002'
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = '/var/log/gunicorn/portfolio-access.log'
errorlog = '/var/log/gunicorn/portfolio-error.log'
pidfile = '/var/run/gunicorn/portfolio.pid'
