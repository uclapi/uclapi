import multiprocessing

bind = "127.0.0.1:9000"

# Run cores * 4 + 1 workers in gunicorn
# This is set deliberately high in case of long Oracle transactions locking Django up
workers = multiprocessing.cpu_count() * 4 + 1
threads = multiprocessing.cpu_count() * 4

# Using gaiohttp because of the long blocking calls to the Oracle database
worker_class = "gaiohttp"

daemon = False

proc_name = "uclapi_gunicorn"
