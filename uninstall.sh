#!/bin/bash
if [[ "$EUID" -ne 0 ]]; then
    echo "This script needs to be run as sudo."
    exit 1
fi
rm -rf /usr/share/bmsg
rm /usr/bin/bmsg
