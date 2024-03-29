#!/bin/bash

cd /web/uclapi/backend/uclapi || exit
python3 manage.py migrate
python3 manage.py migrate --database gencache

while /bin/true; do
    # Ensure Supervisor is alive first
    ps aux | grep supervisor | grep -q -v grep
    SUPERVISOR_STATUS=$?
    if [ $SUPERVISOR_STATUS -ne 0 ]; then
        service supervisor start
    fi

    # Now check each other service
    for SERVICE in celery-beat-uclapi celery-uclapi-gencache celery-uclapi-worker
    do
        supervisorctl status $SERVICE | grep -q RUNNING
        if [ $? -ne 0 ]; then
            echo "$SERVICE"
            supervisorctl restart $SERVICE
        fi
    done

    sleep 60
done
