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
ssh -i ~/.ssh/prod.pem ubuntu@ec2-35-176-91-93.eu-west-2.compute.amazonaws.com -t "cd ~; ./deploy.sh;"
ssh -J ubuntu@ec2-35-176-91-93.eu-west-2.compute.amazonaws.com -i ~/.ssh/staging ubuntu@ip-10-0-1-78.eu-west-2.compute.internal -v -t "cd ~; ./deploy.sh;"
