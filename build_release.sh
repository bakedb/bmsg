#!/bin/bash
mkdir $1
cp bkd.png $1/bkd.png
cp crypt.py $1/crypt.py
cp install.sh $1/install.sh
cp bmsg.sh $1/bmsg.sh
cp gui.py $1/gui.py
cp intro.py $1/intro.py
cp -r languages/ $1/languages/
cp readme.md $1/readme.md
cp LICENSE $1/LICENSE
cp jingle.wav $1/jingle.wav
cp requirements.txt $1/requirements.txt
cp setup.sh $1/setup.sh
cp default_config.ini $1/default_config.ini
cp bmsg.desktop $1/bmsg.desktop
cp uninstall.sh $1/uninstall.sh
tar -czf "bmsg-$1.tar.gz" $1
rm -rf $1