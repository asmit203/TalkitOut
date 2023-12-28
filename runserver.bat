@echo off
start /B python "TalkitOut-Backend (REST-APIs)/manage.py" runserver 8000
cd "talkitout-frontend"
start /B npm start