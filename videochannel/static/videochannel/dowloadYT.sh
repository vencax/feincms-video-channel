#!/bin/bash

cd /tmp/ee
youtube-dl $2 --write-info-json -q $1 &
PID=`ps aux | grep youtube-dl.py | grep -v "grep" | awk '{print $2}'`
wait $PID