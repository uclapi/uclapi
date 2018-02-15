ORACLE_VERSION=12_2
ORACLE_SO_VERSION=12.1
export ORACLE_HOME=/opt/oracle/instantclient_$ORACLE_VERSION

cd backend/uclapi
virtualenv --python=python3 venv
. venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py migrate --database gencache
python manage.py create_lock
python manage.py update_gencache
python manage.py runserver 0.0.0.0:8000
