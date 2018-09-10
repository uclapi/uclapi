import multiprocessing

bind = "0.0.0.0:9000"

# The recommended number of workers is 2 * cores + 1
workers = multiprocessing.cpu_count() * 2 + 1

worker_class = "eventlet"

daemon = False

proc_name = "uclapi_gunicorn"

timeout = 600
greaceful_timeout = 600
