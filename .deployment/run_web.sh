#!/bin/bash

cp requirements.txt /app/
cd /app
pwd
ls .
pip install -r requirements.txt
make html
inotifywait -drq -o /tmp/inotifywait.log -e close_write /app/*.rst | while read file; do
    echo ${file}
done

python -m http.server 8000 --directory /app/_build/html