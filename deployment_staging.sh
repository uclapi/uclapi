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
ssh -i staging.pem ubuntu@52.56.191.73 -t "cd ~; ./deploy.sh;"
ssh -J ubuntu@52.56.191.73 -i staging.pem ubuntu@ip-10-0-2-138.eu-west-2.compute.internal -v -t "cd ~; ./deploy.sh;"
