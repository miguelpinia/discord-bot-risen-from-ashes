#!/bin/bash

virtualenv -p python3 --no-site-packages --distribute .env && source .env/bin/activate && pip install -r requirements.txt

cd src/ && nohup python bot.py > log.txt 2>&1 &
