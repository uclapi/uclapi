ORACLE_VERSION=12_2
ORACLE_SO_VERSION=12.1
export ORACLE_HOME=/opt/oracle/instantclient_$ORACLE_VERSION

sed "s/DB_UCLAPI_HOST=.*/DB_UCLAPI_HOST=$DB_UCLAPI_HOST/" ./backend/uclapi/.env > temp && mv temp ./backend/uclapi/.env 
sed "s/DB_UCLAPI_USERNAME=.*/DB_UCLAPI_USERNAME=$DB_UCLAPI_USERNAME/" ./backend/uclapi/.env > temp && mv temp ./backend/uclapi/.env
sed "s/DB_UCLAPI_PASSWORD=.*/DB_UCLAPI_PASSWORD=$DB_UCLAPI_PASSWORD/" ./backend/uclapi/.env > temp && mv temp ./backend/uclapi/.env
sed "s/DB_CACHE_HOST=.*/DB_CACHE_HOST=$DB_CACHE_HOST/" ./backend/uclapi/.env > temp && mv temp ./backend/uclapi/.env
sed "s/DB_CACHE_USERNAME=.*/DB_CACHE_USERNAME=$DB_CACHE_USERNAME/" ./backend/uclapi/.env > temp && mv temp ./backend/uclapi/.env
sed "s/DB_CACHE_PASSWORD=.*/DB_CACHE_PASSWORD=$DB_CACHE_PASSWORD/" ./backend/uclapi/.env > temp && mv temp ./backend/uclapi/.env
sed "s/REDIS_UCLAPI_HOST=.*/REDIS_UCLAPI_HOST=$REDIS_UCLAPI_HOST/" ./backend/uclapi/.env > temp && mv temp ./backend/uclapi/.env
sed "s/PYTHONUNBUFFERED=.*/PYTHONUNBUFFERED=$PYTHONUNBUFFERED/" ./backend/uclapi/.env > temp && mv temp ./backend/uclapi/.env
sed "s/ORACLE_HOME=.*/ORACLE_HOME=$ORACLE_HOME/" ./backend/uclapi/.env > temp && mv temp ./backend/uclapi/.env
sed "s/DB_UCLAPI_NAME=.*/DB_UCLAPI_NAME=$DB_UCLAPI_NAME/" ./backend/uclapi/.env > temp && mv temp ./backend/uclapi/.env
sed "s/DB_CACHE_NAME=.*/DB_CACHE_NAME=$DB_CACHE_NAME/" ./backend/uclapi/.env > temp && mv temp ./backend/uclapi/.env

cd backend/uclapi
virtualenv --python=python3 venv
. venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py migrate --database gencache
python manage.py create_lock
python manage.py update_gencache
python manage.py runserver 0.0.0.0:8000