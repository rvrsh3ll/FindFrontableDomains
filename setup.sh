#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi
pip3 uninstall -y dnspython
pip3 install -r requirements.txt
git clone https://github.com/aboul3la/Sublist3r.git
cd Sublist3r
python3 setup.py install
pip3 install -r requirements.txt
touch __init__.py
exit 1
