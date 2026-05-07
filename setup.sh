#!/bin/bash
cd /usr/share/bmsg
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "All dependencies have been installed. Execute bmsg.sh to launch the application."
