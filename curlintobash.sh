#!/bin/bash
dir=$(mktemp -d)
cd $dir
git clone https://git.gay/bkd/bmsg.git
cd bmsg
sudo ./install.sh