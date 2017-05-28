#!/bin/bash
python3 ./run.py &
backgroundPID=$!
cd ./MusicBot
python3 ./run.py
trap "kill $backgroundPID" EXIT

