#!/bin/bash
if [ "$1" == "update" ]; then
curl -O https://raw.githubusercontent.com/bakedb/bmsg/refs/heads/main/curlintobash.sh && bash curlintobash.sh
fi
cd /usr/share/bmsg
source venv/bin/activate
python gui.py
