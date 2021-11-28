
from django.db import connections
from django.core.cache import cache
from common.helpers import PrettyJsonResponse

from datetime import datetime, timedelta
from time import sleep
from uclapi.celery import ping_sample_task


def ping_view(request):
    if not request.GET.get('checks'):
        return PrettyJsonResponse({
            "success": True,
        })

    # Early dispatch celery tasks
    celery_connection = {}
    expires = datetime.now() + timedelta(seconds=10)
    queues = ['celery', 'gencache']
    try:
        tasks = [(queue, ping_sample_task.apply_async(expires=expires, queue=queue)) for queue in queues]
    except Exception:
        pass

    # Database connections
    database_connections = {}
    for connection in connections:
        try:
            connections[connection].cursor()
        except Exception as e:
            database_connections[connection] = str(e)
        else:
            database_connections[connection] = "Connected"

    # Cache
    cache_connection = "Failed"
    try:
        cache.set("PING-TEST-CACHE", "Connected", 30)
        cache_connection = cache.get("PING-TEST-CACHE")
    except Exception:
        pass

    # Celery workers
    try:
        while expires > datetime.now() and tasks:
            sleep(0.25)
            for idx, task in enumerate(list(tasks)):
                if task[1].ready() and task[1].result:
                    celery_connection[task[0]] = "Connected"
                    tasks.pop(idx)
    except Exception:
        pass

    for queue in queues:
        print(queue)
        if queue not in celery_connection:
            celery_connection[queue] = "Timeout"

    return PrettyJsonResponse({
        "success": True,
        "ping": {
            "databases": database_connections,
            "cache": cache_connection,
            "celery": celery_connection
        }
    })
