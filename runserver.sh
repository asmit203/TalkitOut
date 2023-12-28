#!/bin/bash
python3 "TalkitOut-Backend (REST-APIs)/manage.py" runserver 8000 & (cd "talkitout-frontend";npm start)