#!/bin/bash
while /bin/true; do
    # Ensure Supervisor is alive first
    ps aux | grep supervisor | grep -q -v grep
    SUPERVISOR_STATUS=$?
    if [ $SUPERVISOR_STATUS -ne 0 ]; then
        service supervisor start
    fi

    # Now check each other service
    supervisorctl status uclapi | grep -q RUNNING
    UCLAPI_STATUS=$?
    supervisorctl status celery-uclapi | grep -q RUNNING
    CELERY_STATUS=$?

    if [ $UCLAPI_STATUS -ne 0 ]; then
        echo "UCL API exited"
        supervisorctl restart uclapi
    fi
    if [ $CELERY_STATUS -ne 0 ]; then
        echo "Celery exited"
        supervisorctl restart celery-uclapi
    fi
   
    sleep 60
done
