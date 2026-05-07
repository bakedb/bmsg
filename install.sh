#!/bin/bash
if [[ "$EUID" -ne 0 ]]; then
    echo "This script needs to be run as sudo."
    exit 1
fi
mkdir /usr/share/bmsg
cp bkd.png /usr/share/bmsg/bkd.png
cp bmsg.sh /usr/bin/bmsg
cp gui.py /usr/share/bmsg/gui.py
cp intro.py /usr/share/bmsg/intro.py
cp jingle.wav /usr/share/bmsg/jingle.wav
cp -r languages/ /usr/share/bmsg/languages
cp LICENSE /usr/share/bmsg/LICENSE
cp requirements.txt /usr/share/bmsg/requirements.txt
cp startup.py /usr/share/bmsg/startup.py
cp setup.sh /usr/share/bmsg/setup.sh
cp crypt.py /usr/share/bmsg/crypt.py
bash /usr/share/bmsg/setup.sh
