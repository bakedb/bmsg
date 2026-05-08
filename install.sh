#!/bin/bash
if [[ "$EUID" -ne 0 ]]; then
    echo "This script needs to be run as sudo."
    exit 1
fi
USER_HOME=$(eval echo "~$SUDO_USER")
mkdir /usr/share/bmsg
cp LICENSE /usr/share/licenses/bmsg
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
mkdir -p "$USER_HOME/.config/bmsg"
cp default_config.ini "$USER_HOME/.config/bmsg/config.ini"
chown -R "$SUDO_USER:$SUDO_USER" "$USER_HOME/.config/bmsg"
cp bmsg.desktop /usr/share/applications/bmsg.desktop
bash /usr/share/bmsg/setup.sh
