#!/bin/bash

if [[ $1 == "" ]]; then
echo "A version must be provided."
exit 1
fi

mkdir v$1
cp crypt.py v$1/crypt.py
cp install.sh v$1/install.sh
cp bmsg.sh v$1/bmsg.sh
cp gui.py v$1/gui.py
cp -r languages/ v$1/languages/
cp readme.md v$1/readme.md
cp LICENSE v$1/LICENSE
cp requirements.txt v$1/requirements.txt
cp setup.sh v$1/setup.sh
cp default_config.ini v$1/default_config.ini
cp bmsg.desktop v$1/bmsg.desktop
cp uninstall.sh v$1/uninstall.sh
tar -czf "bmsg-$1.tar.gz" v$1
rm -rf v$1