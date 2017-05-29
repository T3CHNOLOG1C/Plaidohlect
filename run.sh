#!/bin/bash
python3 ./run.py &
backgroundPID=$!
cp ./config.ini ./MusicBot/config/token.ini
cd ./MusicBot
python3 ./run.py
trap "kill $backgroundPID && rm ./config/token.ini" EXIT

