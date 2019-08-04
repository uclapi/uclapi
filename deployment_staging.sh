#!/bin/sh
cd backend/uclapi
rm -rf static/*
mv .env .env.dev
mv .env.staging .env
cd ../../frontend
sudo npm install
npm run build
cd ../backend/uclapi
. venv/bin/activate
./manage.py collectstatic
deactivate
mv .env .env.staging
mv .env.dev .env

