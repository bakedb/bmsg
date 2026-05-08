#!/bin/bash
if [[ "$EUID" -ne 0 ]]; then
    echo "This script needs to be run as sudo."
    exit 1
fi
USER_HOME=$(eval echo "~$SUDO_USER")
rm -rf /usr/share/bmsg
rm /usr/bin/bmsg
rm -rf "$USER_HOME/.config/bmsg"
rm /usr/share/applications/bmsg.desktop