#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi
pip3 uninstall -y dnspython
pip3 install -r requirements.txt
git clone https://github.com/rvrsh3ll/Sublist3r.git
python3 Sublist3r/setup.py install
pip3 install -r Sublist3r/requirements.txt
touch Sublist3r/__init__.py
exit 1
