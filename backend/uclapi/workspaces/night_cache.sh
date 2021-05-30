#!/bin/bash
echo -n "Full Redis cache of OccupEye data at: "
date

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin

export ORACLE_HOME=/opt/oracle/instantclient_12_2
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME

pushd /web/uclapi/backend/uclapi
. venv/bin/activate
./manage.py feed_occupeye_cache
./manage.py feed_occupeye_archive --mini

echo "OccupEye caching operation done"
echo
popd
