import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1

bind = "127.0.0.1:8187"

daemon = True

pidfile = 'gunicorn.pid'

accesslog = '/logs/report_tools/gunicorn_access.log'

errorlog = '/logs/report_tools/gunicorn_error.log'
