#!/bin/sh
echo "build web monitor shell begin!"
sh ./build-web-monitor.sh
echo "build web monitor shell end!"
echo "build cache monitor shell begin!"
sh ./build-cache-monitor.sh
echo "build cache monitor shell end!"
