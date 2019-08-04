#!/bin/sh
cd backend/uclapi
rm -rf static/*
mv .env .env.dev
mv .env.prod .env
cd ../../frontend
sudo npm install
npm run build
cd ../backend/uclapi
. venv/bin/activate
./manage.py collectstatic
deactivate
mv .env .env.prod
mv .env.dev .env

