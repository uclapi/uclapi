#!/bin/bash
while /bin/true; do
    # Ensure Supervisor is alive first
    ps aux | grep supervisor | grep -q -v grep
    SUPERVISOR_STATUS = $?
    if [ $SUPERVISOR_STATUS -ne 0 ]; then
        service supervisor start
    fi

    # Now check each other service
    ps aux | grep uclapi | grep -q -v grep
    UCLAPI_STATUS=$?
    ps aux | grep celery | grep -q -v grep
    CELERY_STATUS=$?
    ps aux | grep shibauthorizer | grep -q -v grep
    SHIBAUTHORIZER_STATUS=$?
    ps aux | grep shibresponder | grep -q -v grep
    SHIBRESPONDER_STATUS=$?
    ps aux | grep nginx | grep -q -v grep
    NGINX_STATUS=$?

    if [ $UCLAPI_STATUS -ne 0 ]; then
        echo "UCL API exited"
        supervisorctl restart uclapi
    fi
    if [ $CELERY_STATUS -ne 0 ]; then
        echo "Celery exited"
        supervisorctl restart celery-uclapi
    fi
    if [ $SHIBAUTHORIZER_STATUS -ne 0 ]; then
        echo "Shibboleth Authorizer exited"
        supervisorctl restart shibauthorizer
    fi
    if [ $SHIBRESPONDER_STATUS -ne 0 ]; then
        echo "Shibboleth Responder exited"
        supervisorctl restart shibresponder
    fi
    if [ $NGINX_STATUS -ne 0 ]; then
        echo "Nginx exited"
        supervisorctl restart nginx
    fi

    sleep 60
done