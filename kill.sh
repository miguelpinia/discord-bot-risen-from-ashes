#!/bin/bash

kill $(ps aux | grep 'python src/bot.py' | grep -v grep | awk '{print $2}')
