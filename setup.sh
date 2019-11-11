#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi
pip3 uninstall -y dnspython
pip3 install -r requirements.txt
git clone https://github.com/rvrsh3ll/Sublist3r.git
sudo python3 Sublist3r/setup.py install
touch Sublist3r/__init__.py
exit 1
