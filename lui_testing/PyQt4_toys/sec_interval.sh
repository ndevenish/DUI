#!/bin/bash
echo "start"
sleep 1
echo "second 1"
sleep 1
echo "second 2"
sleep 1
python crash.py
echo "second 3"
sleep 1
echo "second 4"
sleep 1
echo "second 5"
sleep 1
echo "second 6"
exit
