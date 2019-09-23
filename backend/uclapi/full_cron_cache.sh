#!/bin/bash
echo -n "gencache update started at "
date

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin

export ORACLE_HOME=/opt/oracle/instantclient_12_2
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME
ldconfig
pushd /web/uclapi/backend/uclapi
. venv/bin/activate
./manage.py update_gencache --unattended

echo "gencache update done!"
echo
popd
