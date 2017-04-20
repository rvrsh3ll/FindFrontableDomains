#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi
pip install -r requirements.txt
pip install -e git://github.com/davedash/Alexa-Top-Sites.git#egg=alexa-top-sites
git clone https://github.com/rvrsh3ll/Sublist3r.git
touch Sublist3r/__init__.py
git clone https://github.com/rthalley/dnspython
cd dnspython/
python setup.py install
exit 1
