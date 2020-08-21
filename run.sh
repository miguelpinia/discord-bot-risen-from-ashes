#!/bin/bash

venv=.venv
venvbin=.venv/bin

if [ -d ${venv} ]; then
        rm -rf ${venv}
fi

virtualenv -p python3 ${venv} &&
    source ${venvbin}/activate &&
    pip install -r requirements.txt &&
    echo $(which python) &&
    nohup python src/bot.py 2>&1 | tee log.txt &
