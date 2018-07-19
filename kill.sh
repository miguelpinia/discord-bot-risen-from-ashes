#!/bin/bash

kill $(ps aux | grep 'python bot.py' | grep -v grep | awk '{print $2}')
