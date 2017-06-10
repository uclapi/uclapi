import multiprocessing

bind = "127.0.0.1:9000"

# Run cores * 4 + 1 workers in gunicorn
# This is set deliberately high in case of long Oracle transactions locking Django up
workers = multiprocessing.cpu_count() * 4 + 1
threads = multiprocessing.cpu_count() * 4

# Using gevent because of the long blocking calls to the Oracle database
# aiohtto stopped supporting gunicorn / wsgi, hence the switch to gevent
worker_class = "gevent"

daemon = False

proc_name = "uclapi_gunicorn"

timeout = 600
greaceful_timeout = 600
